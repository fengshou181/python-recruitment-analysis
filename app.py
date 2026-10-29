from flask import Flask, render_template, request, jsonify
import mysql
import json
import cloud
import match
import speculate
from flask_caching import Cache
import math

app = Flask(__name__)

'''缓存设置'''
cache = Cache()
cache.init_app(app=app, config={'CACHE_TYPE': 'simple'})
timeout = 300

'''首页'''


@app.route('/')
@cache.cached(timeout=timeout)
def frontPage():
    wc = cloud.Cloud()
    wc.popularJobs()
    wc.welfareCloud()
    sql = mysql.MySql()
    num = sql.getLastNum()
    avg = sql.getAllAvgSalary()
    Max = sql.getMaxSalary()
    Min = sql.getMinSalary()
    return render_template('index.html', num=num, avg=avg, Max=Max, Min=Min)


@app.route('/getEducation')
@cache.cached(timeout=timeout)
def getEducation():
    sql = mysql.MySql()
    edu = sql.getEducation()
    return edu


@app.route('/getSalaryForEducation')
@cache.cached(timeout=timeout)
def getSalaryForEducation():
    sql = mysql.MySql()
    salary = sql.getSalaryForEducation()
    return salary


@app.route('/getExperience')
@cache.cached(timeout=timeout)
def getExperience():
    sql = mysql.MySql()
    exp = sql.getExperience()
    return exp


@app.route('/getSalaryForExperience')
@cache.cached(timeout=timeout)
def getSalaryForExperience():
    sql = mysql.MySql()
    salary = sql.getSalaryForExperience()
    return salary


@app.route('/getSalaryForCity')
@cache.cached(timeout=timeout)
def getSalaryForCity():
    sql = mysql.MySql()
    salary = sql.getSalaryForCity()
    return salary


@app.route('/index.html')
@cache.cached(timeout=timeout)
def index():
    wc = cloud.Cloud()
    wc.popularJobs()
    wc.welfareCloud()
    sql = mysql.MySql()
    num = sql.getLastNum()
    avg = sql.getAllAvgSalary()
    Max = sql.getMaxSalary()
    Min = sql.getMinSalary()
    return render_template('index.html', num=num, avg=avg, Max=Max, Min=Min)


'''Java'''


@app.route('/javaGetEdu')
@cache.cached(timeout=timeout)
def javaGetEdu():
    sql = mysql.MySql()
    edu = sql.javaGetEdu()
    return edu


@app.route('/javaGetExp')
@cache.cached(timeout=timeout)
def javaGetExp():
    sql = mysql.MySql()
    exp = sql.javaGetExp()
    return exp


@app.route('/javaGetEduForSalary')
@cache.cached(timeout=timeout)
def javaGetEduForSalary():
    sql = mysql.MySql()
    salary = sql.javaGetEduForSalary()
    return salary


@app.route('/javaGetExpForSalary')
@cache.cached(timeout=timeout)
def javaGetExpForSalary():
    sql = mysql.MySql()
    salary = sql.javaGetExpForSalary()
    return salary


@app.route('/javaRadar')
@cache.cached(timeout=timeout)
def javaRadar():
    sql = mysql.MySql()
    radar = sql.javaRadar()
    return radar


@app.route('/java.html')
@cache.cached(timeout=timeout)
def java():
    wc = cloud.Cloud()
    wc.javaSkillCloud()
    sql = mysql.MySql()
    num = sql.javaGetNum()
    avg = sql.javaGetAvgSalary()
    Max = sql.javaGetMaxSalary()
    Min = sql.javaGetMinSalary()
    return render_template('java.html', num=num, avg=avg, Max=Max, Min=Min)


'''python'''


@app.route('/pythonGetEdu')
@cache.cached(timeout=timeout)
def pythonGetEdu():
    sql = mysql.MySql()
    edu = sql.pythonGetEdu()
    return edu


@app.route('/pythonGetExp')
@cache.cached(timeout=timeout)
def pythonGetExp():
    sql = mysql.MySql()
    exp = sql.pythonGetExp()
    return exp


@app.route('/pythonGetEduForSalary')
@cache.cached(timeout=timeout)
def pythonGetEduForSalary():
    sql = mysql.MySql()
    salary = sql.pythonGetEduForSalary()
    return salary


@app.route('/pythonGetExpForSalary')
@cache.cached(timeout=timeout)
def pythonGetExpForSalary():
    sql = mysql.MySql()
    salary = sql.pythonGetExpForSalary()
    return salary


@app.route('/pythonRadar')
@cache.cached(timeout=timeout)
def pythonRadar():
    sql = mysql.MySql()
    radar = sql.pythonRadar()
    return radar


@app.route('/python.html')
@cache.cached(timeout=timeout)
def python():
    wc = cloud.Cloud()
    wc.pythonSkillCloud()
    sql = mysql.MySql()
    num = sql.pythonGetNum()
    avg = sql.pythonGetAvgSalary()
    Max = sql.pythonGetMaxSalary()
    Min = sql.pythonGetMinSalary()
    return render_template('python.html', num=num, avg=avg, Max=Max, Min=Min)


'''data数据分析'''


@app.route('/dataGetEdu')
@cache.cached(timeout=timeout)
def dataGetEdu():
    sql = mysql.MySql()
    edu = sql.dataGetEdu()
    return edu


@app.route('/dataGetExp')
@cache.cached(timeout=timeout)
def dataGetExp():
    sql = mysql.MySql()
    exp = sql.dataGetExp()
    return exp


@app.route('/dataGetEduForSalary')
@cache.cached(timeout=timeout)
def dataGetEduForSalary():
    sql = mysql.MySql()
    salary = sql.dataGetEduForSalary()
    return salary


@app.route('/dataGetExpForSalary')
@cache.cached(timeout=timeout)
def dataGetExpForSalary():
    sql = mysql.MySql()
    salary = sql.dataGetExpForSalary()
    return salary


@app.route('/dataRadar')
@cache.cached(timeout=timeout)
def dataRadar():
    sql = mysql.MySql()
    radar = sql.dataRadar()
    return radar


