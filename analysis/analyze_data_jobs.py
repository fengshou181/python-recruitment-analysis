#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
招聘数据 —— 数据分析岗市场分析报告生成器（可复用）

用途
----
对 spiderdatabase.data_data 做多维度统计分析，自动生成 Markdown 报告。
每次增量采集并清洗后，重跑本脚本即可刷新全部数据与结论。

用法
----
    python analysis/analyze_data_jobs.py                 # 生成报告到 analysis/ 目录
    python analysis/analyze_data_jobs.py --out 报告.md  # 指定输出文件名
    python analysis/analyze_data_jobs.py --no-filter     # 不做岗位名过滤（含噪声）

口径说明
--------
BOSS 直聘搜索为模糊匹配，搜索"数据分析"会返回大量 JD 中提及该词的无关岗位
（会计、质量工程师、HRBP 等）。默认启用岗位名白名单过滤，仅保留真·数据类岗位，
以保证统计口径干净。加 --no-filter 可查看含噪声的原始口径。
"""

import argparse
import datetime
import os
import statistics
import sys
from collections import defaultdict

import pymysql

DB = dict(host='127.0.0.1', port=3306, user='root', password='123456',
          database='spiderdatabase', charset='utf8')

# 数据类岗位名白名单（LIKE 条件）
DATA_NAME_PATTERN = (
    "name LIKE '%数据%' OR name LIKE '%分析师%' OR name LIKE '%算法%' "
    "OR name LIKE '%BI%' OR name LIKE '%bi%' OR name LIKE '%数仓%' "
    "OR name LIKE '%ETL%' OR name LIKE '%统计%' OR name LIKE '%挖掘%'"
)

EXP_ORDER = ['在校/应届', '1年以内', '经验不限', '1-3年', '3-5年', '5-10年', '10年以上']
EXP_CHAIN = ['1-3年', '3-5年', '5-10年', '10年以上']
EDU_ORDER = ['大专', '本科', '硕士']


class Analyzer:
    def __init__(self, use_filter=True):
        self.conn = pymysql.connect(**DB)
        self.cur = self.conn.cursor()
        self.where = f"WHERE ({DATA_NAME_PATTERN})" if use_filter else ""
        self.use_filter = use_filter
        self.scope = "仅数据类岗位（已过滤噪声）" if use_filter else "全部原始记录（含噪声）"

    def q(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def one(self, sql):
        rows = self.q(sql)
        return rows[0] if rows else (0,)

    def count(self):
        return self.one(f"SELECT COUNT(*) FROM data_data {self.where}")[0]

    def city_count(self):
        return self.one(f"SELECT COUNT(DISTINCT city) FROM data_data {self.where}")[0]

    def avg(self):
        return int(self.one(f"SELECT ROUND(AVG(avg_salary)) FROM data_data {self.where}")[0] or 0)

    def median(self):
        vals = [float(r[0] or 0) for r in self.q(f"SELECT avg_salary FROM data_data {self.where}")]
        return int(statistics.median(vals)) if vals else 0

    # ---------- 分组统计（均值受极值影响，同时给出中位数） ----------
    def _group_rows(self, col):
        d = defaultdict(list)
        for k, v in self.q(f"SELECT {col}, avg_salary FROM data_data {self.where}"):
            if k:
                d[k].append(float(v or 0))
        return d

    @staticmethod
    def _summarize(d, order=None, min_n=1):
        """返回 [(键, 条数, 均值, 中位数), ...]"""
        if order:
            items = [(k, d[k]) for k in order if k in d and len(d[k]) >= min_n]
        else:
            items = sorted(((k, v) for k, v in d.items() if len(v) >= min_n),
                           key=lambda kv: -statistics.median(kv[1]))
        return [(k, len(v), int(statistics.mean(v)), int(statistics.median(v)))
                for k, v in items]

    def by_experience(self):
        return self._summarize(self._group_rows('experience'), order=EXP_ORDER)

    def by_education(self):
        return self._summarize(self._group_rows('education'), order=EDU_ORDER)

    # ---------- 各维度 ----------
    def salary_buckets(self):
        return self.q(f"""
            SELECT CASE
                WHEN avg_salary < 6000  THEN '0-6K'
                WHEN avg_salary < 10000 THEN '6-10K'
                WHEN avg_salary < 15000 THEN '10-15K'
                WHEN avg_salary < 20000 THEN '15-20K'
                WHEN avg_salary < 30000 THEN '20-30K'
                ELSE '30K+' END AS bucket,
                COUNT(*) n
            FROM data_data {self.where}
            GROUP BY bucket ORDER BY MIN(avg_salary)""")

    def edu_exp_matrix(self):
        return self.q(f"""
            SELECT education, experience, COUNT(*) n, ROUND(AVG(avg_salary)) s
            FROM data_data
            {self.where + ' AND' if self.where else 'WHERE'}
                education IN ('大专','本科','硕士')
                AND experience IN ('1-3年','3-5年','5-10年','10年以上')
            GROUP BY education, experience HAVING n >= 20
            ORDER BY education, MIN(avg_salary)""")

    def city_rank(self, min_n=40, limit=15):
        """按中位数降序返回 [(城市, 条数, 均值, 中位数), ...]"""
        return self._summarize(self._group_rows('city'), min_n=min_n)[:limit]

    def high_salary(self, threshold=25000):
        n = self.one(f"SELECT COUNT(*) FROM data_data {self.where + ' AND' if self.where else 'WHERE'} avg_salary >= {threshold}")[0]
        exp = self.q(f"""
            SELECT experience, COUNT(*) n FROM data_data
            {self.where + ' AND' if self.where else 'WHERE'} avg_salary >= {threshold}
            GROUP BY experience ORDER BY n DESC LIMIT 4""")
        city = self.q(f"""
            SELECT city, COUNT(*) n FROM data_data
            {self.where + ' AND' if self.where else 'WHERE'} avg_salary >= {threshold}
            GROUP BY city ORDER BY n DESC LIMIT 5""")
        title = self.q(f"""
            SELECT name, COUNT(*) n FROM data_data
            {self.where + ' AND' if self.where else 'WHERE'} avg_salary >= {threshold}
            GROUP BY name ORDER BY n DESC LIMIT 6""")
        return n, exp, city, title

    def title_rank(self, limit=15):
        """按出现次数降序返回 [(职位, 条数, 均值, 中位数), ...]"""
        d = self._group_rows('name')
        items = sorted(d.items(), key=lambda kv: -len(kv[1]))[:limit]
        return [(k, len(v), int(statistics.mean(v)), int(statistics.median(v)))
                for k, v in items]

    def noise_stats(self):
        """噪声占比（用于数据质量章节）"""
        total = self.one("SELECT COUNT(*) FROM data_data")[0]
        clean = self.one(f"SELECT COUNT(*) FROM data_data WHERE ({DATA_NAME_PATTERN})")[0]
        top = self.q(f"""
            SELECT name, COUNT(*) n FROM data_data
            WHERE NOT ({DATA_NAME_PATTERN})
            GROUP BY name ORDER BY n DESC LIMIT 10""")
        clean_avg = int(self.one(f"SELECT ROUND(AVG(avg_salary)) FROM data_data WHERE ({DATA_NAME_PATTERN})")[0] or 0)
        noise_avg = int(self.one(f"SELECT ROUND(AVG(avg_salary)) FROM data_data WHERE NOT ({DATA_NAME_PATTERN})")[0] or 0)
        return total, clean, top, clean_avg, noise_avg

    def field_coverage(self):
        total = self.one("SELECT COUNT(*) FROM data_data")[0]
        out = {}
        for col in ['scale', 'skill', 'welfare', 'label', 'education', 'experience']:
            n = self.one(f"SELECT COUNT(*) FROM data_data WHERE {col} IS NOT NULL AND {col} <> ''")[0]
            out[col] = (n, round(n * 100 / total) if total else 0)
        return total, out

    def close(self):
        self.conn.close()


# ---------- Markdown 渲染 ----------
def pct(a, b):
    return f"{(a - b) * 100 / b:+.0f}%" if b else "—"


def render(a: Analyzer, out_path: str):
    L = []
    w = L.append

    total_all, cov = a.field_coverage()
    total, clean, noise_top, clean_avg, noise_avg = a.noise_stats()

    w(f"# 数据分析岗市场分析报告")
    w("")
    w(f"> 生成时间：{datetime.datetime.now():%Y-%m-%d %H:%M}　|　"
      f"数据源：spiderdatabase.data_data　|　统计口径：{a.scope}")
    w("")
    w("## 摘要")
    w("")
    w(f"- 样本量：**{a.count():,}** 条　覆盖城市：**{a.city_count()}** 个")
    w(f"- 平均月薪：**¥{a.avg():,}**　|　中位月薪：**¥{a.median():,}**（均值易被头部极值拉高，中位数更接近真实水平）")
    w(f"- 数据质量：全库 {total_all:,} 条记录中，真·数据类岗位 {clean:,} 条（{clean*100//total_all}%），"
      f"噪声 {total_all-clean:,} 条（{(total_all-clean)*100//total_all}%）")
    w("")

    # 一、数据口径与质量
    w("## 一、数据口径与质量")
    w("")
    if total_all - clean > 0:
        w("BOSS 直聘搜索为**模糊匹配**：检索「数据分析」时，凡是 JD 中出现该词的岗位都会被召回，"
          "因此混入大量无关职位。下表为未过滤口径下噪声最大的岗位：")
        w("")
        w("| 噪声岗位 | 条数 |")
        w("|---|---|")
        for name, n in noise_top:
            w(f"| {name} | {n} |")
        w("")
        w(f"两类岗位薪资对比：真·数据岗均薪 **¥{clean_avg:,}**，噪声岗均薪 **¥{noise_avg:,}**。"
          "噪声中的高管岗（财务总监、CIO）会把「行业最高薪资」严重拉高，**必须过滤后再做统计**。")
    else:
        w("BOSS 直聘搜索为**模糊匹配**：检索「数据分析」时，凡是 JD 中出现该词的岗位都会被召回。"
          "库内此类噪声（会计、质量工程师、财务总监等）已在数据清洗阶段整体剔除，"
          f"当前 {total_all:,} 条样本 100% 为真·数据类岗位。")
    w("")
    w("### 字段填充率（决定哪些维度可信）")
    w("")
    w("| 字段 | 填充 | 占比 | 可用性 |")
    w("|---|---|---|---|")
    for col, (n, p) in cov.items():
        usable = "可直接统计" if p >= 90 else ("仅作参考" if p >= 30 else "样本过少，不建议单独成图")
        w(f"| {col} | {n:,} | {p}% | {usable} |")
    w("")
    w(f"> 注：`skill`/`welfare`/`label` 填充率低，是因为新版列表页不再展示这些字段，"
      "仅旧数据（2023 年批次）带有。基于 skill 的雷达图/词云应以旧数据为准。")
    w("")

    # 二、薪资分布
    w("## 二、薪资整体分布")
    w("")
    w("| 薪资区间 | 条数 | 占比 |")
    w("|---|---|---|")
    n_total = a.count()
    for bucket, n in a.salary_buckets():
        w(f"| {bucket} | {n} | {n*100//n_total}% |")
    w("")

    # 三、经验
    exp_rows = a.by_experience()
    w("## 三、经验 = 最强薪资杠杆")
    w("")
    w("| 经验要求 | 条数 | 平均月薪 | 中位月薪 | 相邻档涨幅（按中位数） |")
    w("|---|---|---|---|---|")
    prev = None
    for e, n, s, m in exp_rows:
        # 只有 1-3年→3-5年→5-10年→10年以上 是可比的递增序列，其余档位不给涨幅
        if e in EXP_CHAIN:
            delta = pct(m, prev) if prev else "—"
            prev = m
        else:
            delta = "—"
            prev = None
        w(f"| {e} | {n} | ¥{s:,} | ¥{m:,} | {delta} |")
    w("")
    exp_map = {e: (n, s, m) for e, n, s, m in exp_rows}
    if '1-3年' in exp_map and '5-10年' in exp_map:
        m1, m2 = exp_map['1-3年'][2], exp_map['5-10年'][2]
        w(f"以样本充足的 **1-3年 → 5-10年** 为基准，中位月薪由 ¥{m1:,} 升至 ¥{m2:,}，"
          f"**增长 {m2/max(m1,1):.1f} 倍**，是全表最陡的一级台阶。")
        w("")
    small = exp_map.get('在校/应届') or exp_map.get('10年以上')
    if small:
        notes = []
        if '在校/应届' in exp_map:
            n, s, m = exp_map['在校/应届']
            notes.append(f"在校/应届 {n} 条，均值 ¥{s:,} 明显高于中位 ¥{m:,}")
        if '10年以上' in exp_map:
            n, s, m = exp_map['10年以上']
            notes.append(f"10年以上 {n} 条，均值 ¥{s:,} 明显高于中位 ¥{m:,}")
        w(f"> 口径提示：{'；'.join(notes)}。均为小样本被头部极值（校招 3-4 万、高管 40 万）拉高所致，"
          "**跨档比较请以中位数与条数为准，不要直接看均值**。")
        w("")

    # 四、学历
    edu_rows = a.by_education()
    w("## 四、学历阶梯（大专→本科是最大一道坎）")
    w("")
    w("| 学历 | 条数 | 平均月薪 | 中位月薪 | 相对大专（按中位数） |")
    w("|---|---|---|---|---|")
    base = edu_rows[0][3] if edu_rows else 1
    for e, n, s, m in edu_rows:
        w(f"| {e} | {n} | ¥{s:,} | ¥{m:,} | {pct(m, base)} |")
    w("")
    if len(edu_rows) >= 2:
        w(f"**大专 → 本科 中位薪资溢价 {pct(edu_rows[1][3], edu_rows[0][3])}**，是全表最显著的一道学历分水岭。")
        w("")

    # 五、交叉
    rows = a.edu_exp_matrix()
    if rows:
        w("## 五、学历 × 经验 交叉")
        w("")
        exps = [r[1] for r in rows]
        exps = sorted(set(exps), key=lambda x: EXP_ORDER.index(x) if x in EXP_ORDER else 99)
        matrix = {}
        for edu, exp, n, s in rows:
            matrix[(edu, exp)] = (n, s)
        w("| 经验 | 大专 | 本科 | 硕士 | 本科 vs 大专 |")
        w("|---|---|---|---|---|")
        gap_vals = []
        for exp in exps:
            cells = []
            a_val = b_val = None
            for edu in EDU_ORDER:
                if (edu, exp) in matrix:
                    n, s = matrix[(edu, exp)]
                    cells.append(f"¥{int(round(float(s))):,}<br><sub>{n}条</sub>")
                    if edu == '大专':
                        a_val = s
                    if edu == '本科':
                        b_val = s
                else:
                    cells.append("—")
            gap = pct(b_val, a_val) if (a_val and b_val) else "—"
            if a_val and b_val:
                gap_vals.append((b_val - a_val) * 100 / a_val)
            w(f"| {exp} | {cells[0]} | {cells[1]} | {cells[2]} | {gap} |")
        w("")
        if len(gap_vals) >= 2:
            lo, hi = min(gap_vals), max(gap_vals)
            if hi - lo <= 6:
                w(f"本科相对大专的溢价在各经验段基本稳定在 **{lo:+.0f}% ~ {hi:+.0f}%**，"
                  "说明学历更像一道**固定的入场门槛**，而不是随年限不断放大的乘数。")
            else:
                w(f"本科相对大专的溢价在 {lo:+.0f}% ~ {hi:+.0f}% 之间波动，"
                  "高经验段的学历门槛更硬（管理岗/架构岗普遍要求本科以上）。")
            w("")

    # 六、城市
    w("## 六、城市对比（样本 ≥ 40 条的城市）")
    w("")
    w("| 排名 | 城市 | 条数 | 平均月薪 | 中位月薪 |")
    w("|---|---|---|---|---|")
    cities = a.city_rank()
    for i, (city, n, s, m) in enumerate(cities, 1):
        w(f"| {i} | {city} | {n} | ¥{s:,} | ¥{m:,} |")
    w("")
    if len(cities) >= 5:
        top1, top4, top5 = cities[0], cities[3], cities[4]
        w(f"第一梯队为 **{top1[0]}（中位 ¥{top1[3]:,}）、{cities[1][0]}（中位 ¥{cities[1][3]:,}）、"
          f"{cities[2][0]}（中位 ¥{cities[2][3]:,}）、{top4[0]}（中位 ¥{top4[3]:,}）**，"
          f"与第二名梯队分界在 {top5[0]}（中位 ¥{top5[3]:,}），落差 {pct(top5[3], top4[3])}。")
        w("")

    # 七、高薪
    hs_n, hs_exp, hs_city, hs_title = a.high_salary()
    w("## 七、高薪岗位特征（月薪 ≥ 25K）")
    w("")
    w(f"高薪岗位 **{hs_n:,}** 条，占样本 **{hs_n*100//max(n_total,1)}%**。")
    w("")
    if hs_exp:
        w("**经验分布**：" + "　".join(f"{e} {n}条" for e, n in hs_exp))
        w("")
    if hs_city:
        w("**城市分布**：" + "　".join(f"{c} {n}条" for c, n in hs_city))
        w("")
    if hs_title:
        w("**典型高薪职位**：")
        w("")
        w("| 职位 | 条数 |")
        w("|---|---|")
        for name, n in hs_title:
            w(f"| {name} | {n} |")
        w("")

    # 八、岗位细分
    w("## 八、岗位细分方向 TOP15")
    w("")
    w("| 职位名称 | 条数 | 平均月薪 | 中位月薪 |")
    w("|---|---|---|---|")
    for name, n, s, m in a.title_rank():
        w(f"| {name} | {n} | ¥{s:,} | ¥{m:,} |")
    w("")

    # 附：复现
    w("---")
    w("")
    w("## 附：复现与更新方式")
    w("")
    w("```bash")
    w("# 重新生成报告（默认已过滤噪声岗位）")
    w("python analysis/analyze_data_jobs.py")
    w("")
    w("# 查看含噪声的原始口径")
    w("python analysis/analyze_data_jobs.py --no-filter --out 报告_原始口径.md")
    w("```")
    w("")
    w("前置条件：spiderdatabase 已导入数据，且 `data_data` 表存在。")
    w("每次增量采集后执行 `python clean_new.py` 清洗，再重跑本脚本即可刷新上述全部结论。")
    w("")

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(L))
    return out_path


def render_brief(a: Analyzer, out_path: str):
    """一页速览：给不想读长报告的人，只留决策需要的信息。"""
    L = []
    w = L.append
    n_total = a.count()
    exp = {e: (n, s, m) for e, n, s, m in a.by_experience()}
    edu = {e: (n, s, m) for e, n, s, m in a.by_education()}
    cities = a.city_rank()
    titles = a.title_rank(5)
    hs_n, hs_exp, hs_city, hs_title = a.high_salary()

    rows = a.edu_exp_matrix()
    mm = {(e, x): float(s) for e, x, n, s in rows}
    gaps = [(mm[('本科', x)] - mm[('大专', x)]) * 100 / mm[('大专', x)]
            for x in {x for _, x, _, _ in rows}
            if ('大专', x) in mm and ('本科', x) in mm]
    rest_med = int(statistics.median([c[3] for c in cities[4:]])) if len(cities) > 5 else 0
    step_gap = ((exp['3-5年'][2] - exp['1-3年'][2]) * 100 / max(exp['1-3年'][2], 1)
                if ('3-5年' in exp and '1-3年' in exp) else None)

    w(f"# 数据分析岗市场速览")
    w("")
    w(f"> {datetime.datetime.now():%Y-%m-%d %H:%M}　|　{a.scope}　|　"
      f"样本 {n_total:,} 条 / {a.city_count()} 城")
    w("")
    w("## 关键数字")
    w("")
    w(f"- 平均月薪 **¥{a.avg():,}**，中位月薪 **¥{a.median():,}**（中位数更接近典型水平）")
    w(f"- 月薪 ≥ 25K 的高薪岗 **{hs_n:,}** 条，占 **{hs_n*100//max(n_total,1)}%**")
    if '本科' in edu and '大专' in edu:
        w(f"- 本科 vs 大专 中位薪资溢价 **{pct(edu['本科'][2], edu['大专'][2])}**")
    w("")

    w("## 五条要点")
    w("")
    if '1-3年' in exp and '5-10年' in exp:
        line = (f"1. **经验是最大杠杆**：1-3年 → 5-10年，中位月薪 ¥{exp['1-3年'][2]:,} → ¥{exp['5-10年'][2]:,}"
                f"（{exp['5-10年'][2]/max(exp['1-3年'][2],1):.1f} 倍）")
        if '10年以上' in exp:
            line += (f"；10年以上均值虽高，但仅 {exp['10年以上'][0]} 条、中位 ¥{exp['10年以上'][2]:,}，"
                     "不宜直接与常规档位比较")
        w(line + "。")
    if '大专' in edu and '本科' in edu:
        line = (f"2. **学历是硬门槛**：大专中位 ¥{edu['大专'][2]:,} → 本科 ¥{edu['本科'][2]:,}"
                f"（{pct(edu['本科'][2], edu['大专'][2])}）")
        if gaps:
            line += f"；各经验段溢价稳定在 {min(gaps):+.0f}% ~ {max(gaps):+.0f}%，门槛是固定的，干久也抹不平"
        w(line + "。")
    if len(cities) >= 5:
        w(f"3. **城市分化明显**：第一梯队 {cities[0][0]} / {cities[1][0]} / {cities[2][0]} / {cities[3][0]}，"
          f"中位 ¥{cities[3][3]:,} ~ ¥{cities[0][3]:,}；其余城市中位约 ¥{rest_med:,}。")
    if titles:
        w("4. **高需求细分方向**：" + "、".join(f"{t[0]}({t[1]}条)" for t in titles[:4]) + "。")
    if hs_city:
        w("5. **高薪集中在头部城市**：25K+ 岗位主要分布在 " +
          "、".join(f"{c}{n}条" for c, n in hs_city[:3]) + "。")
    w("")

    w("## 给求职者的三条建议")
    w("")
    w("1. 目标是 25K+ 就优先看**头部四城**；同一岗位在其他城市的中位薪资普遍低一档。")
    if step_gap is not None:
        w(f"2. **1-3 年是涨幅最陡的窗口**（到 3-5年 中位就涨 {step_gap:+.0f}%），"
          "跳槽与技能升级尽量放在这一段。")
    if '硕士' in edu and '本科' in edu:
        w(f"3. **读研的薪资回报弱于同期的经验积累**：硕士中位 ¥{edu['硕士'][2]:,} 仅比本科高 "
          f"{pct(edu['硕士'][2], edu['本科'][2])}，而本科 1-3年 → 3-5年 的中位涨幅更大；"
          f"且硕士样本仅 {edu['硕士'][0]} 条，结论仅供参考。")
    w("")
    w(f"完整分析见同目录 `报告_{datetime.date.today():%Y%m%d}.md`；"
      "重跑脚本即可随新数据刷新。")
    w("")

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(L))
    return out_path


def main():
    ap = argparse.ArgumentParser(description='数据分析岗市场分析报告生成器')
    ap.add_argument('--out', default=None, help='输出文件名（默认 analysis/报告_YYYYMMDD.md）')
    ap.add_argument('--no-filter', action='store_true', help='不做岗位名过滤（含噪声）')
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    out = args.out or os.path.join(here, f"报告_{datetime.date.today():%Y%m%d}.md")
    if not os.path.isabs(out):
        out = os.path.join(os.getcwd(), out)
    brief = os.path.join(os.path.dirname(out), f"速览_{datetime.date.today():%Y%m%d}.md")

    a = Analyzer(use_filter=not args.no_filter)
    try:
        path = render(a, out)
        brief_path = render_brief(a, brief)
        scope, n, nc, av, md = a.scope, a.count(), a.city_count(), a.avg(), a.median()
    finally:
        a.close()

    print(f"报告已生成: {path}")
    print(f"速览已生成: {brief_path}")
    print(f"  口径: {scope}")
    print(f"  样本: {n} 条 / {nc} 城 / 均薪 ¥{av:,} / 中位 ¥{md:,}")


if __name__ == '__main__':
    main()
