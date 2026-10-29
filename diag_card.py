# -*- coding: utf-8 -*-
"""探针2：打印一个 .job-card-box 的内部结构"""
import json
import requests
import websocket

ts = requests.get('http://127.0.0.1:9222/json', timeout=5).json()
t = [p for p in ts if p.get('type') == 'page' and 'zhipin.com' in p['url']][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], timeout=10, suppress_origin=True)


def ev(expr, _i=[0]):
    _i[0] += 1
    ws.send(json.dumps({'id': _i[0], 'method': 'Runtime.evaluate',
                        'params': {'expression': expr, 'returnByValue': True}}))
    while True:
        m = json.loads(ws.recv())
        if m.get('id') == _i[0]:
            return m['result']['result'].get('value')


html = ev("document.querySelector('.job-card-box').outerHTML")
print(html[:4000])
ws.close()
