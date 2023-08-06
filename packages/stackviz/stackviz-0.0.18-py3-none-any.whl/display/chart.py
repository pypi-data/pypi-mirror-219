"""
图表基础类定义
"""
import string
import random
import os


def generate_variable_name(length):
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for _ in range(length))
    return name


class Chart:
    """
    定义图表基础类
    """
    def __init__(self, js, div_id=None, ref: dict=None):
        """
        构造函数

        Parameters:
        -----------
        js : str
            js脚本信息：若传文件路径 ，则读取对应文件的内容；否则直接将该信息作为内容
        """
        if os.path.exists(js):
            with open(js, 'r', encoding='UTF-8') as js_file:
                self.js_code = js_file.read()
        else:
            self.js_code = js
        self.div_id = div_id if div_id is not None else generate_variable_name(10)
        self.ref = ref
    
    def get_div(self):
        """
        返回图表的DIV对象
        """
        return f"<div id='{self.div_id}' style='width: [w]px; height: [h]px'></div>"
    
    def get_script(self):
        """
        返回加载图表的JS代码
        """
        if self.ref:
            for key in self.ref:
                self.js_code = self.js_code.replace("${%s}" % key, str(self.ref[key]))
        return self.js_code.replace('${id}', self.div_id)
