#!/usr/bin/env python
# -*- coding:utf-8 -*-

TEMP1 = """
<li class="items" style='padding:8px 0 0 %spx;'>
    <span class="folder" id='comment_folder_%s'>
        <div class="comment-L comment-L-top">
            <a href="#" class="icons zhan-ico"></a>
            <a href="/user/moyujian/submitted/1">
                <img src="/statics/images/1.jpg">
            </a>
        </div>
        <div class="comment-R comment-R-top" style="background-color: rgb(246, 246, 246);">
            <div class="pp">
                <a class="name" href="/user/moyujian/submitted/1">%s</a>
                <span class="p3">%s</span>
                <span class="into-time into-time-top">%s</span>
            </div>
            <div class="comment-line-top">
                <div class="comment-state">
                    <a class="ding" href="javascript:void(0);">
                        <b>顶</b>
                        <span class="ding-num">[0]</span>
                    </a>
                    <a class="cai" href="javascript:void(0);">
                        <b>踩</b>
                        <span class="cai-num">[0]</span>
                    </a>
                    <span class="line-huifu">|</span>
                    <a class="see-a jubao" href="javascript:void(0);">举报</a>
                    <span class="line-huifu">|</span>
                    <a class="see-a huifu-a" href="javascript:void(0);" onclick="reply(%s,%s,'%s')"  id='comment_reply_%s' >回复</a>
                </div>
            </div>
        </div>
    </span>

"""


def generate_comment_html(sub_comment_dic, margin_left_val):
    # html = '<ul style="background: url(&quot;/statics/images/pinglun_line.gif&quot;) 0px -10px no-repeat scroll transparent;margin-left:3px;">'
    html = '<ul>'
    for k, v_dic in sub_comment_dic.items():
        html += TEMP1 %(margin_left_val,k[0], k[3],k[1],k[4],k[7],k[0], k[3],k[0])
        if v_dic:
            html += generate_comment_html(v_dic, margin_left_val)
        html += "</li>"
    html += "</ul>"
    return html


def tree(self, comment_dic):
    html = ''
    for k, v in comment_dic.items():
        html += TEMP1 %(0,k[0], k[3],k[1],k[4],k[7],k[0], k[3],k[0])
        html += generate_comment_html(v, 16)
        html += "</li>"

    return html
