# -*- coding: utf-8 -*-
"""
BOSS 直聘采集器 —— 裸 CDP 模式（无 chromedriver，对页面零侵入）

前提：Chrome 已带 --remote-debugging-port=9222 启动且已登录 BOSS 直聘。

模式：
  1) 被动模式：人工翻页，脚本只读当前页入库
       python spider/cdp_reader.py --keyword python
  2) 自动模式：脚本自行 JS 翻页（深页会重复，默认每查询最多3页）
       python spider/cdp_reader.py --keyword python --auto
  3) 多城市矩阵：逐城市自动翻页（绕过单查询深页上限）
       python spider/cdp_reader.py --keyword python --auto --cities 深圳 北京 上海
"""
import os
import sys
import json
import time
import random
import signal
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import websocket

import mysql
from spider.bosszp_spider_v2 import parse_jobs, CITIES

DEBUG_HTTP = 'http://127.0.0.1:9222/json'


def find_zhipin_target():
    for t in requests.get(DEBUG_HTTP, timeout=5).json():
        if t.get('type') == 'page' and 'zhipin.com' in t.get('url', ''):
            return t
    return None


def cdp_eval(ws, expr, _id=[0]):
    _id[0] += 1
    ws.send(json.dumps({
        'id': _id[0], 'method': 'Runtime.evaluate',
        'params': {'expression': expr, 'returnByValue': True},
    }))
    while True:
        msg = json.loads(ws.recv())
        if msg.get('id') == _id[0]:
            return msg.get('result', {}).get('result', {}).get('value')


