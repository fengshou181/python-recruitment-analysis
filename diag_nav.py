# -*- coding: utf-8 -*-
"""诊断：用与 v2 相同的配置打开 Boss 搜索页，打印真实停留的 URL/标题/页面特征"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spider.bosszp_spider_v2 import build_driver

d = build_driver()
try:
    url = 'https://www.zhipin.com/web/geek/job?query=Python&city=101010100&page=1'
    print('GET ->', url)
    try:
        d.get(url)
    except Exception as e:
        print('get exception:', type(e).__name__, str(e)[:200])
    for i in range(6):
        time.sleep(5)
        cur = d.current_url
        title = d.title
        src = d.page_source or ''
        print(f'[{i}] url={cur} | title={title} | len={len(src)} '
              f'| has_jobcard={"job-card-wrapper" in src} | has_login={"登录" in src}')
finally:
    d.quit()
