# -*- coding: utf-8 -*-
import pymysql

c = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                    database='spiderdatabase', charset='utf8')
cur = c.cursor(pymysql.cursors.DictCursor)

# 1) 删乱码薪资行（含 PUA 字符）
cur.execute('SELECT num, salary FROM row_data')
bad = [r['num'] for r in cur.fetchall()
       if any(0xE031 <= ord(ch) <= 0xE03A for ch in (r['salary'] or ''))]
if bad:
    cur.execute('DELETE FROM row_data WHERE num IN (%s)' % ','.join(map(str, bad)))
print('garbled deleted:', len(bad))

# 2) 删完全重复行（保留 num 最小）
cur.execute('''SELECT num, name, company, place, salary FROM row_data
               ORDER BY num''')
seen = {}
dups = []
for r in cur.fetchall():
    key = (r['name'], r['company'], r['place'], r['salary'])
    if key in seen:
        dups.append(r['num'])
    else:
        seen[key] = r['num']
if dups:
    for i in range(0, len(dups), 5000):
        cur.execute('DELETE FROM row_data WHERE num IN (%s)'
                    % ','.join(map(str, dups[i:i + 5000])))
print('dup deleted:', len(dups))

c.commit()
cur.execute('SELECT COUNT(*) c FROM row_data')
print('row_data:', cur.fetchone()['c'])
