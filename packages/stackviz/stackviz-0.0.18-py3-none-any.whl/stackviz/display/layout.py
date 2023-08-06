"""
布局类定义
"""

class LayOut:
    """
    布局基础类
    """
    def __init__(self, w_multi, h_multi, css_class="Nikf092"):
        self.width_group  = w_multi
        self.height_group = h_multi
        self.css_class = css_class
        self.html = None

    def load(self, loc_htmls: list=None):
        """
        加载布局元素

        Parameters:
        -----------
        loc_htmls : list
            布局信息：(row_seq, col_seq, html),(row_seq, col_seq, html)]
        """
        tab_html = f"<table class='{self.css_class}'>"
        for r_i, h_val in enumerate(self.height_group):
            row_html = f"<tr height={h_val}>"
            for c_i, w_val in enumerate(self.width_group):
                insert_html = ""
                if loc_htmls:
                    for e in loc_htmls:
                        if r_i+1 == e[0] and c_i +1 == e[1]:
                            insert_html = e[2]
                row_html += f"<td width={w_val}>{insert_html}</td>"
            row_html += "</tr>"
            tab_html += row_html
        self.html = tab_html + "</table>"
