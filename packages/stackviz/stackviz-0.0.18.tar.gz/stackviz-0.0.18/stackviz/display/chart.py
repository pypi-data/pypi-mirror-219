"""
图表基础类定义
"""
import string
import random
import json
import re


def load_dict(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        tmp_str = f.read()
    tmp_str = re.sub(r'(\w+)(?=:)', r'"\1"', tmp_str)
    tmp_str = re.sub(r"'(.*?)'", r'"\1"', tmp_str)
    return json.loads(tmp_str)

def gen_name(length):
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for _ in range(length))
    return name


class Chart:
    """
    定义图表基础类
    """
    def __init__(self, chart_dict):
        """
        构造函数

        Parameters:
        -----------
        chart_dict : dict or str
            echarts配置信息: 若传文件路径 ，则读取对应文件的内容；否则直接将该信息作为内容
        """
        self.div_id = gen_name(10)
        json_cnt = json.dumps(chart_dict if type(chart_dict) == dict else load_dict(chart_dict))
        self.js_code = f"""
        var option_{self.div_id} = {json_cnt};
        var chart_{self.div_id} = echarts.init(document.getElementById('{self.div_id}'));
        option_{self.div_id} && chart_{self.div_id}.setOption(option_{self.div_id});
        """
        
    
    def get_div(self):
        """
        返回图表的DIV对象
        """
        return f"<div id='{self.div_id}' style='width: [w]px; height: [h]px'></div>"
    
    def get_script(self):
        """
        返回加载图表的JS代码
        """
        return self.js_code
