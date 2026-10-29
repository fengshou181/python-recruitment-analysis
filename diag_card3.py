# -*- coding: utf-8 -*-
"""探针4：枚举页面所有含 card 的类名及数量，并打印主列表第一张卡"""
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


classes = ev("""(function(){
  var cnt = {};
  document.querySelectorAll('[class]').forEach(function(e){
    (e.getAttribute('class')||'').split(/\\s+/).forEach(function(c){
      if(c && c.indexOf('card')>=0){ cnt[c]=(cnt[c]||0)+1; }
    });
  });
  return JSON.stringify(cnt);
})()""")
print('card 类统计:', classes)

# 左侧主列表通常是 .search-job-result 或 job-list-container；直接找包含招聘卡片的 ul
main = ev("""(function(){
  var uls = document.querySelectorAll('ul');
  for(var i=0;i<uls.length;i++){
    var lis = uls[i].querySelectorAll(':scope > li');
    if(lis.length>=5 && uls[i].innerText.indexOf('K')>=0 && (uls[i].className||'').indexOf('rec')<0){
      return 'UL_CLASS=' + uls[i].className + ' LI_COUNT=' + lis.length + '\\nLI_CLASS=' + (lis[0].className||'(empty)') + '\\n---\\n' + lis[0].outerHTML.slice(0,3000);
    }
  }
  return 'not found';
})()""")
print(main)
ws.close()
