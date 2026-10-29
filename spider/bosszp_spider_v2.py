# -*- coding: utf-8 -*-
"""
Boss直聘爬虫 v2（2026 现行页面结构）
- 半自动：启动 Chrome 后由人工扫码登录，登录态保存在 spider/chrome_profile
- 解析现行 geek 端列表页 DOM，选择器带多组容错
- 命中安全验证/无数据时保存 debug HTML 并暂停等人工处理
- 数据写入 spiderdatabase.row_data，之后可跑 datahandle.py 清洗到各子表

用法（在项目根目录执行）：
    python spider/bosszp_spider_v2.py --keywords Python --cities 北京 上海 --pages 2
"""
import os
import sys
import time
import random
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import mysql

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = os.path.join(BASE_DIR, 'chrome_profile')
DEBUG_DIR = os.path.join(BASE_DIR, 'debug_html')

CITIES = [
    {"name": "北京", "code": 101010100}, {"name": "上海", "code": 101020100},
    {"name": "广州", "code": 101280100}, {"name": "深圳", "code": 101280600},
    {"name": "杭州", "code": 101210100}, {"name": "成都", "code": 101270100},
    {"name": "武汉", "code": 101200100}, {"name": "西安", "code": 101110100},
    {"name": "南京", "code": 101190100}, {"name": "苏州", "code": 101190400},
    {"name": "长沙", "code": 101250100}, {"name": "重庆", "code": 101040100},
    {"name": "郑州", "code": 101180100}, {"name": "天津", "code": 101030100},
    {"name": "合肥", "code": 101220100}, {"name": "青岛", "code": 101120200},
    {"name": "济南", "code": 101120100}, {"name": "东莞", "code": 101281600},
    {"name": "佛山", "code": 101280800}, {"name": "福州", "code": 101230100},
    {"name": "厦门", "code": 101230200},
    {"name": "哈尔滨", "code": 101050100}, {"name": "长春", "code": 101060100},
    {"name": "沈阳", "code": 101070100}, {"name": "大连", "code": 101070200},
    {"name": "呼和浩特", "code": 101080100}, {"name": "石家庄", "code": 101090100},
    {"name": "太原", "code": 101100100}, {"name": "乌鲁木齐", "code": 101130100},
    {"name": "兰州", "code": 101160100}, {"name": "银川", "code": 101170100},
    {"name": "南昌", "code": 101240100}, {"name": "贵阳", "code": 101260100},
    {"name": "昆明", "code": 101290100}, {"name": "南宁", "code": 101300100},
    {"name": "海口", "code": 101310100},
    # 三四线城市（扩量）
    {"name": "无锡", "code": 101190200}, {"name": "南通", "code": 101190500},
    {"name": "常州", "code": 101191100}, {"name": "徐州", "code": 101190800},
    {"name": "盐城", "code": 101190700}, {"name": "扬州", "code": 101190600},
    {"name": "镇江", "code": 101190300}, {"name": "泰州", "code": 101191200},
    {"name": "温州", "code": 101210700}, {"name": "嘉兴", "code": 101210300},
    {"name": "绍兴", "code": 101210500}, {"name": "金华", "code": 101210900},
    {"name": "台州", "code": 101210600}, {"name": "湖州", "code": 101210200},
    {"name": "泉州", "code": 101230500}, {"name": "烟台", "code": 101120500},
    {"name": "潍坊", "code": 101120600}, {"name": "临沂", "code": 101120900},
    {"name": "济宁", "code": 101120700}, {"name": "泰安", "code": 101120800},
    {"name": "威海", "code": 101121300}, {"name": "淄博", "code": 101120300},
    {"name": "珠海", "code": 101280700}, {"name": "中山", "code": 101281700},
    {"name": "惠州", "code": 101280300}, {"name": "汕头", "code": 101280500},
    {"name": "江门", "code": 101281100}, {"name": "洛阳", "code": 101180900},
    {"name": "新乡", "code": 101180300}, {"name": "保定", "code": 101090200},
    {"name": "廊坊", "code": 101090600}, {"name": "唐山", "code": 101090500},
    {"name": "绵阳", "code": 101270400}, {"name": "芜湖", "code": 101220300},
    {"name": "柳州", "code": 101300300}, {"name": "桂林", "code": 101300500},
    {"name": "赣州", "code": 101240700}, {"name": "九江", "code": 101240200},
    {"name": "襄阳", "code": 101200200}, {"name": "宜昌", "code": 101200900},
    {"name": "株洲", "code": 101250300}, {"name": "岳阳", "code": 101251000},
    {"name": "包头", "code": 101080200}, {"name": "吉林", "code": 101060200},
    {"name": "大庆", "code": 101050800}, {"name": "齐齐哈尔", "code": 101050200},
]


