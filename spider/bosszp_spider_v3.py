# -*- coding: utf-8 -*-
"""
Boss直聘爬虫 v3 —— 被动采集模式（应对 browser-check 反自动化检测）

原理：以调试端口启动一个"干净的"Chrome（非 chromedriver 拉起，无自动化特征），
用户在其中正常登录、搜索、翻页；脚本通过 CDP 接管，只读取当前页面内容并解析入库，
不主动导航，因此不触发反爬。

用法（项目根目录）：
    python spider/bosszp_spider_v2.py            # 旧版（会被反爬踢出，勿用）
    python spider/bosszp_spider_v3.py --keyword python --pages 30

操作：
    1. 脚本启动后会弹出 Chrome 窗口并打开 BOSS 直聘首页
    2. 在窗口里扫码登录，然后搜索关键词、选择城市
    3. 之后逐页点击"下一页"，脚本每 4 秒检测当前页，发现是新一页职位列表就自动入库
    4. 达到 --pages 页数或按 Ctrl+C 结束
"""
import os
import sys
import time
import signal
import argparse
import subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import mysql
from spider.bosszp_spider_v2 import parse_jobs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = os.path.join(BASE_DIR, 'chrome_profile')
DEBUG_PORT = 9222

CHROME = r'C:\Users\Lenovo\AppData\Local\Google\Chrome\Application\chrome.exe'


def launch_chrome():
    """手动方式启动带调试端口的 Chrome（无自动化特征）"""
    proc = subprocess.Popen([
        CHROME,
        f'--remote-debugging-port={DEBUG_PORT}',
        f'--user-data-dir={PROFILE_DIR}',
        '--start-maximized',
        'https://www.zhipin.com/',
    ])
    time.sleep(4)
    return proc


def attach_driver():
    options = Options()
    options.debugger_address = f'127.0.0.1:{DEBUG_PORT}'
    driver = webdriver.Chrome(options=options)
    return driver


def split_exp_edu(text):
    education = ''
    for kw in ['博士', '硕士', '本科', '大专', '中专/中技', '高中', '学历不限']:
        if kw in text:
            education = kw
            break
    experience = text.replace(education, '').strip() or text
    return experience, education


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keyword', default='python', help='入库时的 type 字段（决定清洗后进入哪个子表）')
    parser.add_argument('--pages', type=int, default=30, help='采集多少页后自动停止')
    parser.add_argument('--interval', type=int, default=4, help='页面检测间隔秒数')
    args = parser.parse_args()

    sql = mysql.MySql()
    chrome_proc = launch_chrome()
    driver = attach_driver()

    print('=' * 64)
    print('被动采集已就绪。请在 Chrome 窗口中：')
    print('  1) 扫码登录 BOSS 直聘')
    print('  2) 搜索岗位关键词、选择城市')
    print('  3) 进入职位列表后逐页点"下一页"，脚本会自动抓取每一页')
    print('=' * 64)

    seen_pages = set()      # 已采集的页面指纹
    seen_jobs = set()       # 职位去重
    total = 0
    running = True

    def stop(*_):
        nonlocal running
        running = False
    signal.signal(signal.SIGINT, stop)

    try:
        while running and len(seen_pages) < args.pages:
            try:
                url = driver.current_url
                src = driver.page_source or ''
            except Exception as e:
                print(f'>>> 读取页面失败: {e}')
                time.sleep(args.interval)
                continue

            if 'zhipin.com' not in url:
                time.sleep(args.interval)
                continue

            jobs = parse_jobs(src)
            if not jobs:
                time.sleep(args.interval)
                continue

            # 页面指纹：URL + 首尾职位名，防止同页重复采集
            fp = f"{url}|{jobs[0]['job_name']}|{jobs[-1]['job_name']}|{len(jobs)}"
            if fp in seen_pages:
                time.sleep(args.interval)
                continue
            seen_pages.add(fp)

            page_new = 0
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
                    page_new += 1
                except Exception as e:
                    print(f'>>> 入库失败: {e}')
            total += page_new
            print(f'>>> 第 {len(seen_pages)} 页入库 {page_new}/{len(jobs)} 条，累计 {total} 条')

            time.sleep(args.interval)
    finally:
        print(f'>>> 采集结束：共 {len(seen_pages)} 页，新增 {total} 条到 row_data')
        print('>>> 下一步可运行 python datahandle.py 清洗到 handled_data 及各岗位子表')
        try:
            chrome_proc.terminate()
        except Exception:
            pass


if __name__ == '__main__':
    main()