def split_exp_edu(text):
    education = ''
    for kw in ['博士', '硕士', '本科', '大专', '中专/中技', '高中', '学历不限']:
        if kw in text:
            education = kw
            break
    return text.replace(education, '').strip() or text, education


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keyword', default='python')
    parser.add_argument('--filter-arg', default='',
                        help='追加到搜索 URL 的筛选参数，如 "experience=105&degree=203"')
    parser.add_argument('--pages', type=int, default=60, help='总页数上限')
    parser.add_argument('--interval', type=int, default=4)
    parser.add_argument('--auto', action='store_true')
    parser.add_argument('--cities', nargs='+', default=None)
    parser.add_argument('--pages-per-city', type=int, default=3)
    # 反风控参数
    parser.add_argument('--delay-min', type=int, default=12, help='翻页随机延迟下限(秒)')
    parser.add_argument('--delay-max', type=int, default=25, help='翻页随机延迟上限(秒)')
    parser.add_argument('--rest-every', type=int, default=10, help='每采多少页休息一次')
    parser.add_argument('--rest-min', type=int, default=120, help='休息时长下限(秒)')
    parser.add_argument('--rest-max', type=int, default=240, help='休息时长上限(秒)')
    parser.add_argument('--max-retries', type=int, default=3, help='被风控后重试次数')
    parser.add_argument('--retry-wait-min', type=int, default=60, help='重试前等待下限(秒)')
    parser.add_argument('--retry-wait-max', type=int, default=180, help='重试前等待上限(秒)')
    args = parser.parse_args()

    sql = mysql.MySql()
    seen_pages, seen_jobs = set(), set()
    try:
        sql.cursor.execute('SELECT name,company,place,salary FROM row_data ORDER BY num DESC LIMIT 20000')
        for r in sql.cursor.fetchall():
            seen_jobs.add((r['name'], r['company'], r['place'], r['salary']))
        print(f'>>> 已加载历史去重键 {len(seen_jobs)} 条')
    except Exception as e:
        print(f'>>> 加载历史键失败（忽略）: {e}')

    total = 0
    total_pages = 0
    running = True

    def stop(*_):
        nonlocal running
        running = False
    signal.signal(signal.SIGINT, stop)

    def open_target():
        t = find_zhipin_target()
        if not t:
            return None
        ws = websocket.create_connection(t['webSocketDebuggerUrl'], timeout=15,
                                         suppress_origin=True)
        return ws

    def read_page(ws):
        url = cdp_eval(ws, 'location.href') or ''
        html = cdp_eval(ws, 'document.documentElement.outerHTML') or ''
        return url, html

    def insert_jobs(jobs):
        new = 0
        for j in jobs:
            key = (j['job_name'], j['job_company'], j['job_place'], j['job_salary'])
            if key in seen_jobs:
                continue
            seen_jobs.add(key)
            experience, education = split_exp_edu(j['job_education_exp'])
            try:
                sql.saveData(j['job_name'], j['job_place'], j['job_company'],
                             j['job_scale'], j['job_salary'], education,
                             experience, j['job_label'], j['job_skill'],
                             j['job_welfare'], args.keyword.lower())
                new += 1
            except Exception as e:
                print(f'>>> 入库失败: {e}')
        return new

    def goto(ws, url):
        cdp_eval(ws, f'location.href={json.dumps(url)}')
        time.sleep(random.uniform(5, 8))
        # 模拟真人浏览滚动，降低风控特征
        cdp_eval(ws, 'window.scrollTo(0, document.body.scrollHeight * 0.5)')

    def maybe_rest():
        """每采 rest_every 页休息 2~4 分钟，模拟真人"""
        if args.rest_every > 0 and total_pages > 0 and total_pages % args.rest_every == 0:
            rest = random.uniform(args.rest_min, args.rest_max)
            print(f'>>> 已采 {total_pages} 页，休息 {rest:.0f} 秒', flush=True)
            time.sleep(rest)

    def next_url(url):
        if 'page=' in url:
            import re
            return re.sub(r'page=(\d+)', lambda m: f'page={int(m.group(1)) + 1}', url)
        return url + ('&' if '?' in url else '?') + 'page=2'

    def wait_change(ws, old_url, old_html):
        for _ in range(15):
            time.sleep(2)
            try:
                cur, html = read_page(ws)
                if cur != old_url and html != old_html:
                    time.sleep(random.uniform(1, 2))
                    return True
            except Exception:
                time.sleep(2)
        return False

    print('=' * 64)
    mode = '多城市自动矩阵' if (args.auto and args.cities) else ('自动翻页' if args.auto else '被动（人工翻页）')
    print(f'模式: {mode} | 关键词: {args.keyword} | 总页数上限: {args.pages}')
    print('=' * 64)

    def collect_here(max_pages):
        """在当前查询下采集（被动=只读当前；自动=自行翻页）。返回 True 表示应整体停止"""
        nonlocal total, total_pages
        done = 0
        zero_streak = 0
        empty_streak = 0
        skip_streak = 0
        while running and done < max_pages and total_pages < args.pages:
            ws = open_target()
            if not ws:
                time.sleep(args.interval)
                continue
            try:
                url, html = read_page(ws)
                if 'zhipin.com' not in url:
                    time.sleep(args.interval)
                    continue
                jobs = parse_jobs(html)
                if not jobs:
                    empty_streak += 1
                    if empty_streak >= 3:
                        print('>>> 连续未解析到职位（可能被风控）', flush=True)
                        return 'blocked'
                    time.sleep(args.interval)
                    continue
                empty_streak = 0

                fp = f"{url}|{jobs[0]['job_name']}|{jobs[-1]['job_name']}|{len(jobs)}"
                if fp in seen_pages:
                    # 已采过的页：快速跳过往深翻，不计入无新数据判定
                    skip_streak += 1
                    if skip_streak >= 8:
                        break  # 连续 8 页都是旧页，说明翻到底了
                    if args.auto:
                        time.sleep(random.uniform(args.delay_min, args.delay_max))
                        goto(ws, next_url(url))
                        if not wait_change(ws, url, html):
                            return 'blocked'
                        done += 1
                    else:
                        time.sleep(args.interval)
                    continue
                skip_streak = 0
                seen_pages.add(fp)
                total_pages += 1
                done += 1

                new = insert_jobs(jobs)
                total += new
                zero_streak = 0 if new > 0 else zero_streak + 1
                print(f'>>> 第 {total_pages} 页入库 {new}/{len(jobs)} 条，累计 {total} 条', flush=True)
                if zero_streak >= 2:
                    break

                if args.auto:
                    time.sleep(random.uniform(args.delay_min, args.delay_max))
                    maybe_rest()
                    goto(ws, next_url(url))
                    if not wait_change(ws, url, html):
                        print('>>> 翻页等待超时', flush=True)
                        return 'blocked'
                else:
                    time.sleep(args.interval)
            except Exception as e:
                print(f'>>> 读取异常: {type(e).__name__} {e}', flush=True)
                time.sleep(args.interval)
            finally:
                try:
                    ws.close()
                except Exception:
                    pass
        return False

    if args.auto and args.cities:
        name2code = {c['name']: c['code'] for c in CITIES}
        blocked_cities = 0
        for name in args.cities:
            if not running or total_pages >= args.pages:
                break
            code = name2code.get(name)
            if not code:
                print(f'>>> 未知城市 {name}，跳过')
                continue
            base = f'https://www.zhipin.com/web/geek/jobs?city={code}&query={args.keyword}'
            if args.filter_arg:
                base += f'&{args.filter_arg}'
            city_blocked = True
            for attempt in range(args.max_retries + 1):
                ws = open_target()
                if not ws:
                    print('>>> 找不到 BOSS 页面，整体停止')
                    running = False
                    break
                print(f'>>> 切换城市: {name} -> {base}', flush=True)
                try:
                    goto(ws, base)
                finally:
                    ws.close()
                if collect_here(args.pages_per_city) != 'blocked':
                    city_blocked = False
                    break
                if attempt < args.max_retries:
                    wait = random.uniform(args.retry_wait_min, args.retry_wait_max)
                    print(f'>>> {name} 疑似被风控，{wait:.0f} 秒后重试（第 {attempt + 1}/{args.max_retries} 次）', flush=True)
                    time.sleep(wait)
            if not running:
                break
            if city_blocked:
                blocked_cities += 1
                print(f'>>> {name} 重试仍被拦，跳过该城市', flush=True)
                if blocked_cities >= 3:
                    print('>>> 连续 3 城被拦，整体停止，建议冷却 30 分钟后再跑', flush=True)
                    break
            else:
                blocked_cities = 0
                # 城市间随机间隔，模拟人工切换
                time.sleep(random.uniform(args.delay_min, args.delay_max))
    else:
        collect_here(args.pages)

    print(f'>>> 结束：共 {total_pages} 页，新增 {total} 条')


if __name__ == '__main__':
    main()