@app.route('/data.html')
@cache.cached(timeout=timeout)
def data():
    sql = mysql.MySql()
    num = sql.dataGetNum()
    avg = sql.dataGetAvgSalary()
    Max = sql.dataGetMaxSalary()
    Min = sql.dataGetMinSalary()
    return render_template('data.html', num=num, avg=avg, Max=Max, Min=Min)


'''c'''


@app.route('/cGetEdu')
@cache.cached(timeout=timeout)
def cGetEdu():
    sql = mysql.MySql()
    edu = sql.cGetEdu()
    return edu


@app.route('/cGetExp')
@cache.cached(timeout=timeout)
def cGetExp():
    sql = mysql.MySql()
    exp = sql.cGetExp()
    return exp


@app.route('/cGetEduForSalary')
@cache.cached(timeout=timeout)
def cGetEduForSalary():
    sql = mysql.MySql()
    salary = sql.cGetEduForSalary()
    return salary


@app.route('/cGetExpForSalary')
@cache.cached(timeout=timeout)
def cGetExpForSalary():
    sql = mysql.MySql()
    salary = sql.cGetExpForSalary()
    return salary


@app.route('/cRadar')
@cache.cached(timeout=timeout)
def cRadar():
    sql = mysql.MySql()
    radar = sql.cRadar()
    return radar


@app.route('/c.html')
@cache.cached(timeout=timeout)
def c():
    wc = cloud.Cloud()
    wc.cSkillCloud()
    sql = mysql.MySql()
    num = sql.cGetNum()
    avg = sql.cGetAvgSalary()
    Max = sql.cGetMaxSalary()
    Min = sql.cGetMinSalary()
    return render_template('c.html', num=num, avg=avg, Max=Max, Min=Min)


'''c23'''


@app.route('/c23GetEdu')
@cache.cached(timeout=timeout)
def c23GetEdu():
    sql = mysql.MySql()
    edu = sql.c23GetEdu()
    return edu


@app.route('/c23GetExp')
@cache.cached(timeout=timeout)
def c23GetExp():
    sql = mysql.MySql()
    exp = sql.c23GetExp()
    return exp


@app.route('/c23GetEduForSalary')
@cache.cached(timeout=timeout)
def c23GetEduForSalary():
    sql = mysql.MySql()
    salary = sql.c23GetEduForSalary()
    return salary


@app.route('/c23GetExpForSalary')
@cache.cached(timeout=timeout)
def c23GetExpForSalary():
    sql = mysql.MySql()
    salary = sql.c23GetExpForSalary()
    return salary


@app.route('/c23Radar')
@cache.cached(timeout=timeout)
def c23Radar():
    sql = mysql.MySql()
    radar = sql.c23Radar()
    return radar


@app.route('/c23.html')
@cache.cached(timeout=timeout)
def c23():
    wc = cloud.Cloud()
    wc.c23SkillCloud()
    sql = mysql.MySql()
    num = sql.c23GetNum()
    avg = sql.c23GetAvgSalary()
    Max = sql.c23GetMaxSalary()
    Min = sql.c23GetMinSalary()
    return render_template('c23.html', num=num, avg=avg, Max=Max, Min=Min)


'''u3dUe'''


@app.route('/u3dUeGetEdu')
@cache.cached(timeout=timeout)
def u3dUeGetEdu():
    sql = mysql.MySql()
    edu = sql.u3dUeGetEdu()
    return edu


@app.route('/u3dUeGetExp')
@cache.cached(timeout=timeout)
def u3dUeGetExp():
    sql = mysql.MySql()
    exp = sql.u3dUeGetExp()
    return exp


@app.route('/u3dUeGetEduForSalary')
@cache.cached(timeout=timeout)
def u3dUeGetEduForSalary():
    sql = mysql.MySql()
    salary = sql.u3dUeGetEduForSalary()
    return salary


@app.route('/u3dUeGetExpForSalary')
@cache.cached(timeout=timeout)
def u3dUeGetExpForSalary():
    sql = mysql.MySql()
    salary = sql.u3dUeGetExpForSalary()
    return salary


@app.route('/u3dUeRadar')
@cache.cached(timeout=timeout)
def u3dUeRadar():
    sql = mysql.MySql()
    radar = sql.u3dUeRadar()
    return radar


@app.route('/u3d-ue.html')
@cache.cached(timeout=timeout)
def u3dUe():
    wc = cloud.Cloud()
    wc.u3dUeSkillCloud()
    sql = mysql.MySql()
    num = sql.u3dUeGetNum()
    avg = sql.u3dUeGetAvgSalary()
    Max = sql.u3dUeGetMaxSalary()
    Min = sql.u3dUeGetMinSalary()
    return render_template('u3d-ue.html', num=num, avg=avg, Max=Max, Min=Min)


'''php'''


@app.route('/phpGetEdu')
@cache.cached(timeout=timeout)
def phpGetEdu():
    sql = mysql.MySql()
    edu = sql.phpGetEdu()
    return edu


@app.route('/phpGetExp')
@cache.cached(timeout=timeout)
def phpGetExp():
    sql = mysql.MySql()
    exp = sql.phpGetExp()
    return exp


@app.route('/phpGetEduForSalary')
@cache.cached(timeout=timeout)
def phpGetEduForSalary():
    sql = mysql.MySql()
    salary = sql.phpGetEduForSalary()
    return salary


@app.route('/phpGetExpForSalary')
@cache.cached(timeout=timeout)
def phpGetExpForSalary():
    sql = mysql.MySql()
    salary = sql.phpGetExpForSalary()
    return salary


@app.route('/phpRadar')
@cache.cached(timeout=timeout)
def phpRadar():
    sql = mysql.MySql()
    radar = sql.phpRadar()
    return radar


@app.route('/php.html')
@cache.cached(timeout=timeout)
def php():
    wc = cloud.Cloud()
    wc.phpSkillCloud()
    sql = mysql.MySql()
    num = sql.phpGetNum()
    avg = sql.phpGetAvgSalary()
    Max = sql.phpGetMaxSalary()
    Min = sql.phpGetMinSalary()
    return render_template('php.html', num=num, avg=avg, Max=Max, Min=Min)


