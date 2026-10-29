# -*- coding: utf-8 -*-
"""
定向清洗：只处理本次新采集的 row_data（num > NEW_ROW_BOUNDARY），
写入 handled_data 和对应岗位子表。跳过解析不了的记录（实习日薪等）。
采集器入库时 type 已小写化。
"""
import re
import pymysql

NEW_ROW_BOUNDARY = 132176  # 本次采集前 row_data 的最大 num

TYPE_TABLE = {
    'java': 'java_data',
    'python': 'python_data',
    'c++': 'c_data',
    'c': 'c_data',
    'c#': 'c23_data',
    '.net': 'c23_data',
    'web前端': 'web_data',
    'u3d': 'u3due_data',
    'ue': 'u3due_data',
    '算法': 'algorithm_data',
    '算法工程师': 'algorithm_data',
    '运维': 'oam_data',
    '测试': 'test_data',
    'ios': 'ios_data',
    'php': 'php_data',
    'android': 'android_data',
    '安卓': 'android_data',
    '数据分析': 'data_data',
    '数据开发': 'data_data',
    '数据挖掘': 'data_data',
    '数据仓库': 'data_data',
}


def parse_salary(s):
    """返回 (min,max,avg) 或 None（无法解析则跳过该行）"""
    if not s:
        return None
    if '元/天' in s or '元/月' in s:
        return None  # 实习/日薪不纳入月薪统计
    m = re.match(r'^(\d+)-(\d+)K(?:·(\d+)薪)?$', s)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        k = int(m.group(3)) / 12 if m.group(3) else 1.0
        lo, hi = int(a * k * 1000), int(b * k * 1000)
        return lo, hi, (lo + hi) / 2.0
    m = re.match(r'^(\d+)K以上$', s)
    if m:
        v = int(m.group(1)) * 1000
        return v, v, float(v)
    return None


def parse_place(place):
    if not place:
        return '其他', '其他', '其他'
    parts = place.split('·')
    if len(parts) == 1:
        return parts[0], '其他', '其他'
    if len(parts) == 2:
        return parts[0], parts[1], '其他'
    return parts[0], parts[1], parts[2]


def main():
    c = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                        database='spiderdatabase', charset='utf8')
    cur = c.cursor(pymysql.cursors.DictCursor)

    cur.execute('SELECT * FROM row_data WHERE num > %s', (NEW_ROW_BOUNDARY,))
    rows = cur.fetchall()
    print(f'待清洗新数据: {len(rows)} 条')

    # 预加载 handled_data 与各子表已有键用于去重
    def load_keys(table):
        cur.execute(f'SELECT name,company,city,min_salary,max_salary FROM {table}')
        return {(r['name'], r['company'], r['city'], r['min_salary'], r['max_salary'])
                for r in cur.fetchall()}

    handled_keys = load_keys('handled_data')
    sub_keys = {}
    stats = {'ok': 0, 'skip_salary': 0, 'skip_type': 0, 'dup': 0}

    for r in rows:
        salary = parse_salary((r['salary'] or '').strip())
        if not salary:
            stats['skip_salary'] += 1
            continue
        t = (r['type'] or '').strip().lower()
        sub_table = TYPE_TABLE.get(t)
        if not sub_table:
            stats['skip_type'] += 1
            continue
        if sub_table not in sub_keys:
            sub_keys[sub_table] = load_keys(sub_table)

        city, area, detail = parse_place((r['place'] or '').strip())
        scale = (r['scale'] or '').strip() or '未知'
        lo, hi, avg = salary
        vals = (r['name'], city, area, detail, r['company'], scale, lo, hi, avg,
                r['education'] or '', r['experience'] or '',
                r['label'] or '', r['skill'] or '', r['welfare'] or '')

        key = (r['name'], r['company'], city, lo, hi)
        if key in handled_keys or key in sub_keys[sub_table]:
            stats['dup'] += 1
            continue

        sql = ('''insert into {} (name, city, area, detail, company, scale,
                  min_salary, max_salary, avg_salary, education, experience,
                  label, skill, welfare)
                  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''')
        try:
            cur.execute(sql.format('handled_data'), vals)
            cur.execute(sql.format(sub_table), vals)
            # 岗位子表之外同步写总表，保证薪资地图等全局视图能看到新数据
            if sub_table != 'c_data':
                cur.execute(sql.format('c_data'), vals)
            handled_keys.add(key)
            sub_keys[sub_table].add(key)
            stats['ok'] += 1
        except Exception as e:
            c.rollback()
            print(f'插入失败: {e} {vals[:5]}')
    c.commit()
    print('清洗完成:', stats)

    for t in sorted(set(TYPE_TABLE.values())):
        cur.execute(f'SELECT COUNT(*) c FROM {t}')
        print(f'  {t}: {cur.fetchone()["c"]} 条')


if __name__ == '__main__':
    main()
