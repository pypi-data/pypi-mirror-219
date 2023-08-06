"""
操作主类
"""
from .layout import LayOut
from .chart import Chart
from IPython.display import display, HTML
import os


class Stack:
    """
    实现 stackviz 的主类
    """
    def __init__(self, rows_span=None, cols_span=None, css=''):
        """
        构造函数

        Parameters:
        -----------
        css : str
            css信息：若传文件路径 ，则读取对应文件的内容；否则直接将该信息作为内容
        """
        if os.path.exists(css):
            with open(css, 'r', encoding='utf-8') as css_file:
                self.css = css_file.read()
        else:
            self.css = css
        with open(os.path.join(os.path.dirname(__file__), '../resources/template.tpl'), "r", encoding="UTF-8") as tpl_file:
            self.html = tpl_file.read()
        self.html = self.html.replace("${style}", css)
        self.rows_span = rows_span
        self.cols_span = cols_span
        self.layout = LayOut(rows_span, cols_span)
        self.layout_settings = []
        self.scripts = []
        
    def add_layout(self, row, col, layout_object: LayOut):
        self.layout_settings.append((row, col, layout_object.html))
        
    def add_chart(self, row, col, chart_object: Chart):
        w = str(self.rows_span[col - 1])
        h = str(self.cols_span[row - 1])
        self.layout_settings.append((row, col, chart_object.get_div().replace('[w]',w).replace('[h]',h)))
        self.scripts.append(chart_object.get_script())
        
    def add_text(self, row, col, text):
        self.layout_settings.append((row, col, text))
        
    def show_chart(self, chart_object: Chart, w, h):
        display(HTML(
            self.html.replace("${body}",chart_object.get_div().replace('[w]',str(w)).replace('[h]',str(h))).\
                      replace("${script}", chart_object.get_script())
        ))
        
    def show(self):
        self.layout.load(self.layout_settings)
        display(HTML(
            self.html.replace("${body}", self.layout.html).\
                      replace("${script}","\n\n".join(self.scripts))
        ))