'''web'''


@app.route('/webGetEdu')
@cache.cached(timeout=timeout)
def webGetEdu():
    sql = mysql.MySql()
    edu = sql.webGetEdu()
    return edu


@app.route('/webGetExp')
@cache.cached(timeout=timeout)
def webGetExp():
    sql = mysql.MySql()
    exp = sql.webGetExp()
    return exp


@app.route('/webGetEduForSalary')
@cache.cached(timeout=timeout)
def webGetEduForSalary():
    sql = mysql.MySql()
    salary = sql.webGetEduForSalary()
    return salary


@app.route('/webGetExpForSalary')
@cache.cached(timeout=timeout)
def webGetExpForSalary():
    sql = mysql.MySql()
    salary = sql.webGetExpForSalary()
    return salary


@app.route('/webRadar')
@cache.cached(timeout=timeout)
def webRadar():
    sql = mysql.MySql()
    radar = sql.webRadar()
    return radar


@app.route('/web.html')
@cache.cached(timeout=timeout)
def web():
    wc = cloud.Cloud()
    wc.webSkillCloud()
    sql = mysql.MySql()
    num = sql.webGetNum()
    avg = sql.webGetAvgSalary()
    Max = sql.webGetMaxSalary()
    Min = sql.webGetMinSalary()
    return render_template('web.html', num=num, avg=avg, Max=Max, Min=Min)


'''Android'''


@app.route('/AndroidGetEdu')
@cache.cached(timeout=timeout)
def AndroidGetEdu():
    sql = mysql.MySql()
    edu = sql.AndroidGetEdu()
    return edu


@app.route('/AndroidGetExp')
@cache.cached(timeout=timeout)
def AndroidGetExp():
    sql = mysql.MySql()
    exp = sql.AndroidGetExp()
    return exp


@app.route('/AndroidGetEduForSalary')
@cache.cached(timeout=timeout)
def AndroidGetEduForSalary():
    sql = mysql.MySql()
    salary = sql.AndroidGetEduForSalary()
    return salary


@app.route('/AndroidGetExpForSalary')
@cache.cached(timeout=timeout)
def AndroidGetExpForSalary():
    sql = mysql.MySql()
    salary = sql.AndroidGetExpForSalary()
    return salary


@app.route('/AndroidRadar')
@cache.cached(timeout=timeout)
def AndroidRadar():
    sql = mysql.MySql()
    radar = sql.AndroidRadar()
    return radar


@app.route('/android.html')
@cache.cached(timeout=timeout)
def Android():
    wc = cloud.Cloud()
    wc.AndroidSkillCloud()
    sql = mysql.MySql()
    num = sql.AndroidGetNum()
    avg = sql.AndroidGetAvgSalary()
    Max = sql.AndroidGetMaxSalary()
    Min = sql.AndroidGetMinSalary()
    return render_template('android.html', num=num, avg=avg, Max=Max, Min=Min)


'''ios'''


@app.route('/iosGetEdu')
@cache.cached(timeout=timeout)
def iosGetEdu():
    sql = mysql.MySql()
    edu = sql.iosGetEdu()
    return edu


@app.route('/iosGetExp')
@cache.cached(timeout=timeout)
def iosGetExp():
    sql = mysql.MySql()
    exp = sql.iosGetExp()
    return exp


@app.route('/iosGetEduForSalary')
@cache.cached(timeout=timeout)
def iosGetEduForSalary():
    sql = mysql.MySql()
    salary = sql.iosGetEduForSalary()
    return salary


@app.route('/iosGetExpForSalary')
@cache.cached(timeout=timeout)
def iosGetExpForSalary():
    sql = mysql.MySql()
    salary = sql.iosGetExpForSalary()
    return salary


@app.route('/iosRadar')
@cache.cached(timeout=timeout)
def iosRadar():
    sql = mysql.MySql()
    radar = sql.iosRadar()
    return radar


@app.route('/ios.html')
@cache.cached(timeout=timeout)
def ios():
    wc = cloud.Cloud()
    wc.iosSkillCloud()
    sql = mysql.MySql()
    num = sql.iosGetNum()
    avg = sql.iosGetAvgSalary()
    Max = sql.iosGetMaxSalary()
    Min = sql.iosGetMinSalary()
    return render_template('ios.html', num=num, avg=avg, Max=Max, Min=Min)


'''algorithm'''


@app.route('/algorithmGetEdu')
@cache.cached(timeout=timeout)
def algorithmGetEdu():
    sql = mysql.MySql()
    edu = sql.algorithmGetEdu()
    return edu


@app.route('/algorithmGetExp')
@cache.cached(timeout=timeout)
def algorithmGetExp():
    sql = mysql.MySql()
    exp = sql.algorithmGetExp()
    return exp


@app.route('/algorithmGetEduForSalary')
@cache.cached(timeout=timeout)
def algorithmGetEduForSalary():
    sql = mysql.MySql()
    salary = sql.algorithmGetEduForSalary()
    return salary


@app.route('/algorithmGetExpForSalary')
@cache.cached(timeout=timeout)
def algorithmGetExpForSalary():
    sql = mysql.MySql()
    salary = sql.algorithmGetExpForSalary()
    return salary


@app.route('/algorithmRadar')
@cache.cached(timeout=timeout)
def algorithmRadar():
    sql = mysql.MySql()
    radar = sql.algorithmRadar()
    return radar


@app.route('/algorithm.html')
@cache.cached(timeout=timeout)
def algorithm():
    wc = cloud.Cloud()
    wc.algorithmSkillCloud()
    sql = mysql.MySql()
    num = sql.algorithmGetNum()
    avg = sql.algorithmGetAvgSalary()
    Max = sql.algorithmGetMaxSalary()
    Min = sql.algorithmGetMinSalary()
    return render_template('algorithm.html', num=num, avg=avg, Max=Max, Min=Min)


'''test'''


@app.route('/testGetEdu')
@cache.cached(timeout=timeout)
def testGetEdu():
    sql = mysql.MySql()
    edu = sql.testGetEdu()
    return edu


