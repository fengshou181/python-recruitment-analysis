# -*- coding: utf-8 -*-
"""探针：读取当前 BOSS 页面 DOM，测试各选择器命中数"""
import json
import requests
import websocket

ts = requests.get('http://127.0.0.1:9222/json', timeout=5).json()
pages = [t for t in ts if t.get('type') == 'page']
for p in pages:
    print('PAGE:', p['url'][:110])
t = [p for p in pages if 'zhipin.com' in p['url']][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], timeout=10, suppress_origin=True)


def ev(expr, _i=[0]):
    _i[0] += 1
    ws.send(json.dumps({'id': _i[0], 'method': 'Runtime.evaluate',
                        'params': {'expression': expr, 'returnByValue': True}}))
    while True:
        m = json.loads(ws.recv())
        if m.get('id') == _i[0]:
            return m['result']['result'].get('value')


print('url:', ev('location.href'))
sels = ['li.job-card-wrapper', '.job-card-wrapper', '.job-list-box li',
        '[class*="job-card"]', '.job-card-box', 'ul.job-list-box > li',
        '.search-job-result li', '[class*="job-list"] li', 'li[class*="card"]']
for s in sels:
    try:
        print(f'{s} => {ev(f"document.querySelectorAll(\'{s}\').length")}')
    except Exception as e:
        print(s, 'ERR', e)

# 打印第一张卡片外层类名结构
probe = ev("""(function(){
  var li = document.querySelector('ul li');
  var out = [];
  document.querySelectorAll('ul').forEach(function(u){
    if(u.querySelectorAll('li').length > 5){ out.push(u.className + ' -> ' + (u.querySelector('li')||{}).className); }
  });
  return out.join('\\n');
})()""")
print('--- ul/li class 概览 ---')
print(probe)
ws.close()
