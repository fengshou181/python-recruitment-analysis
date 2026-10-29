# -*- coding: utf-8 -*-
"""
BOSS 直聘 接口直连采集器（快速版）

原理：在已登录的 Chrome 页面内用同源 fetch 请求内部搜索接口
/wapi/zpgeek/search/joblist.json，自动携带登录 cookie，
一次返回 30 条完整字段（含技能标签、福利、公司规模、融资阶段），
无需渲染页面，比 DOM 翻页快约 10 倍。

用法：
    python spider/api_reader.py --keywords 数据分析 数据开发 数据仓库 \
        --cities 北京 上海 深圳 --pages-per-city 8
"""
import argparse
import json
import os
import random
import signal
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import websocket

import mysql

DEBUG_HTTP = 'http://127.0.0.1:9222'

CITY_CODES = {
    '北京': 101010100, '上海': 101020100, '广州': 101280100, '深圳': 101280600,
    '杭州': 101210100, '成都': 101270100, '武汉': 101200100, '西安': 101110100,
    '南京': 101190100, '苏州': 101190400, '长沙': 101250100, '重庆': 101040100,
    '郑州': 101180100, '天津': 101030100, '合肥': 101220100, '青岛': 101120200,
    '济南': 101120100, '东莞': 101281600, '佛山': 101280800, '福州': 101230100,
    '厦门': 101230200, '哈尔滨': 101050100, '长春': 101060100, '沈阳': 101070100,
    '大连': 101070200, '呼和浩特': 101080100, '石家庄': 101090100, '太原': 101100100,
    '乌鲁木齐': 101130100, '兰州': 101160100, '银川': 101170100, '南昌': 101240100,
    '贵阳': 101260100, '昆明': 101290100, '南宁': 101300100, '海口': 101310100,
    # 三四线城市
    '无锡': 101190200, '南通': 101190500, '常州': 101191100, '徐州': 101190800,
    '盐城': 101190700, '扬州': 101190600, '镇江': 101190300, '泰州': 101191200,
    '温州': 101210700, '嘉兴': 101210300, '绍兴': 101210500, '金华': 101210900,
    '台州': 101210600, '湖州': 101210200, '泉州': 101230500, '烟台': 101120500,
    '潍坊': 101120600, '临沂': 101120900, '济宁': 101120700, '泰安': 101120800,
    '威海': 101121300, '淄博': 101120300, '珠海': 101280700, '中山': 101281700,
    '惠州': 101280300, '汕头': 101280500, '江门': 101281100, '洛阳': 101180900,
    '新乡': 101180300, '保定': 101090200, '廊坊': 101090600, '唐山': 101090500,
    '绵阳': 101270400, '芜湖': 101220300, '柳州': 101300300, '桂林': 101300500,
    '赣州': 101240700, '九江': 101240200, '襄阳': 101200200, '宜昌': 101200900,
    '株洲': 101250300, '岳阳': 101251000, '包头': 101080200, '吉林': 101060200,
    '大庆': 101050800, '齐齐哈尔': 101050200,
}

running = True

# 搜索关键词 → 入库 type（需与 clean_new.py 的 TYPE_TABLE 对齐）
KEYWORD_TYPE = {
    '数据分析': '数据分析', '数据分析师': '数据分析', 'BI分析师': '数据分析',
    '数据专员': '数据分析', '商业分析': '数据分析', '数据运营': '数据分析',
    '经营分析': '数据分析', '业务分析': '数据分析',
    '数据开发': '数据开发', '大数据开发': '数据开发',
    '数仓工程师': '数据开发', 'ETL工程师': '数据开发',
    '数据仓库': '数据仓库',
    '数据挖掘': '数据挖掘', '机器学习': '数据挖掘',
    '算法工程师': '算法工程师',
}


def find_target():
    try:
        for t in requests.get(DEBUG_HTTP + '/json', timeout=5).json():
            if t.get('type') == 'page' and 'zhipin.com' in t.get('url', ''):
                return t['webSocketDebuggerUrl']
    except Exception:
        pass
    return None


def connect():
    url = find_target()
    if not url:
        return None
    return websocket.create_connection(url, timeout=30, suppress_origin=True)


_id = [0]


