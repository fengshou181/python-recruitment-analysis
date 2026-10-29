# -*- coding: utf-8 -*-
"""探针3：对比不同位置的 job-card-box 结构"""
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


for idx in (1, 5, 30, 45):
    html = ev(f"document.querySelectorAll('.job-card-box')[{idx}] && document.querySelectorAll('.job-card-box')[{idx}].outerHTML")
    print(f'===== card[{idx}] =====')
    print((html or 'None')[:2500])
    print()
ws.close()
