"""
操作主类
"""
from .chart import Chart
from IPython.display import display, HTML
import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Stack:
    """
    实现 stackviz 的主类
    """
    def __init__(self, rows_span=None, cols_span=None, css='', class_name='main_tab'):
        """
        构造函数

        Parameters:
        -----------
        rows_span: 定义 各行的高度
        cols_span: 定义 各列的宽度
        css : str
            css信息: 若传文件路径 ，则读取对应文件的内容；否则直接将该信息作为内容
        class_name: 自定义 table 样式的 class名称, 用于自定义样式表
        """
        if os.path.exists(css):
            with open(css, 'r', encoding='utf-8') as css_file:
                self.css = css_file.read()
        else:
            self.css = css
        if len(self.css) == 0:
            self.css = """
                .%s {
                    display: flex;
                    justify-content: center;
                }

                .%s table{
                    border-collapse: collapse;
                    border-spacing: 0;
                    margin-bottom: 0px;
                }

                .%s th, .%s td {
                    border: 1px solid #ddd;
                    padding: 0px;
                    text-align: center !important;
                    vertical-align: middle !important;
                }

                .%s th {
                    font-weight: 600;
                    background-color: #f6f6f6;
                }
            """ % (class_name, class_name, class_name, class_name, class_name)
        with open(os.path.join(parent_directory, 'resources/echarts.min.js'), "r", encoding="UTF-8") as echarts_file:
            self.echarts_js = echarts_file.read()
        with open(os.path.join(parent_directory, 'resources/template.tpl'), "r", encoding="UTF-8") as tpl_file:
            self.html = tpl_file.read()
        self.s_html = ""
        self.rows_span = rows_span
        self.cols_span = cols_span
        self.class_name = class_name
        self.layout_settings = []
        self.scripts = []

    def __load(self):
        """
        加载布局元素

        Parameters:
        -----------
        loc_htmls : list
            布局信息：(row_seq, col_seq, html),(row_seq, col_seq, html)]
        """
        tab_html = f"<table class='{self.class_name}'>"
        for r_i, h_val in enumerate(self.cols_span):
            row_html = f"<tr height={h_val}>"
            for c_i, w_val in enumerate(self.rows_span):
                insert_html = ""
                if len(self.layout_settings) > 0:
                    for e in self.layout_settings:
                        if r_i+1 == e[0] and c_i +1 == e[1]:
                            insert_html = e[2]
                row_html += f"<td width={w_val}>{insert_html}</td>"
            row_html += "</tr>"
            tab_html += row_html
        self.s_html = tab_html + "</table>"
        
    def add_stack(self, row, col, stack_object: 'Stack'):
        stack_object.__load()
        self.layout_settings.append((row, col, stack_object.s_html))
        self.scripts.extend(stack_object.scripts)
        
    def add_chart(self, row, col, chart_object: Chart):
        w = str(self.rows_span[col - 1])
        h = str(self.cols_span[row - 1])
        self.layout_settings.append((row, col, chart_object.get_div().replace('[w]',w).replace('[h]',h)))
        self.scripts.append(chart_object.get_script())
        
    def add_text(self, row, col, text):
        self.layout_settings.append((row, col, text))

    def __display_html(self, content):
        current_dir = os.getcwd()
        target_file = os.path.join(current_dir, 'stackviz.html')
        if os.path.exists(target_file):
            os.remove(target_file)
        with open(target_file, 'w', encoding='utf-8') as temp_file:
            temp_file.write(content)
        # TODO: 当前仅支持从工作目录根目录访问 ，不支持从子级目录访问 
        return """
            <style>
                /* 设置容器 div 的宽度和高度 */
                .iframe-container {
                width: 100%;
                height: 0;
                padding-bottom: 56.25%; /* 设置宽高比为 16:9，如果需要其他比例，可以调整此值 */
                position: relative;
                }

                /* 设置 iframe 的样式 */
                .iframe-container iframe {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                }
            </style>
            <div class="iframe-container">
                <iframe src="[link]" frameborder="0" allowfullscreen></iframe>
            </div>
        """.replace('[link]', '/files/stackviz.html')

    def show_chart(self, chart_object: Chart, w, h):
        if '${echarts}' in self.html:
            self.html = self.html.replace('${echarts}', self.echarts_js)
        display(HTML(self.__display_html(
            self.html.replace("${body}",chart_object.get_div().replace('[w]',str(w)).replace('[h]',str(h))).\
                      replace("${script}", chart_object.get_script())
        )))
        
    def show(self):
        if '${echarts}' in self.html:
            self.html = self.html.replace('${echarts}', self.echarts_js)
        if '${style}' in self.html:
            self.html = self.html.replace("${style}", self.css)
        self.__load()
        display(HTML(self.__display_html(
            self.html.replace("${body}", self.s_html).\
                      replace("${script}","\n\n".join(self.scripts))
        )))
