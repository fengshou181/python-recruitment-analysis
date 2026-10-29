# BOSS 直聘每日采集包装脚本
# 由 Windows 任务计划程序（BossRecruitDaily）调用，替代原先的「睡眠 + 定时唤醒」方案。
# 流程：确保 Chrome 处于 CDP 调试态 -> 执行采集 -> 做一次数据体检 -> 全部写入 logs/。
$ErrorActionPreference = 'Stop'

$root = 'E:\HUBXM01\python-recruitment-analysis-master'
$py   = 'E:\HM\software\Anaconda\ancon\python.exe'
$chrome  = 'C:\Users\Lenovo\AppData\Local\Google\Chrome\Application\chrome.exe'
$profile = Join-Path $root 'spider\chrome_profile'
$logDir  = Join-Path $root 'logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir ('daily_' + (Get-Date -Format 'yyyyMMdd_HHmm') + '.log')

function Write-Log($msg) {
    ('[{0}] {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $msg) |
        Tee-Object -FilePath $log -Append
}

function Test-Cdp {
    try {
        Invoke-WebRequest 'http://127.0.0.1:9222/json/version' -UseBasicParsing -TimeoutSec 3 | Out-Null
        return $true
    } catch { return $false }
}

Write-Log '===== 每日采集开始 ====='

# 1) 确保 Chrome 已带调试端口启动（复用已登录的 profile）
if (-not (Test-Cdp)) {
    Write-Log 'Chrome CDP 未就绪，启动中...'
    Start-Process $chrome -ArgumentList @(
        '--remote-debugging-port=9222',
        "--user-data-dir=$profile",
        'https://www.zhipin.com/web/geek/job?query=python&city=101280600'
    )
    $ok = $false
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Seconds 2
        if (Test-Cdp) { $ok = $true; break }
    }
    if (-not $ok) { Write-Log 'ERROR: CDP 端口 9222 未就绪，退出'; exit 1 }
}
Start-Sleep -Seconds 8   # 等页面与登录态加载

# 2) 采集：保守参数，避免触发风控
Write-Log '开始采集（10 城 × 3 页）...'
& $py (Join-Path $root 'spider\cdp_reader.py') `
    --keyword python --auto `
    --cities 北京 上海 深圳 杭州 广州 成都 武汉 西安 南京 苏州 `
    --pages 3 --interval 5 *>&1 | Tee-Object -FilePath $log -Append
Write-Log ('采集退出码: ' + $LASTEXITCODE)

# 3) 数据体检（dry-run，只报不改）
Write-Log '数据体检（只统计）...'
& $py (Join-Path $root 'clean_salary_experience.py') *>&1 | Tee-Object -FilePath $log -Append
& $py (Join-Path $root 'dedup_tables.py') *>&1 | Tee-Object -FilePath $log -Append

Write-Log '===== 每日采集结束 ====='
