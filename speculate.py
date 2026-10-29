import os
from salary_model import SalaryPredictor


class Speculate:
    """薪资推测类"""

    def __init__(self):
        """初始化"""
        self.predictor = SalaryPredictor()
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model')
        self.model_loaded = self.predictor.load_model(model_path)

        if not self.model_loaded:
            print("警告：薪资预测模型加载失败，请先运行salary_model.py训练模型")

    def normalize_location(self, city, area=None):
        """规范化城市和地区信息"""
        if '市' not in city and city not in ['北京', '上海', '天津', '重庆']:
            city = city + '市'

        if not area and '区' in city:
            parts = city.split('区')
            if len(parts) > 1:
                city = parts[0] + '区'
                area = parts[1]

        return city, area

    def _prepare_input_data(self, city, area, lan, scale, name, education, experience, skill):
        """准备模型输入数据"""
        city, area = self.normalize_location(city, area)

        if lan.lower() not in name.lower():
            name = f"{lan}{name}" if name else lan

        skill_text = ' '.join(skill) if isinstance(skill, list) else skill

        return {
            'city': city,
            'area': area,
            'scale': scale,
            'name': name,
            'education': education,
            'experience': experience,
            'skill': skill_text
        }

    def salarySpeculate(self, city, area, lan, scale, name, education, experience, skill):
        """薪资推测主函数"""
        if not self.model_loaded:
            return 0
        try:
            input_data = self._prepare_input_data(
                city, area, lan, scale, name, education, experience, skill
            )
            prediction = self.predictor.predict_salary(input_data)
            return int(prediction['avg_salary'])
        except Exception as e:
            print(f"薪资预测发生错误: {str(e)}")
            return 0

    def salary_predict_detail(self, city, area, lan, scale, name, education, experience, skill):
        """获取详细的薪资预测信息"""
        if not self.model_loaded:
            return {
                'min_salary': 0,
                'max_salary': 0,
                'avg_salary': 0,
                'confidence': 0,
                'error': '模型未加载'
            }
        try:
            input_data = self._prepare_input_data(
                city, area, lan, scale, name, education, experience, skill
            )
            return self.predictor.predict_salary(input_data)
        except Exception as e:
            print(f"薪资预测发生错误: {str(e)}")
            return {
                'min_salary': 0,
                'max_salary': 0,
                'avg_salary': 0,
                'confidence': 0,
                'error': str(e)
            }


if __name__ == "__main__":
    sp = Speculate()
    test_data = {
        'city': '北京', 'area': '朝阳区', 'lan': 'Python',
        'scale': '1000-9999人', 'name': '开发工程师',
        'education': '本科', 'experience': '3-5年',
        'skill': ['Python', 'Django', 'Flask', '数据分析', '爬虫']
    }
    result = sp.salarySpeculate(**test_data)
    print(f"预测薪资: {result} 元/月")
    detail = sp.salary_predict_detail(**test_data)
    print(f"薪资区间: {detail['min_salary']} ~ {detail['max_salary']} 元/月")
    print(f"平均薪资: {detail['avg_salary']} 元/月")
    print(f"置信度: {detail['confidence']}")