@app.route('/testGetExp')
@cache.cached(timeout=timeout)
def testGetExp():
    sql = mysql.MySql()
    exp = sql.testGetExp()
    return exp


@app.route('/testGetEduForSalary')
@cache.cached(timeout=timeout)
def testGetEduForSalary():
    sql = mysql.MySql()
    salary = sql.testGetEduForSalary()
    return salary


@app.route('/testGetExpForSalary')
@cache.cached(timeout=timeout)
def testGetExpForSalary():
    sql = mysql.MySql()
    salary = sql.testGetExpForSalary()
    return salary


@app.route('/testRadar')
@cache.cached(timeout=timeout)
def testRadar():
    sql = mysql.MySql()
    radar = sql.testRadar()
    return radar


@app.route('/test.html')
@cache.cached(timeout=timeout)
def test():
    wc = cloud.Cloud()
    wc.testSkillCloud()
    sql = mysql.MySql()
    num = sql.testGetNum()
    avg = sql.testGetAvgSalary()
    Max = sql.testGetMaxSalary()
    Min = sql.testGetMinSalary()
    return render_template('test.html', num=num, avg=avg, Max=Max, Min=Min)


'''oam'''


@app.route('/oamGetEdu')
@cache.cached(timeout=timeout)
def oamGetEdu():
    sql = mysql.MySql()
    edu = sql.oamGetEdu()
    return edu


@app.route('/oamGetExp')
@cache.cached(timeout=timeout)
def oamGetExp():
    sql = mysql.MySql()
    exp = sql.oamGetExp()
    return exp


@app.route('/oamGetEduForSalary')
@cache.cached(timeout=timeout)
def oamGetEduForSalary():
    sql = mysql.MySql()
    salary = sql.oamGetEduForSalary()
    return salary


@app.route('/oamGetExpForSalary')
@cache.cached(timeout=timeout)
def oamGetExpForSalary():
    sql = mysql.MySql()
    salary = sql.oamGetExpForSalary()
    return salary


@app.route('/oamRadar')
@cache.cached(timeout=timeout)
def oamRadar():
    sql = mysql.MySql()
    radar = sql.oamRadar()
    return radar


@app.route('/oam.html')
@cache.cached(timeout=timeout)
def oam():
    wc = cloud.Cloud()
    wc.oamSkillCloud()
    sql = mysql.MySql()
    num = sql.oamGetNum()
    avg = sql.oamGetAvgSalary()
    Max = sql.oamGetMaxSalary()
    Min = sql.oamGetMinSalary()
    return render_template('oam.html', num=num, avg=avg, Max=Max, Min=Min)


'''匹配'''


@app.route('/job-speculate.html')
def job_speculate():
    """岗位匹配页面"""
    return render_template('job-speculate.html')