def build_driver():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    options.add_argument(f'--user-data-dir={PROFILE_DIR}')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    # 不等待页面完全加载（目标站资源可能挂起导致 get 卡住）
    options.page_load_strategy = 'none'
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)
    return driver


def save_debug_html(driver, tag):
    os.makedirs(DEBUG_DIR, exist_ok=True)
    path = os.path.join(DEBUG_DIR, f'{tag}_{int(time.time())}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print(f'>>> 已保存调试页面: {path}')


def is_security_check(driver):
    url = driver.current_url
    title = driver.title or ''
    return 'security-check' in url or '验证' in title or '安全' in title


def wait_for_jobs(driver, timeout=600):
    """轮询等待页面出现职位卡片；期间的人工登录/滑块验证由用户在浏览器完成。
    返回解析出的职位列表，超时返回 None。"""
    waited = 0
    hint_at = 0
    while waited < timeout:
        if is_security_check(driver):
            if waited >= hint_at:
                print('>>> 命中安全验证，请在浏览器窗口中手动完成滑块/验证，脚本会自动继续...')
                hint_at = waited + 30
        else:
            jobs = parse_jobs(driver.page_source)
            if jobs:
                return jobs
            if waited >= hint_at:
                print('>>> 页面暂无职位数据：请在浏览器窗口中完成登录（扫码），或检查页面状态，脚本会自动继续...')
                hint_at = waited + 30
        time.sleep(3)
        waited += 3
    return None


def first_text(node, selectors):
    """多组选择器容错取文本"""
    for sel in selectors:
        el = node.select_one(sel)
        if el:
            return el.get_text(strip=True)
    return ''


def all_texts(node, selectors):
    for sel in selectors:
        els = node.select(sel)
        if els:
            return ' '.join(e.get_text(strip=True) for e in els)
    return ''


def decode_font(text):
    """BOSS 薪资数字用私有区字体混淆：\\ue031-\\ue03a 依次对应 0-9，需解码"""
    if not text:
        return text
    out = []
    for ch in text:
        code = ord(ch)
        if 0xE031 <= code <= 0xE03A:
            out.append(str(code - 0xE031))
        else:
            out.append(ch)
    return ''.join(out)


def parse_jobs(html):
    """解析一页职位卡片，返回字段字典列表。
    现行（2026）结构：li.job-card-box（含 .job-name/.job-salary/.tag-list/.boss-name/.company-location），
    列表页不再展示公司规模/技能标签/福利，这些字段留空。
    兼容旧结构 li.job-card-wrapper。"""
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.select('.job-card-box')
    if cards:
        jobs = []
        for card in cards:
            job_name = first_text(card, ['.job-name'])
            job_salary = decode_font(first_text(card, ['.job-salary']))
            if not job_name or not job_salary:
                continue
            tags = [decode_font(li.get_text(strip=True)) for li in card.select('.tag-list li')]
            jobs.append({
                'job_name': job_name,
                'job_place': first_text(card, ['.company-location']),
                'job_salary': job_salary,
                'job_company': first_text(card, ['.boss-name']),
                'job_scale': '',
                'job_education_exp': ' '.join(tags),
                'job_label': '',
                'job_skill': '',
                'job_welfare': '',
            })
        return jobs

    # 旧版结构回退
    cards = soup.select('li.job-card-wrapper') or soup.select('.job-card-wrapper')
    jobs = []
    for card in cards:
        job_name = first_text(card, ['.job-name', '.job-title .job-name'])
        if not job_name:
            continue
        jobs.append({
            'job_name': job_name,
            'job_place': first_text(card, ['.job-area', '.job-area-wrapper', '.job-title .job-area']),
            'job_salary': first_text(card, ['.salary', '.job-salary', 'span.red']),
            'job_company': first_text(card, ['.company-name', '.company-text .name', '.boss-name']),
            'job_scale': all_texts(card, ['.company-tag-list li', '.company-text p']),
            'job_education_exp': all_texts(card, ['.job-card-footer .tag-list li',
                                                  '.job-info .tag-list li',
                                                  'ul.tag-list li']),
            'job_label': first_text(card, ['.job-card-footer .info-desc', '.info-desc']),
            'job_skill': all_texts(card, ['.job-card-footer .tag-list li', '.job-tags li']),
            'job_welfare': first_text(card, ['.info-desc', '.job-card-footer .info-desc']),
        })
    return jobs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keywords', nargs='+', default=['Python'])
    parser.add_argument('--cities', nargs='+', default=['北京'])
    parser.add_argument('--pages', type=int, default=2)
    args = parser.parse_args()

    cities = [c for c in CITIES if c['name'] in args.cities]
    if not cities:
        print('>>> 没有匹配的城市，可选：', ' '.join(c['name'] for c in CITIES))
        return

    sql = mysql.MySql()
    driver = build_driver()

    try:
        print('=' * 60)
        print('即将打开 Chrome 窗口采集。若弹出登录/验证，请在窗口中手动完成，')
        print('脚本检测到职位列表后会自动继续，无需在终端操作。')
        print('=' * 60)

        total = 0
        for key in args.keywords:
            for city in cities:
                city_count = 0
                for page in range(1, args.pages + 1):
                    url = (f'https://www.zhipin.com/web/geek/job'
                           f'?query={key}&city={city["code"]}&page={page}')
                    time.sleep(random.uniform(3, 6))
                    try:
                        driver.get(url)
                    except Exception as e:
                        print(f'>>> 导航异常（忽略，继续轮询）: {e}')

                    jobs = wait_for_jobs(driver)
                    if jobs is None:
                        print(f'>>> [{key}|{city["name"]}|p{page}] 等待超时，跳过')
                        save_debug_html(driver, f'timeout_{key}_{city["name"]}_p{page}')
                        continue

                    for j in jobs:
                        # 拆分 "3-5年 本科" 这类经验学历混合文本
                        exp_edu = j['job_education_exp']
                        education = ''
                        for kw in ['博士', '硕士', '本科', '大专', '学历不限', '高中', '中专/中技']:
                            if kw in exp_edu:
                                education = kw
                                break
                        experience = exp_edu.replace(education, '').strip() or exp_edu
                        try:
                            sql.saveData(j['job_name'], j['job_place'], j['job_company'],
                                         j['job_scale'], j['job_salary'], education,
                                         experience, j['job_label'], j['job_skill'],
                                         j['job_welfare'], key.lower())
                            city_count += 1
                        except Exception as e:
                            print(f'>>> 入库失败: {e}')

                    print(f'>>> [{key}|{city["name"]}|p{page}] 解析 {len(jobs)} 条，累计入库 {city_count} 条')
                total += city_count
                print(f'>>> 城市 "{city["name"]}" 完成，入库 {city_count} 条')
        print(f'>>> 全部完成，共入库 {total} 条')
        print('>>> 下一步可运行 python datahandle.py 清洗到 handled_data 及各岗位子表')
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
