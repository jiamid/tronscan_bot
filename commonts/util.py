# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 15:29
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : util.py
# @Software: PyCharm

def to_escape_string(string):
    string = str(string)
    return string.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]").replace("(",
                                                                                                          "\\(").replace(
        ")", "\\)").replace("~", "\\~").replace("`", "\\`").replace(">", "\\>").replace("#", "\\#").replace("+",
                                                                                                            "\\+").replace(
        "-", "\\-").replace("=", "\\=").replace("|", "\\|").replace("{", "\\{").replace("}", "\\}").replace(".",
                                                                                                            "\\.").replace(
        "!", "\\!")
