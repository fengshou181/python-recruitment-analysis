# -*- coding: utf-8 -*-
"""
各岗位子表清洗：按岗位名白名单剔除与岗位无关的噪声记录。

背景
----
爬虫按关键词检索，BOSS 的模糊匹配会把仅在 JD 中提到该关键词的无关岗位
一并返回（如 C 表里混进测试、运维、iOS；iOS 表里混进 Android）。
这些行会让各岗位页的 KPI 与图表失真。

用法
----
    python clean_tables.py            # 只统计（dry-run，默认）
    python clean_tables.py --apply    # 备份后执行删除

每张表删除前都会备份为 <table>_backup_<YYYYMMDD_HHMM>，可回滚。
规则与 analysis 报告的岗位口径保持一致：岗位名必须体现该技术栈。
"""
import argparse
import datetime
import pymysql

DB = dict(host='127.0.0.1', port=3306, user='root', password='123456',
          database='spiderdatabase', charset='utf8')

# 表 -> 保留条件（岗位名白名单）
RULES = {
    'java_data':     "name LIKE '%java%'",
    'python_data':   "name LIKE '%python%' OR name LIKE '%爬虫%' OR name LIKE '%django%' OR name LIKE '%flask%'",
    'c_data':        "(name REGEXP '(^|[^a-zA-Z])c([^a-zA-Z]|$)' OR name LIKE '%c++%' "
                     "OR name LIKE '%c语言%' OR name LIKE '%c/c++%' "
                     "OR name LIKE '%嵌入式%' OR name LIKE '%单片机%')",
    'c23_data':      "name LIKE '%net%' OR name LIKE '%c#%' OR name LIKE '%csharp%'",
    'u3dUe_data':    "name LIKE '%u3d%' OR name LIKE '%unity%' OR name LIKE '%ue4%' "
                     "OR name LIKE '%ue5%' OR name LIKE '%unreal%' OR name LIKE '%虚幻%' "
                     "OR name LIKE '%vr%' OR name LIKE '%ar%'",
    'php_data':      "name LIKE '%php%'",
    'web_data':      "name LIKE '%web%' OR name LIKE '%前端%' OR name LIKE '%h5%' "
                     "OR name LIKE '%vue%' OR name LIKE '%react%' OR name LIKE '%html%'",
    'Android_data':  "name LIKE '%android%' OR name LIKE '%安卓%'",
    'ios_data':      "name LIKE '%ios%'",
    'algorithm_data': "name LIKE '%算法%' OR name LIKE '%机器学习%' OR name LIKE '%深度学习%' "
                      "OR name LIKE '%视觉%' OR name LIKE '%nlp%' OR name LIKE '%ai%' "
                      "OR name LIKE '%人工智能%'",
    'test_data':     "name LIKE '%测试%'",
    'oam_data':      "name LIKE '%运维%' OR name LIKE '%dba%' OR name LIKE '%sre%' "
                     "OR name LIKE '%系统管理员%'",
}


def one(cur, sql):
    cur.execute(sql)
    return cur.fetchone()[0]


def table_exists(cur, name):
    cur.execute('SELECT COUNT(*) FROM information_schema.tables '
                'WHERE table_schema = DATABASE() AND table_name = %s', (name,))
    return cur.fetchone()[0] > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='执行删除（默认仅统计）')
    ap.add_argument('--batch', type=int, default=5000, help='每批删除条数')
    ap.add_argument('--tables', default='', help='只处理指定表，逗号分隔')
    args = ap.parse_args()

    only = [t.strip() for t in args.tables.split(',') if t.strip()]
    targets = [t for t in RULES if not only or t in only]

    conn = pymysql.connect(**DB)
    cur = conn.cursor()
    summary = []

    for t in targets:
        cond = RULES[t]
        total = one(cur, f'SELECT COUNT(*) FROM `{t}`')
        keep = one(cur, f'SELECT COUNT(*) FROM `{t}` WHERE ({cond})')
        noise = total - keep
        print(f'\n=== {t}  total={total}  keep={keep}  noise={noise} ===')
        if noise:
            cur.execute(f'SELECT name, COUNT(*) n FROM `{t}` '
                        f'WHERE NOT ({cond}) GROUP BY name ORDER BY n DESC LIMIT 8')
            for name, n in cur.fetchall():
                print(f'   {n:>7}  {name}')
        summary.append((t, total, keep, noise))

        if args.apply and noise:
            backup = f'{t}_backup_' + datetime.datetime.now().strftime('%Y%m%d_%H%M')
            suffix = 0
            while table_exists(cur, backup):
                suffix += 1
                backup = f'{t}_backup_' + datetime.datetime.now().strftime('%Y%m%d_%H%M') + f'_{suffix}'
            cur.execute(f'CREATE TABLE `{backup}` AS SELECT * FROM `{t}`')
            conn.commit()
            deleted = 0
            while True:
                cur.execute(f'DELETE FROM `{t}` WHERE NOT ({cond}) LIMIT {args.batch}')
                n = cur.rowcount
                conn.commit()
                if n <= 0:
                    break
                deleted += n
            left = one(cur, f'SELECT COUNT(*) FROM `{t}`')
            print(f'   -> 已删除 {deleted} 条，剩余 {left} 条，备份 {backup}')

    print('\n===== 汇总 =====')
    tt = sum(s[1] for s in summary)
    tk = sum(s[2] for s in summary)
    for t, total, keep, noise in summary:
        print(f'  {t:<15} {total:>8} -> {keep:>8}  (-{noise})')
    print(f'  {"合计":<15} {tt:>8} -> {tk:>8}  (-{tt - tk})')

    if not args.apply:
        print('\n[dry-run] 未写库。确认后加 --apply 执行。')
    conn.close()


if __name__ == '__main__':
    main()
