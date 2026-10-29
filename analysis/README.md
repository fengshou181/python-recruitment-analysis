# 分析文档目录（可复用）

本目录下的文档**全部由脚本自动生成**，不是手写的一次性结论。新数据入库后重跑脚本，所有数字与结论自动刷新。

## 文件清单

| 文件 | 性质 | 说明 |
|---|---|---|
| `analyze_data_jobs.py` | 脚本 | 唯一入口。连 MySQL 统计并生成下面两份文档 |
| `报告_YYYYMMDD.md` | 自动生成 | 完整分析（9 章：口径质量、薪资分布、经验、学历、交叉、城市、高薪、细分方向、复现） |
| `速览_YYYYMMDD.md` | 自动生成 | 一页速览，只留决策需要的关键数字、5 条要点、3 条建议 |

## 复用方式（三步）

```bash
# 1. 增量采集（可选，已有新数据则跳过）
python spider/cdp_reader.py --keyword 数据分析师 --pages 1 --cities 上海,北京,深圳

# 2. 清洗入库（写入 data_data 子表 + c_data 总表）
python clean_new.py

# 3. 重跑分析（生成当天日期的新报告）
python analysis/analyze_data_jobs.py
```

每次运行会按当天日期生成新文件，历史报告不会被覆盖，可对比前后变化。

可选参数：

```bash
python analysis/analyze_data_jobs.py --out 报告_对比.md   # 自定义输出名（速览同名替换）
python analysis/analyze_data_jobs.py --no-filter          # 不过滤噪声岗位，看原始口径
```

## 统计口径（重要）

1. **噪声过滤**：BOSS 搜索是模糊匹配，搜「数据分析」会召回 JD 里提到该词的会计、质量工程师、财务总监等岗位。默认按岗位名白名单过滤（`DATA_NAME_PATTERN`），只保留数据类岗位。全库 8,865 条 → 噪声清洗后 3,943 条 → 表内去重后 3,928 条。
2. **均值 + 中位数双口径**：均值会被头部极值（校招 3-4 万、高管 40 万）严重拉高，因此每张表都同时给出中位数。**跨档比较以中位数为准**，样本量 < 200 的档位额外标注。
3. **样本量门槛**：城市榜只统计 ≥ 40 条的城市；学历×经验交叉只统计 ≥ 20 条的组合。
4. **字段填充率**：`skill`/`welfare`/`label` 仅 9%~16% 填充（新版列表页不展示），基于这些字段的图表不可用于最新数据。

## 扩展新维度

在 `Analyzer` 里加一个方法即可，`render()` 中调用即可见：

```python
def by_company(self, limit=10):
    return self.q(f"""
        SELECT company, COUNT(*) n, ROUND(AVG(avg_salary)) s
        FROM data_data {self.where}
        GROUP BY company ORDER BY n DESC LIMIT {limit}""")
```

需要中位数口径时，用现成的 `_group_rows()` + `_summarize()`：

```python
def by_company(self):
    return self._summarize(self._group_rows('company'), min_n=10)[:10]
```

## 依赖

- Python 3.x，`pymysql`
- MySQL 8 本地库 `spiderdatabase`，表 `data_data`（字段：`name` `city` `experience` `education` `min_salary` `max_salary` `avg_salary` `scale` `company` 等）