@app.route('/job-submit', methods=['POST', 'GET'])
def job_submit():
    """处理岗位匹配请求"""
    try:
        # 获取分页参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        
        # 检查是否是从结果页面提交的筛选请求
        if request.method == 'GET' and request.args.get('from_results') == 'true':
            # 从查询参数获取筛选条件
            name = request.args.get('name', '')
            province = request.args.get('province', '')
            city = request.args.get('city', '')
            district = request.args.get('district', '')
            education = request.args.get('education', '')
            experience = request.args.get('experience', '')
            skill_text = request.args.get('skill', '')
            salary = request.args.get('salary', 0)
            scale = request.args.get('scale', '')
            priority = request.args.get('priority', 'match')
            min_match = float(request.args.get('min_match', 0)) / 100  # 转换为0-1的比例
            
            # 获取薪资范围
            min_salary = int(request.args.get('min_salary', 0) or 0)
            max_salary = int(request.args.get('max_salary', 0) or 0)
            salary = min_salary if min_salary > 0 else salary
        else:
            # 从表单获取数据
            name = request.form.get('name', '')             # 岗位方向
            province = request.form.get('province', '')     # 省份
            city = request.form.get('city', '')             # 城市
            district = request.form.get('district', '')     # 区县
            education = request.form.get('education', '')   # 学历
            experience = request.form.get('experience', '')  # 工作经验
            skill_text = request.form.get('skill', '')      # 技能（字符串）
            salary = request.form.get('salary', 0)          # 期望薪资
            scale = request.form.get('scale', '')           # 公司规模
            priority = request.form.get('priority', 'match') # 匹配优先级
            min_match = 0  # 默认不设置最低匹配度要求
        
        # 数据验证
        if not skill_text:
            from flask import flash, redirect, url_for
            flash('请至少输入一项技能', 'danger')
            return redirect(url_for('job_speculate'))
            
        # 处理技能列表
        skills = [s.strip() for s in skill_text.split() if s.strip()] 
        
        # 将薪资转为整数
        try:
            salary = int(salary) if salary else 0
        except (ValueError, TypeError):
            salary = 0
        
        # 使用mysql.py中的方法查询匹配岗位
        db = mysql.MySql()
        matched_jobs, total_jobs = db.match_jobs(name, province, city, skills, education, experience, salary, scale, 
                                                 priority, page, page_size)
        
        # 如果设置了最低匹配度要求，过滤结果
        if min_match > 0:
            matched_jobs = [job for job in matched_jobs if job['match_score'] >= min_match]
        
        # 构建前端所需数据结构
        job_input = {
            'name': name,
            'province': province,
            'city': city,
            'district': district,
            'education': education,
            'experience': experience,
            'skills': skills,
            'salary': salary,
            'scale': scale,
            'priority': priority
        }
        
        # 使用mysql.py中的方法计算匹配分析
        match_analysis = db.calculate_match_analysis(matched_jobs, skills)
        
        # 计算分页信息
        total_pages = (total_jobs + page_size - 1) // page_size
        has_prev = page > 1
        has_next = page < total_pages
        
        # 从匹配分析中提取技能匹配度和其他分析数据
        skill_match_percentage = int(match_analysis.get('skill_match_percentage', 0))
        area_match_percentage = int(match_analysis.get('area_match_percentage', 80))
        avg_salary = match_analysis.get('avg_salary', 0)
        avg_salary_text = f"{int(avg_salary/1000)}K" if avg_salary else "0K"
        
        # 岗位方向匹配和学历匹配默认值
        job_match = 90
        edu_match = 85
        
        # 构建缺失技能列表
        missing_skills = []
        for skill_info in match_analysis.get('missing_skills', []):
            missing_skills.append(skill_info['name'])
        
        # 渲染结果页面
        return render_template(
            'job-match-result.html',
            job_input=job_input,
            jobs=matched_jobs,
            skills=skills,
            missing_skills=missing_skills,
            skill_match=skill_match_percentage,
            area_match=area_match_percentage,
            job_match=job_match,
            edu_match=edu_match,
            avg_salary=avg_salary_text,
            # 分页信息
            page=page,
            page_size=page_size,
            total_jobs=total_jobs,
            total_pages=total_pages,
            has_prev=has_prev,
            has_next=has_next
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        from flask import flash, redirect, url_for
        flash(f'处理岗位匹配请求时发生错误: {str(e)}', 'danger')
        return redirect(url_for('job_speculate'))

@app.route('/salary-speculate.html')
def salary_speculate():
    return render_template('salary-speculate.html')

@app.route('/salary-submit', methods=['GET', 'POST'])
def salary_submit():
    if request.method == 'POST':
        try:
            # 获取表单数据
            province = request.form.get('province')
            city = request.form.get('city')
            area = request.form.get('area')
            job = request.form.get('job')
            scale = request.form.get('scale')
            name = request.form.get('name')
            education = request.form.get('education')
            experience = request.form.get('experience')
            skill = request.form.get('skill')
            
            # 数据验证
            if not all([province, city, area, job, scale, name, education, experience, skill]):
                return render_template("speculate-result.html", 
                                       error="所有字段都为必填项，请返回填写完整",
                                       job_input={})
            
            # 准备输入数据
            input_data = {
                'province': province,
                'city': city,
                'area': area,
                'scale': scale,
                'name': name,
                'education': education,
                'experience': experience,
                'skill': skill
            }
            
            # 导入模型并预测
            from salary_model import SalaryPredictor
            predictor = SalaryPredictor()
            
            # 尝试加载模型
            if not predictor.load_model():
                return render_template("speculate-result.html", 
                                    error="模型加载失败，请联系管理员",
                                    job_input=input_data)
            
            # 执行预测
            prediction = predictor.predict_salary(input_data)
            
            # 格式化结果
            min_salary = prediction['min_salary']
            max_salary = prediction['max_salary']
            avg_salary = prediction['avg_salary']
            confidence = prediction['confidence']
            
            # 处理展示格式
            min_salary_text = f"{int(min_salary/1000)}K"
            max_salary_text = f"{int(max_salary/1000)}K"
            avg_salary_text = f"{int(avg_salary/1000)}K"
            
            # 计算置信度百分比
            confidence_percent = int(confidence * 100)
            
            # 设置置信度颜色
            if confidence_percent >= 80:
                confidence_color = "bg-success"
            elif confidence_percent >= 60:
                confidence_color = "bg-info"
            else:
                confidence_color = "bg-warning"
            
            # 影响因素权重 (基于模型的特征重要性)
            factor_weights = {
                'location': 35,   # 地区影响
                'experience': 25,  # 经验影响
                'education': 15,   # 学历影响
                'skills': 15,      # 技能影响
                'scale': 10        # 公司规模影响
            }
            
            # 准备结果数据
            result = {
                'min_salary': min_salary,
                'max_salary': max_salary,
                'avg_salary': avg_salary,
                'confidence': confidence,
                'min_salary_text': min_salary_text,
                'max_salary_text': max_salary_text,
                'avg_salary_text': avg_salary_text,
                'confidence_percent': confidence_percent,
                'confidence_color': confidence_color
            }
            
            # 准备输入数据(用于显示)
            job_input = {
                'province': province,
                'city': city,
                'area': area,
                'job': job,
                'scale': scale,
                'name': name,
                'education': education,
                'experience': experience,
                'skill': skill
            }
            
            # 获取相似岗位（这里可以添加实际的相似岗位查询逻辑）
            similar_jobs = []
            
            return render_template("speculate-result.html", 
                                  result=result, 
                                  job_input=job_input, 
                                  factor_weights=factor_weights,
                                  similar_jobs=similar_jobs)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return render_template("speculate-result.html", 
                                  error=f"处理请求时发生错误: {str(e)}",
                                  job_input={})
    else:
        return render_template("404.html")

@app.route('/charts.html')
@cache.cached(timeout=timeout)
def charts():
    return render_template("charts.html")


@app.route('/cards.html')
@cache.cached(timeout=timeout)
def cards():
    return render_template("demo/cards.html")


@app.route('/forgot-password.html')
def forgotPassword():
    return render_template("forgot-password.html")


@app.route('/login.html')
def login():
    return render_template("login.html")


@app.route('/tables.html')
@cache.cached(timeout=timeout)
def tables():
    return render_template("tables.html")


@app.route('/register.html')
def register():
    return render_template("register.html")


@app.route('/404.html')
def error():
    return render_template("404.html")


@app.route('/salary-map.html')
def salary_map():
    return render_template('salary-map.html')


@app.route('/api/salary-map-data')
def get_salary_map_data():
    """
    获取薪资热力图数据接口
    """
    # 获取查询参数
    job_table = request.args.get('job_table', '')
    education = request.args.get('education', '')
    experience = request.args.get('experience', '')
    scale = request.args.get('scale', '')
    province = request.args.get('province', '')
    city = request.args.get('city', '')  # 新增城市参数
    level = request.args.get('level', 'country')
    metric = request.args.get('metric', 'salary')  # 默认是薪资
    
    # 调试日志
    print(f"DEBUG API: level={level}, province={province}, city={city}, job_table={job_table}")
    
    # 硬编码城市-省份映射表
    city_province_map = {
        '北京': '北京',
        '天津': '天津',
        '上海': '上海',
        '广州': '广东',
        '深圳': '广东',
        '杭州': '浙江',
        '宁波': '浙江',
        '合肥': '安徽',
        '南京': '江苏',
        '苏州': '江苏',
        '成都': '四川',
        '重庆': '重庆',
        '武汉': '湖北',
        '长沙': '湖南',
        '西安': '陕西',
        '青岛': '山东',
        '济南': '山东',
        '郑州': '河南',
        '石家庄': '河北',
        '福州': '福建',
        '厦门': '福建',
        '东莞': '广东',
        '佛山': '广东',
        '大连': '辽宁',
        '沈阳': '辽宁',
        '哈尔滨': '黑龙江',
        '长春': '吉林',
        '呼和浩特': '内蒙古',
        '太原': '山西',
        '乌鲁木齐': '新疆',
        '兰州': '甘肃',
        '银川': '宁夏',
        '南昌': '江西',
        '贵阳': '贵州',
        '昆明': '云南',
        '南宁': '广西',
        '海口': '海南'
    }
    
    # 直辖市列表
    direct_cities = ['北京', '上海', '天津', '重庆']
    
    try:
        db = mysql.MySql()
        
        # 移除省份或城市名称中可能存在的后缀
        if province and (province.endswith('省') or province.endswith('市') or province.endswith('自治区')):
            province = province.replace('省', '').replace('市', '').replace('自治区', '')
        
        # 重要修改：确保当province有值时level必须是province
        if province:
            level = 'province'
            print(f"DEBUG: 由于提供了省份参数 {province}，设置level为province")
            
        # 对于直辖市，特殊处理
        if province in direct_cities:
            # 直辖市当作省份处理
            print(f"DEBUG: 处理直辖市 {province}")
        
        print(f"DEBUG: 使用级别 {level}, 省份: {province}")
        
        if level == 'country':
            # 获取省级数据
            map_data = db.getProvinceSalaryData(
                job_table=job_table,
                education=education,
                experience=experience,
                scale=scale
            )

            # 数据实际按城市分组，聚合到省份：薪资按岗位数加权平均，岗位数求和
            city_counts = {}
            for item in map_data.get('job_count', []):
                pname = city_province_map.get(item['name'], item['name'])
                city_counts[pname] = city_counts.get(pname, 0) + (item['value'] or 0)

            prov_salary_weighted = {}
            prov_salary_cnt = {}
            raw_counts = {item['name']: (item['value'] or 0) for item in map_data.get('job_count', [])}
            for item in map_data.get('salary', []):
                pname = city_province_map.get(item['name'], item['name'])
                cnt = raw_counts.get(item['name'], 0) or 0
                prov_salary_weighted[pname] = prov_salary_weighted.get(pname, 0) + (item['value'] or 0) * cnt
                prov_salary_cnt[pname] = prov_salary_cnt.get(pname, 0) + cnt

            map_data = {
                'salary': [
                    {'name': p, 'value': int(prov_salary_weighted[p] / prov_salary_cnt[p])}
                    for p in prov_salary_weighted if prov_salary_cnt.get(p)
                ],
                'job_count': [
                    {'name': p, 'value': c} for p, c in city_counts.items()
                ]
            }
            
            # 数据预处理：修正数据中的省份名称，移除后缀
            if 'salary' in map_data:
                for item in map_data['salary']:
                    if item.get('name') and (item['name'].endswith('省') or item['name'].endswith('市') or item['name'].endswith('自治区')):
                        item['name'] = item['name'].replace('省', '').replace('市', '').replace('自治区', '')
                        
            if 'job_count' in map_data:
                for item in map_data['job_count']:
                    if item.get('name') and (item['name'].endswith('省') or item['name'].endswith('市') or item['name'].endswith('自治区')):
                        item['name'] = item['name'].replace('省', '').replace('市', '').replace('自治区', '')
            
            # 获取排名TOP10
            rank_data = db.getSalaryRankTop10(
                job_table=job_table,
                education=education,
                experience=experience,
                scale=scale,
                metric=metric
            )
        elif level == 'province' and province:
            # 获取特定省份的城市数据
            map_data = db.getCitySalaryData(
                province=province,
                job_table=job_table,
                education=education,
                experience=experience, 
                scale=scale
            )
            
            # 获取省内城市排名TOP10
            rank_data = db.getSalaryRankTop10(
                province=province,
                job_table=job_table,
                education=education,
                experience=experience,
                scale=scale, 
                metric=metric
            )
        else:
            map_data = {
                'salary': [],
                'job_count': []
            }
            rank_data = []
        
        # 处理薪资和岗位数据，确保没有NaN值
        salary_data = map_data.get('salary', [])
        job_count_data = map_data.get('job_count', [])
        
        # 数据过滤，移除无效值
        salary_data = [item for item in salary_data if isinstance(item.get('value'), (int, float)) and not math.isnan(item['value'])]
        job_count_data = [item for item in job_count_data if isinstance(item.get('value'), (int, float)) and not math.isnan(item['value'])]
        
        print(f"DEBUG: 薪资数据条数 {len(salary_data)}, 岗位数据条数 {len(job_count_data)}")
        
        # 处理排名数据，确保格式正确
        if rank_data:
            for item in rank_data:
                # 确保数值字段是整数
                if 'salary' in item and item['salary'] is not None:
                    try:
                        item['salary'] = int(float(item['salary']))
                    except (ValueError, TypeError):
                        item['salary'] = 0
                else:
                    item['salary'] = 0
                    
                if 'job_count' in item and item['job_count'] is not None:
                    try:
                        item['job_count'] = int(float(item['job_count']))
                    except (ValueError, TypeError):
                        item['job_count'] = 0
                else:
                    item['job_count'] = 0
                    
                # 去掉名称中可能有的后缀
                if item.get('name'):
                    if item['name'].endswith('市') or item['name'].endswith('省') or item['name'].endswith('自治区'):
                        item['name'] = item['name'].replace('市', '').replace('省', '').replace('自治区', '')
            
            print(f"DEBUG: 排名数据条数 {len(rank_data)}")
        
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': {
                'salary': salary_data,
                'job_count': job_count_data,
                'ranking': rank_data
            }
        })
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()  # 打印完整错误堆栈
        
        return jsonify({
            'code': 1,
            'message': error_msg,
            'data': {
                'salary': [],
                'job_count': [],
                'ranking': []
            }
        })

