# -*- coding: utf-8 -*-
"""
表内重复记录去除。

问题
----
爬虫按关键词翻页采集时，同一岗位会在不同页/不同检索里被重复写入，
导致 544 次重复的「C|华为|西安」这类记录，使 KPI 与图表严重失真。

规则
----
同一张表内 (name, company, city) 完全相同视为同一岗位，只保留 num 最小
（即最早入库）的一条。不同表之间不做互删——handled_data 是采集总表，
各岗位表是按技术栈拆分的独立视图。

用法
----
    python dedup_tables.py                    # 只统计
    python dedup_tables.py --apply            # 备份后去重
    python dedup_tables.py --tables java_data # 指定表
"""
import argparse
import datetime
import pymysql

DB = dict(host='127.0.0.1', port=3306, user='root', password='123456',
          database='spiderdatabase', charset='utf8')

TABLES = ['handled_data', 'data_data', 'java_data', 'python_data', 'c_data', 'c23_data',
          'u3dUe_data', 'php_data', 'web_data', 'Android_data', 'ios_data',
          'algorithm_data', 'test_data', 'oam_data']

KEY = "COALESCE(name,''), COALESCE(company,''), COALESCE(city,'')"


def one(cur, sql):
    cur.execute(sql)
    return cur.fetchone()[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--tables', default='')
    ap.add_argument('--no-backup', action='store_true')
    args = ap.parse_args()

    targets = [t.strip() for t in args.tables.split(',') if t.strip()] or TABLES

    conn = pymysql.connect(**DB)
    cur = conn.cursor()
    rows = []

    for t in targets:
        total = one(cur, f'SELECT COUNT(*) FROM `{t}`')
        uniq = one(cur, f'SELECT COUNT(*) FROM (SELECT 1 FROM `{t}` GROUP BY {KEY}) x')
        dup = total - uniq
        rows.append((t, total, uniq, dup))
        print(f'{t:<16} total={total:>7}  uniq={uniq:>7}  重复={dup:>7}')

        if args.apply and dup:
            if not args.no_backup:
                backup = f'{t}_backup_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                cur.execute(f'CREATE TABLE `{backup}` AS SELECT * FROM `{t}`')
                conn.commit()
                print(f'   备份 -> {backup}')
            cur.execute(f'''
                DELETE t1 FROM `{t}` t1
                INNER JOIN (
                    SELECT COALESCE(name,'') n, COALESCE(company,'') c,
                           COALESCE(city,'') ct, MIN(num) mn
                    FROM `{t}` GROUP BY n, c, ct HAVING COUNT(*) > 1
                ) k ON COALESCE(t1.name,'') = k.n
                   AND COALESCE(t1.company,'') = k.c
                   AND COALESCE(t1.city,'') = k.ct
                WHERE t1.num > k.mn
            ''')
            conn.commit()
            print(f'   删除 {cur.rowcount} 行，剩余 {one(cur, f"SELECT COUNT(*) FROM `{t}`")}')

    tt = sum(r[1] for r in rows)
    tu = sum(r[2] for r in rows)
    print(f'\n合计 {tt} -> {tu}，可去除 {tt - tu} 行 ({(tt - tu) / tt * 100:.1f}%)')
    if not args.apply:
        print('[dry-run] 未写库')
    conn.close()


if __name__ == '__main__':
    main()