def cdp_eval(ws, expr):
    _id[0] += 1
    ws.send(json.dumps({'id': _id[0], 'method': 'Runtime.evaluate',
                        'params': {'expression': expr, 'awaitPromise': True,
                                   'returnByValue': True}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get('id') == _id[0]:
            if 'exceptionDetails' in msg.get('result', {}):
                raise RuntimeError(str(msg['result']['exceptionDetails'])[:200])
            return msg.get('result', {}).get('result', {}).get('value')


def fetch_page(ws, keyword, city_code, page, page_size=30):
    """返回接口 JSON 的 dict"""
    from urllib.parse import quote
    api = (f'/wapi/zpgeek/search/joblist.json?scene=1&query={quote(keyword)}'
           f'&city={city_code}&page={page}&pageSize={page_size}')
    expr = f'''(async () => {{
        try {{
            const r = await fetch("{api}", {{credentials: "include"}});
            const t = await r.text();
            return t;
        }} catch (e) {{ return JSON.stringify({{code: -1, message: String(e)}}); }}
    }})()'''
    raw = cdp_eval(ws, expr)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None


def build_place(j):
    parts = [j.get('cityName') or '', j.get('areaDistrict') or '', j.get('businessDistrict') or '']
    return '·'.join([p for p in parts if p]) or '其他'


def insert_jobs(sql, jobs, keyword, seen_jobs):
    new = 0
    db_type = KEYWORD_TYPE.get(keyword, keyword)
    for j in jobs:
        name = (j.get('jobName') or '').strip()
        company = (j.get('brandName') or '').strip()
        place = build_place(j)
        salary = (j.get('salaryDesc') or '').strip()
        if not name or not salary:
            continue
        key = (name, company, place, salary)
        if key in seen_jobs:
            continue
        seen_jobs.add(key)
        try:
            sql.saveData(
                name, place, company,
                (j.get('brandScaleName') or '').strip(),
                salary,
                (j.get('jobDegree') or '').strip(),
                (j.get('jobExperience') or '').strip(),
                ','.join(j.get('jobLabels') or []),
                ','.join(j.get('skills') or []),
                ','.join(j.get('welfareList') or []),
                db_type,
            )
            new += 1
        except Exception as e:
            print(f'>>> 入库失败: {e}')
    return new


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keywords', nargs='+', required=True)
    parser.add_argument('--cities', nargs='+', required=True)
    parser.add_argument('--pages-per-city', type=int, default=1,
                        help='每城每词的页数（接口已限制深翻，默认1页=15条）')
    parser.add_argument('--page-size', type=int, default=15)
    parser.add_argument('--delay-min', type=float, default=8.0)
    parser.add_argument('--delay-max', type=float, default=11.0)
    parser.add_argument('--rest-every', type=int, default=30)
    parser.add_argument('--rest-min', type=int, default=60)
    parser.add_argument('--rest-max', type=int, default=120)
    parser.add_argument('--max-retries', type=int, default=2)
    args = parser.parse_args()

    def stop(*_):
        global running
        running = False
    signal.signal(signal.SIGINT, stop)

    sql = mysql.MySql()
    seen_jobs = set()
    try:
        sql.cursor.execute('SELECT name,company,place,salary FROM row_data ORDER BY num DESC LIMIT 100000')
        for r in sql.cursor.fetchall():
            seen_jobs.add((r['name'], r['company'], r['place'], r['salary']))
        print(f'>>> 已加载历史去重键 {len(seen_jobs)} 条')
    except Exception as e:
        print(f'>>> 加载历史键失败（忽略）: {e}')

    total = 0
    pages = 0
    t_start = time.time()

    for keyword in args.keywords:
        if not running:
            break
        for city in args.cities:
            if not running:
                break
            code = CITY_CODES.get(city)
            if not code:
                print(f'>>> 未知城市 {city}，跳过')
                continue
            city_new = 0
            empty_pages = 0
            for page in range(1, args.pages_per_city + 1):
                if not running:
                    break
                ws = None
                data = None
                for attempt in range(args.max_retries + 1):
                    try:
                        ws = connect()
                        if not ws:
                            raise RuntimeError('找不到 BOSS 页面')
                        data = fetch_page(ws, keyword, code, page, args.page_size)
                        break
                    except Exception as e:
                        if attempt < args.max_retries:
                            wait = random.uniform(8, 20)
                            print(f'>>> {keyword}/{city} 第{page}页 请求失败({type(e).__name__})，{wait:.0f}秒后重试', flush=True)
                            time.sleep(wait)
                        else:
                            print(f'>>> {keyword}/{city} 第{page}页 放弃: {e}', flush=True)
                    finally:
                        if ws:
                            try:
                                ws.close()
                            except Exception:
                                pass

                if not data:
                    empty_pages += 1
                    if empty_pages >= 3:
                        print(f'>>> {city} 连续空页，跳过', flush=True)
                        break
                    continue

                if data.get('code') != 0:
                    print(f'>>> 接口返回异常 code={data.get("code")} msg={data.get("message")}', flush=True)
                    wait = random.uniform(180, 300)
                    print(f'>>> 疑似风控，休息 {wait:.0f} 秒', flush=True)
                    time.sleep(wait)
                    continue

                zp = data.get('zpData') or {}
                jobs = zp.get('jobList') or []
                if not jobs:
                    empty_pages += 1
                    if empty_pages >= 2:
                        break
                    continue
                empty_pages = 0
                pages += 1

                new = insert_jobs(sql, jobs, keyword, seen_jobs)
                total += new
                city_new += new
                print(f'>>> {keyword} | {city} 第{page}页 入库 {new}/{len(jobs)} 条，'
                      f'城市累计 {city_new}，总计 {total} 条', flush=True)

                if not zp.get('hasMore'):
                    break

                if args.rest_every > 0 and pages % args.rest_every == 0:
                    rest = random.uniform(args.rest_min, args.rest_max)
                    print(f'>>> 已采 {pages} 页，休息 {rest:.0f} 秒', flush=True)
                    time.sleep(rest)
                else:
                    time.sleep(random.uniform(args.delay_min, args.delay_max))

            print(f'>>> 城市 {city} 完成，新增 {city_new} 条', flush=True)

    cost = time.time() - t_start
    print(f'>>> 结束：{pages} 页，新增 {total} 条，耗时 {cost / 60:.1f} 分钟')


if __name__ == '__main__':
    main()
