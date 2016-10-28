#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

TEMP1 = """
<div class='content' style='margin-left:%s;'>
    <span>%s</span>
"""


def generate_comment_html(sub_comment_dic, margin_left_val):
    html = '<div class="comment">'
    for k, v_dic in sub_comment_dic.items():
        html += TEMP1 % (margin_left_val, k[1])
        if v_dic:
            html += generate_comment_html(v_dic, margin_left_val)
        html += "</div>"
    html += "</div>"
    return html


@register.simple_tag
def tree(comment_dic):
    html = '<div class="comment">'
    for k, v in comment_dic.items():
        html += TEMP1 % (0, k[1])
        html += generate_comment_html(v, 30)
        html += "</div>"
    html += '</div>'

    return mark_safe(html)


