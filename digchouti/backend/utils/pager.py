#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Pagination:
    def __init__(self, current_page, all_item):
        try:
            page = int(current_page)
        except:
            page = 1
        if page < 1:
            page = 1

        all_pager, c = divmod(all_item, 10)
        if c > 0:
            all_pager += 1

        self.current_page = page
        self.all_pager = all_pager

    @property
    def start(self):
        return (self.current_page - 1) * 10

    @property
    def end(self):
        return self.current_page * 10

    def string_pager(self, base_url="/index/"):
        list_page = []
        if self.all_pager < 11:
            s = 1
            t = self.all_pager + 1
        else:  # 总页数大于11
            if self.current_page < 6:
                s = 1
                t = 12
            else:
                if (self.current_page + 5) < self.all_pager:
                    s = self.current_page - 5
                    t = self.current_page + 5 + 1
                else:
                    s = self.all_pager - 11
                    t = self.all_pager + 1
        # 首页
        # first = '<a href="%s1">首页</a>' % base_url
        # list_page.append(first)
        # 上一页
        # 当前页 page
        if self.current_page == 1:
            prev = '<a href="javascript:void(0);">上一页</a>'
        else:
            prev = '<a href="%s%s">上一页</a>' % (base_url, self.current_page - 1,)
        list_page.append(prev)

        for p in range(s, t):  # 1-11
            if p == self.current_page:
                temp = '<a class="active" href="%s%s">%s</a>' % (base_url,p, p)
            else:
                temp = '<a href="%s%s">%s</a>' % (base_url,p, p)
            list_page.append(temp)
        if self.current_page == self.all_pager:
            nex = '<a href="javascript:void(0);">下一页</a>'
        else:
            nex = '<a href="%s%s">下一页</a>' % (base_url, self.current_page + 1,)

        list_page.append(nex)

        # 尾页
        # last = '<a href="%s%s">尾页</a>' % (base_url, self.all_pager,)
        # list_page.append(last)

        # 跳转
        # jump = """<input type='text' /><a onclick="Jump('%s',this);">GO</a>""" % ('/index/', )
        # script = """<script>
        #     function Jump(baseUrl,ths){
        #         var val = ths.previousElementSibling.value;
        #         if(val.trim().length>0){
        #             location.href = baseUrl + val;
        #         }
        #     }
        #     </script>"""
        # list_page.append(jump)
        # list_page.append(script)
        str_page = "".join(list_page)
        return str_page