@app.route('/api/province-detail')
def get_province_detail():
    """
    获取省份详细数据接口（包含城市数据）
    """
    # 获取查询参数
    province_name = request.args.get('province', '')
    job_table = request.args.get('job_table', '')
    education = request.args.get('education', '')
    experience = request.args.get('experience', '')
    scale = request.args.get('scale', '')
    
    # 移除省份名称中可能存在的后缀
    if province_name and (province_name.endswith('省') or province_name.endswith('市') or province_name.endswith('自治区')):
        province_name = province_name.replace('省', '').replace('市', '').replace('自治区', '')
    
    print(f"DEBUG: 获取省份详细数据, 省份={province_name}, 职位类别={job_table}")
    
    # 硬编码城市-省份映射表
    city_province_map = {
        '北京': '北京',
        '天津': '天津',
        '上海': '上海',
        '广州': '广东',
        '深圳': '广东',
        '杭州': '浙江',
        '宁波': '浙江',
        '合肥': '安徽',
        '南京': '江苏',
        '苏州': '江苏',
        '成都': '四川',
        '重庆': '重庆',
        '武汉': '湖北',
        '长沙': '湖南',
        '西安': '陕西',
        '青岛': '山东',
        '济南': '山东',
        '郑州': '河南',
        '石家庄': '河北',
        '福州': '福建',
        '厦门': '福建',
        '东莞': '广东',
        '佛山': '广东',
        '大连': '辽宁',
        '沈阳': '辽宁',
        '哈尔滨': '黑龙江',
        '长春': '吉林',
        '呼和浩特': '内蒙古',
        '太原': '山西',
        '乌鲁木齐': '新疆',
        '兰州': '甘肃',
        '银川': '宁夏',
        '南昌': '江西',
        '贵阳': '贵州',
        '昆明': '云南',
        '南宁': '广西',
        '海口': '海南'
    }
    
    # 直辖市列表
    direct_cities = ['北京', '上海', '天津', '重庆']
    
    try:
        db = mysql.MySql()
        
        # 构建表名
        if not job_table:
            table_name = 'c_data'
        else:
            table_name = job_table + '_data'
        
        # 构建查询条件
        conditions = []
        params = []
        
        if education:
            conditions.append("education = %s")
            params.append(education)
        
        if experience:
            conditions.append("experience = %s")
            params.append(experience)
            
        if scale:
            conditions.append("scale = %s")
            params.append(scale)
        
        # 构建省份条件
        province_cities = []
        
        # 如果是直辖市，则直接查询该城市
        if province_name in direct_cities:
            conditions.append("city = %s OR city LIKE %s")
            params.append(province_name)
            params.append(f"{province_name}-%")
            print(f"DEBUG: 处理直辖市 {province_name}")
        else:
            # 对于普通省份，查找该省份下的所有城市
            for city, prov in city_province_map.items():
                if prov == province_name:
                    province_cities.append(city)
            
            if province_cities:
                city_conditions = []
                for city in province_cities:
                    city_conditions.append("city = %s OR city LIKE %s")
                    params.append(city)
                    params.append(f"{province_name}-{city}%")
                
                conditions.append("(" + " OR ".join(city_conditions) + ")")
                print(f"DEBUG: 查询省份 {province_name} 下的城市: {', '.join(province_cities)}")
            else:
                # 如果找不到对应的城市，尝试直接用省份名称查询
                conditions.append("city LIKE %s")
                params.append(f"{province_name}%")
                print(f"DEBUG: 未找到省份 {province_name} 的城市映射，使用模糊匹配")
        
        where_clause = " AND ".join(conditions) if conditions else ""
        
        # 构建查询SQL - 获取城市级数据
        sql = f'''
            SELECT 
                city,
                AVG(avg_salary) as avg_salary,
                MAX(avg_salary) as max_salary,
                MIN(avg_salary) as min_salary,
                COUNT(*) as job_count
            FROM {table_name}
        '''
        
        if where_clause:
            sql += f" WHERE {where_clause}"
            
        sql += " GROUP BY city"
        
        # 执行查询
        db.cursor.execute(sql, params)
        city_results = db.cursor.fetchall()
        
        # 处理城市数据
        cities_data = []
        total_salary = 0
        total_jobs = 0
        max_provincial_salary = 0
        min_provincial_salary = float('inf')
        
        for row in city_results:
            city_name = row['city'].split('-')[-1] if '-' in row['city'] else row['city']
            city_name = city_name + "市" if not city_name.endswith("市") else city_name
            avg_salary = int(row['avg_salary'])
            max_salary = int(row['max_salary'])
            min_salary = int(row['min_salary'])
            job_count = row['job_count']
            
            # 统计省级汇总数据
            total_salary += avg_salary * job_count
            total_jobs += job_count
            max_provincial_salary = max(max_provincial_salary, max_salary)
            min_provincial_salary = min(min_provincial_salary, min_salary) if min_salary > 0 else min_provincial_salary
            
            # 添加城市数据
            cities_data.append({
                "region": city_name,
                "province": province_name,
                "value": avg_salary,
                "count": job_count,
                "max": max_salary,
                "min": min_salary
            })
        
        # 计算省级平均薪资
        province_avg_salary = int(total_salary / total_jobs) if total_jobs > 0 else 0
        
        # 构建返回数据
        response_data = {
            "province": province_name,
            "average": province_avg_salary,
            "max": max_provincial_salary,
            "min": min_provincial_salary if min_provincial_salary != float('inf') else 0,
            "count": total_jobs,
            "cities": cities_data
        }
        
        print(f"DEBUG: 省份 {province_name} 总计找到 {len(cities_data)} 个城市数据")
        
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': response_data
        })
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()  # 打印完整错误堆栈
        
        return jsonify({
            'code': 1,
            'message': error_msg,
            'data': {
                "province": province_name,
                "average": 0,
                "max": 0,
                "min": 0,
                "count": 0,
                "cities": []
            }
        })

