# -*- coding: utf-8 -*-
"""
data_data 表清洗落库：删除「非数据类岗位」噪声，让页面口径与
analysis/analyze_data_jobs.py 生成的报告保持一致。

背景
----
BOSS 直聘搜索"数据分析"为模糊匹配，返回大量仅在 JD 里提到该词的无关岗位
（会计、质量工程师、HRBP、销售等）。这些行采集时统一落到 data_data，
导致 data.html 显示 8865 条，而报告口径只有 3943 条。

用法
----
    python clean_data_table.py            # 只统计，不写库（dry-run，默认）
    python clean_data_table.py --apply    # 备份后执行删除

删除前会将整表备份为 data_data_backup_<YYYYMMDD>，可随时回滚。
"""
import argparse
import datetime
import statistics
import sys

import pymysql

DB = dict(host='127.0.0.1', port=3306, user='root', password='123456',
          database='spiderdatabase', charset='utf8')

# 与 analysis/analyze_data_jobs.py 中的 DATA_NAME_PATTERN 完全一致
DATA_NAME_PATTERN = (
    "name LIKE '%数据%' OR name LIKE '%分析师%' OR name LIKE '%算法%' "
    "OR name LIKE '%BI%' OR name LIKE '%bi%' OR name LIKE '%数仓%' "
    "OR name LIKE '%ETL%' OR name LIKE '%统计%' OR name LIKE '%挖掘%'"
)


def one(cur, sql):
    cur.execute(sql)
    return cur.fetchone()[0]


def snapshot(cur):
    """返回当前 data_data 的口径快照"""
    total = one(cur, 'SELECT COUNT(*) FROM data_data')
    clean = one(cur, f'SELECT COUNT(*) FROM data_data WHERE ({DATA_NAME_PATTERN})')
    cur.execute(f'SELECT ROUND(AVG(avg_salary)) FROM data_data WHERE ({DATA_NAME_PATTERN})')
    avg = cur.fetchone()[0] or 0
    cur.execute(f'SELECT avg_salary FROM data_data WHERE ({DATA_NAME_PATTERN})')
    vals = [float(r[0] or 0) for r in cur.fetchall()]
    med = statistics.median(vals) if vals else 0
    cities = one(cur, f'SELECT COUNT(DISTINCT city) FROM data_data WHERE ({DATA_NAME_PATTERN})')
    return dict(total=total, clean=clean, noise=total - clean,
                avg=int(avg), median=int(med), cities=cities)


def top_noise(cur, limit=15):
    cur.execute(
        'SELECT name, COUNT(*) n FROM data_data '
        f'WHERE NOT ({DATA_NAME_PATTERN}) GROUP BY name ORDER BY n DESC LIMIT {limit}')
    return cur.fetchall()


def table_exists(cur, name):
    cur.execute('SELECT COUNT(*) FROM information_schema.tables '
                'WHERE table_schema = DATABASE() AND table_name = %s', (name,))
    return cur.fetchone()[0] > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='执行删除（默认仅统计）')
    ap.add_argument('--batch', type=int, default=1000, help='每批删除条数')
    args = ap.parse_args()

    conn = pymysql.connect(**DB)
    cur = conn.cursor()

    before = snapshot(cur)
    print('=== 清洗前 ===')
    print(f"  总行数      : {before['total']}")
    print(f"  数据类岗位  : {before['clean']}")
    print(f"  噪声岗位    : {before['noise']}")
    print(f"  均薪/中位   : ¥{before['avg']} / ¥{before['median']}")
    print(f"  覆盖城市    : {before['cities']}")

    print('\n=== 噪声 TOP 15（将被删除）===')
    for name, n in top_noise(cur):
        print(f'  {n:>5}  {name}')

    if not args.apply:
        print('\n[dry-run] 未写库。确认无误后加 --apply 执行。')
        conn.close()
        return

    if before['noise'] == 0:
        print('\n表中已无噪声，无需清洗。')
        conn.close()
        return

    backup = 'data_data_backup_' + datetime.datetime.now().strftime('%Y%m%d_%H%M')
    if table_exists(cur, backup):
        backup += '_b'
    cur.execute(f'CREATE TABLE `{backup}` AS SELECT * FROM data_data')
    conn.commit()
    print(f'\n已备份到 {backup}（{one(cur, f"SELECT COUNT(*) FROM `{backup}`")} 行）')

    deleted = 0
    while True:
        cur.execute(f'DELETE FROM data_data WHERE NOT ({DATA_NAME_PATTERN}) LIMIT {args.batch}')
        affected = cur.rowcount
        conn.commit()
        if affected <= 0:
            break
        deleted += affected
        print(f'  已删除 {deleted} 条...', end='\r')
    print(f'\n删除完成，共 {deleted} 条')

    after = snapshot(cur)
    print('\n=== 清洗后 ===')
    print(f"  总行数      : {after['total']}")
    print(f"  均薪/中位   : ¥{after['avg']} / ¥{after['median']}")
    print(f"  覆盖城市    : {after['cities']}")

    ok = after['noise'] == 0 and after['total'] == before['clean']
    print('\n校验:', '通过' if ok else '异常，请检查')
    if not ok:
        sys.exit(1)
    conn.close()


if __name__ == '__main__':
    main()
