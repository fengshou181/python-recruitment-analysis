# -*- coding: utf-8 -*-
"""
薪资 / 经验字段的数据质量修复。

两类问题
--------
1. experience 字段被采集逻辑污染：
   - 实习岗位把「4天/周3个月」这类实习周期写进了经验字段
   - 部分记录把学历拼在经验尾部，如「经验不限中专/」
   统一归一到标准经验枚举，避免图表按脏值分档。
2. 薪资离群：个别远程/计件岗位的单月薪资达到 40 万~81 万，
   会把薪资图表的纵轴拉爆，也让均值失真。超过上限的记录薪资置 NULL，
   岗位本身保留（不参与薪资统计，但仍计入数量）。

用法
----
    python clean_salary_experience.py                 # 仅统计（默认表 c_data）
    python clean_salary_experience.py --tables all    # 统计全部岗位表
    python clean_salary_experience.py --apply         # 备份后执行
"""
import argparse
import datetime
import re
import pymysql

DB = dict(host='127.0.0.1', port=3306, user='root', password='123456',
          database='spiderdatabase', charset='utf8')

JOBS = ['handled_data', 'data_data', 'java_data', 'python_data', 'c_data', 'c23_data', 'u3dUe_data',
        'php_data', 'web_data', 'Android_data', 'ios_data', 'algorithm_data',
        'test_data', 'oam_data']

SALARY_CAP = 100000          # 月薪上限，超过视为异常
INTERN = re.compile(r'^\d+天/周\d+个月$')
EDU_TAIL = re.compile(r'^(经验不限|在校/应届|应届生|1年以内|1-3年|3-5年|5-10年|10年以上)'
                      r'(中专|大专|本科|硕士|博士)/?$')


def table_exists(cur, name):
    cur.execute('SELECT COUNT(*) FROM information_schema.tables '
                'WHERE table_schema = DATABASE() AND table_name = %s', (name,))
    return cur.fetchone()[0] > 0


def fix_experience(cur, table, apply):
    """返回 (待修正行数, {原值: 新值})"""
    cur.execute(f'SELECT DISTINCT experience FROM `{table}`')
    mapping = {}
    for (v,) in cur.fetchall():
        if not v:
            continue
        if INTERN.match(v):
            mapping[v] = '在校/应届'
        else:
            m = EDU_TAIL.match(v)
            if m:
                mapping[v] = m.group(1)

    if not mapping:
        return 0, {}

    cur.execute(f'SELECT COUNT(*) FROM `{table}` WHERE experience IN ({",".join(["%s"] * len(mapping))})',
                tuple(mapping))
    affected = cur.fetchone()[0]

    if apply:
        for old, new in mapping.items():
            cur.execute(f'UPDATE `{table}` SET experience = %s WHERE experience = %s', (new, old))
        cur.connection.commit()

    return affected, mapping


def fix_salary(cur, table, apply):
    """返回 (待处理行数, 其中原最高薪资)"""
    cur.execute(f'SELECT COUNT(*) FROM `{table}` '
                f'WHERE max_salary > %s OR avg_salary > %s OR min_salary > %s',
                (SALARY_CAP, SALARY_CAP, SALARY_CAP))
    n = cur.fetchone()[0]
    if n and apply:
        cur.execute(f'UPDATE `{table}` SET min_salary = NULL, avg_salary = NULL, max_salary = NULL '
                    f'WHERE max_salary > %s OR avg_salary > %s OR min_salary > %s',
                    (SALARY_CAP, SALARY_CAP, SALARY_CAP))
        cur.connection.commit()
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--tables', default='c_data', help='表名逗号分隔，或 all')
    ap.add_argument('--no-backup', action='store_true', help='不建临时备份表')
    args = ap.parse_args()

    targets = JOBS if args.tables == 'all' else [t.strip() for t in args.tables.split(',') if t.strip()]

    conn = pymysql.connect(**DB)
    cur = conn.cursor()

    for t in targets:
        if not table_exists(cur, t):
            print(f'{t}: 表不存在，跳过')
            continue
        cur.execute(f'SELECT COUNT(*) FROM `{t}`')
        total = cur.fetchone()[0]
        print(f'\n=== {t}  total={total} ===')

        if args.apply and not args.no_backup:
            backup = f'{t}_backup_' + datetime.datetime.now().strftime('%Y%m%d_%H%M')
            cur.execute(f'CREATE TABLE `{backup}` AS SELECT * FROM `{t}`')
            conn.commit()
            print(f'  备份 -> {backup}')

        aff, mp = fix_experience(cur, t, args.apply)
        print(f'  experience 归一: {aff} 行, {len(mp)} 种脏值')
        for old, new in list(mp.items())[:12]:
            print(f'     {old:<18} -> {new}')

        sal = fix_salary(cur, t, args.apply)
        print(f'  薪资离群(>{SALARY_CAP}): {sal} 行 -> 薪资置 NULL')

    if not args.apply:
        print('\n[dry-run] 未写库。确认后加 --apply。')
    conn.close()


if __name__ == '__main__':
    main()
