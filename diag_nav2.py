# -*- coding: utf-8 -*-
"""诊断2：抓取过渡页全文 + 监听窗口句柄变化"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spider.bosszp_spider_v2 import build_driver

d = build_driver()
try:
    url = 'https://www.zhipin.com/web/geek/job?query=Python&city=101010100&page=1'
    try:
        d.get(url)
    except Exception as e:
        print('get exception:', type(e).__name__, str(e)[:200])
    time.sleep(4)
    src = d.page_source or ''
    print('=== 过渡页全文(前3000字) ===')
    print(src[:3000])
    print('=== handles ===')
    for i in range(4):
        time.sleep(4)
        try:
            print(f'[{i}] handles={d.window_handles} current={d.current_window_handle} url={d.current_url}')
        except Exception as e:
            print(f'[{i}] error:', type(e).__name__, str(e)[:150])
finally:
    d.quit()