@app.route('/api/province-cities')
def get_province_cities():
    """
    获取省份及其城市详情API（使用新方法）
    """
    # 获取查询参数
    province = request.args.get('province', '')
    job_table = request.args.get('job_table', '')
    education = request.args.get('education', '')
    experience = request.args.get('experience', '')
    scale = request.args.get('scale', '')
    
    print(f"DEBUG: /api/province-cities 接收参数: province={province}, job_table={job_table}")
    
    try:
        db = mysql.MySql()
        # 使用新方法获取省份详情
        province_data = db.getProvinceDetail(
            province_name=province,
            job_table=job_table, 
            education=education,
            experience=experience,
            scale=scale
        )
        
        if province_data:
            return jsonify({
                'code': 0,
                'message': 'success',
                'data': province_data
            })
        else:
            return jsonify({
                'code': 1,
                'message': f'未找到省份 {province} 的数据',
                'data': {
                    "province": province,
                    "average": 0,
                    "max": 0,
                    "min": 0,
                    "count": 0,
                    "cities": []
                }
            })
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        
        return jsonify({
            'code': 1,
            'message': error_msg,
            'data': {
                "province": province,
                "average": 0,
                "max": 0,
                "min": 0,
                "count": 0,
                "cities": []
            }
        })

@app.route('/api/city-districts')
def get_city_districts():
    """
    获取城市及其区县详情API
    """
    # 获取查询参数
    province = request.args.get('province', '')
    city = request.args.get('city', '')
    job_table = request.args.get('job_table', '')
    education = request.args.get('education', '')
    experience = request.args.get('experience', '')
    scale = request.args.get('scale', '')
    
    print(f"DEBUG: /api/city-districts 接收参数: province={province}, city={city}, job_table={job_table}")
    
    try:
        db = mysql.MySql()
        # 使用新方法获取城市及区县详情
        city_data = db.getCityDistrictData(
            province_name=province,
            city_name=city,
            job_table=job_table, 
            education=education,
            experience=experience,
            scale=scale
        )
        
        if city_data:
            return jsonify({
                'code': 0,
                'message': 'success',
                'data': city_data
            })
        else:
            return jsonify({
                'code': 1,
                'message': f'未找到城市 {city} 的区县数据',
                'data': {
                    "province": province,
                    "city": city,
                    "average": 0,
                    "max": 0,
                    "min": 0,
                    "count": 0,
                    "districts": []
                }
            })
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        
        return jsonify({
            'code': 1,
            'message': error_msg,
            'data': {
                "province": province,
                "city": city,
                "average": 0,
                "max": 0,
                "min": 0,
                "count": 0,
                "districts": []
            }
        })

