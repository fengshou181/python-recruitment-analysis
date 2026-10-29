# Python 招聘数据分析平台

基于 BOSS 直聘公开招聘页面样本的岗位数据分析与可视化平台。后端使用 Flask + MySQL，前端使用 Bootstrap 4（SB Admin 2）与 ECharts 5，提供岗位薪资分析、地区薪资热力图、薪资预测、岗位匹配，以及脚本自动生成的分析报告。

数据为本地采集的静态样本，非实时接口，适合作为就业市场研究与数据可视化工程实践。

## 功能

- **首页总览**：样本量、平均薪资、薪资区间，以及学历/经验维度的薪资分布
- **分技术栈分析**：Java、Python、C/C++、C#、前端、测试、算法、Android、iOS、PHP、U3D/UE、运维、数据分析等岗位页，覆盖薪资分布、学历要求、经验要求、公司规模、行业、技能词云
- **薪资热力图**：全国城市 × 薪资水平的交互式地图、条件筛选与城市薪资榜单
- **薪资预测**：基于历史样本训练的回归模型，按城市/学历/经验/规模输出期望薪资
- **岗位匹配**：按技能、城市、薪资区间等条件匹配岗位并给出匹配度
- **分析报告**：`analysis/` 下的 Markdown 专题报告由脚本自动生成，均值与中位数双口径，可按新数据一键重跑

## 界面风格

全站采用终端极客风：深色底、直角卡片、无阴影无渐变、等宽字体，仅保留单一琥珀色作为强调；ECharts 统一注入灰阶主题，避免多色图表割裂视觉。

## 技术栈

| 层 | 选型 |
|---|---|
| Web 后端 | Flask 2.0、Jinja2、Werkzeug |
| 数据库 | MySQL 8、PyMySQL |
| 数据处理 | pandas、NumPy |
| 机器学习 | scikit-learn（薪资回归） |
| 前端 | Bootstrap 4 / SB Admin 2、jQuery、ECharts 5 |
| 数据采集 | 裸 CDP（Chrome DevTools Protocol）只读读取，非 Selenium 注入 |

## 目录结构

```
python-recruitment-analysis-master/
├── app.py                       # Flask 入口与全部路由（端口 8080）
├── mysql.py                     # 数据库访问层（连接配置在文件顶部）
├── match.py                     # 岗位匹配算法
├── salary_model.py              # 薪资预测模型封装
├── train_salary_model.py        # 模型训练脚本
├── clean_tables.py              # 按岗位名白名单清洗各表噪声岗位
├── clean_salary_experience.py   # 经验字段归一化 + 离群薪资置 NULL
├── dedup_tables.py              # 表内重复记录去除
├── runtest.py                   # 路由自检脚本
├── analysis/                    # 数据分析：脚本 + 自动生成的报告
│   ├── analyze_data_jobs.py     # 数据分析岗专题（均值/中位数双口径）
│   ├── 报告_YYYYMMDD.md         # 完整报告
│   └── 速览_YYYYMMDD.md         # 一页速览
├── spider/                      # 采集层
│   ├── cdp_reader.py            # 裸 CDP 只读采集器（当前方案）
│   ├── bosszp_spider*.py        # 历史采集脚本
│   └── run_combos.py            # 多城市多关键词矩阵调度
├── templates/                   # Jinja2 模板（20+ 页面）
├── static/
│   ├── css/terminal.css         # 全站终端极客风皮肤
│   └── js/term-echarts.js       # ECharts 灰阶主题注入
├── sql/                         # 建库建表语句
└── model/                       # 训练产物（薪资模型、编码器）
```

## 快速开始

### 1. 环境

Python 3.8+、MySQL 8.0+、Chrome（仅采集时需要）。

```bash
pip install -r requirements.txt
```

### 2. 数据库

```sql
CREATE DATABASE spiderdatabase DEFAULT CHARSET utf8mb4;
```

用 `sql/` 下的建表语句初始化。数据库连接通过环境变量配置，代码里的缺省值仅用于本地开发：

```bash
set DB_HOST=127.0.0.1
set DB_PORT=3306
set DB_USER=root
set DB_PASSWORD=你的密码
set DB_NAME=spiderdatabase
```

### 3. 启动

```bash
python app.py
```

访问 <http://127.0.0.1:8080/>。各页面路由均为 `*.html` 形式，例如 `/data.html`、`/salary-map.html`。

> 注意：`debug=False` 时 Jinja 模板与 `@cache.cached` 视图缓存都在进程内，修改模板或数据后需要重启进程才会生效。

## 数据说明

样本采集自 BOSS 直聘公开列表页，字段包括岗位名、公司、城市、薪资区间、学历、经验、公司规模、行业、技能标签等。

清洗后的分布（本仓库当前快照）：

| 范围 | 记录数 |
|---|---:|
| 采集总表 + 13 张岗位表（去重后） | 122,071 |
| 数据分析岗专题（白名单过滤后） | 3,928 |

清洗链路：

1. `clean_tables.py`：按岗位名白名单剔除模糊匹配引入的噪声岗位（如搜「数据分析」召回会计、质量工程师）
2. `clean_salary_experience.py`：实习周期格式的 `experience` 归一为标准枚举；>10 万/月的薪资视为离群值置 NULL（保留岗位行，仅不参与薪资统计）
3. `dedup_tables.py`：同一表内「岗位 + 公司 + 城市」重复只保留最早入库的一条

## 数据采集

`spider/cdp_reader.py` 通过 Chrome DevTools Protocol 读取**本机已登录浏览器**中已渲染的页面内容，不注入自动化脚本、不破解加密参数，因此不会与页面的反自动化检测正面冲突。

运行前提：

```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir=<你的用户目录>
```

需人工登录后执行：

```bash
python spider/cdp_reader.py --keyword python --city 深圳 --pages 1
```

**使用提醒**：采集仅用于个人学习与研究，请遵守目标网站的 robots 协议与服务条款，控制频率、避免给站点造成压力，不要将采集数据用于商业用途或二次分发。本仓库不包含浏览器登录态与数据库转储，数据库连接统一通过环境变量注入。

## 分析报告

```bash
python analysis/analyze_data_jobs.py                 # 生成 报告_YYYYMMDD.md + 速览_YYYYMMDD.md
python analysis/analyze_data_jobs.py --no-filter     # 不过滤噪声，看原始口径
```

报告按日期命名保留历史版本，新数据入库后重跑即可刷新。统计口径见 `analysis/README.md`。

## 免责声明

本项目仅用于技术学习与研究：展示 Web 数据可视化、数据分析与工程化清洗的完整链路。数据来源于公开页面，版权归原站点与发布者所有；使用者需自行承担合规责任。

## License

[MIT](LICENSE)