@app.route('/api/map/districts')
def get_map_districts():
    """
    获取城市及其区县详情API
    """
    # 获取查询参数
    city = request.args.get('city', '')
    job_table = request.args.get('job_table', '')
    education = request.args.get('education', '')
    experience = request.args.get('experience', '')
    scale = request.args.get('scale', '')
    
    print(f"DEBUG: /api/map/districts 接收参数: city={city}, job_table={job_table}")
    
    # 确定城市所在的省份
    province = None
    for key, value in city_province_map.items():
        if key.replace('市', '') == city.replace('市', ''):
            province = value
            break
    
    if not province and city in direct_cities:
        province = city  # 直辖市自己是省级单位
    
    try:
        db = mysql.MySql()
        # 使用现有的获取城市区县数据的方法
        city_data = db.getCityDistrictData(
            province_name=province,
            city_name=city,
            job_table=job_table, 
            education=education,
            experience=experience,
            scale=scale
        )
        
        if city_data and city_data.get('regions'):
            # 返回区县数据，按照要求的格式
            return jsonify({
                'code': 0,
                'message': 'success',
                'data': {
                    'level': 'district',
                    'regions': city_data.get('regions', [])
                }
            })
        else:
            return jsonify({
                'code': 1,
                'message': f'未找到城市 {city} 的区县数据',
                'data': {
                    'level': 'district',
                    'regions': []
                }
            })
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        
        return jsonify({
            'code': 1,
            'message': error_msg,
            'data': {
                'level': 'district',
                'regions': []
            }
        })

@app.route('/api/salary-predict', methods=['POST'])
def api_salary_predict():
    """薪资预测接口"""
    if request.method == 'POST':
        try:
            # 获取POST请求数据
            data = request.json or request.form.to_dict()
            
            # 必要参数检查
            required_fields = ['city', 'area', 'job', 'scale', 'name', 'education', 'experience', 'skill']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        'code': 1, 
                        'message': f'缺少必要参数: {field}',
                        'data': {}
                    })
                    
            # 处理技能参数
            skill = data['skill'].split(' ') if isinstance(data['skill'], str) else data['skill']
            
            # 实例化预测器
            sp = speculate.Speculate()
            
            # 获取详细预测结果
            result = sp.salary_predict_detail(
                city=data['city'],
                area=data['area'],
                lan=data['job'],
                scale=data['scale'],
                name=data['name'],
                education=data['education'],
                experience=data['experience'],
                skill=skill
            )
            
            # 格式化为前端需要的格式
            response = {
                'min_salary': result['min_salary'],
                'max_salary': result['max_salary'],
                'avg_salary': result['avg_salary'],
                'confidence': result['confidence']
            }
            
            # 格式化薪资显示
            response['min_salary_text'] = f"{int(response['min_salary']/1000)}K"
            response['max_salary_text'] = f"{int(response['max_salary']/1000)}K"
            response['avg_salary_text'] = f"{int(response['avg_salary']/1000)}K"
            
            return jsonify({
                'code': 0,
                'message': 'success',
                'data': response
            })
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({
                'code': 2,
                'message': f'服务器处理错误: {str(e)}',
                'data': {}
            })
    else:
        return jsonify({
            'code': 1,
            'message': '请使用POST方法请求此接口',
            'data': {}
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
