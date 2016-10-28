#!/usr/bin/env python
# -*- coding:utf-8 -*-

CURRENT_USER_OBJECT = None
from src.models import School
from src.models import Course


def create_school():
    """
    创建学校
    :return:
    """
    name = input('请输入学校名称：')
    obj = School(name)
    obj.save()


def show_school():
    print('======学校======')
    school_list = School.get_all_list()
    for obj in school_list:
        print(obj)


def create_teacher():
    """
    创建老师
    :return:
    """


def create_course():
    """
    创建课程
    :return:
    """
    print('======创建学校======')

    school_list = School.get_all_list()
    for k, obj in enumerate(school_list, 1):
        print(k, obj)
    sid = input('请选择学校:')
    sid = int(sid)
    school_obj = school_list[sid - 1]

    name = input('请输入课程名称：')
    price = input('请输入课程价格：')
    period = input('请输入课程周期：')

    obj = Course(name, price, period, school_obj.nid)
    obj.save()
    print('课程【%s】创建成功' % name)


def show_course():
    print('=====查看课程=====')
    course_list = Course.get_all_list()
    for item in course_list:
        print(item.courseName, item.coursePrice, item.coursePeriod, item.schoolId.get_obj_by_uuid())


def create_course_teacher():
    """
    为课程分配老师
    :return:
    """


def create_class():
    """
    创建班级
    """


def show_choice():
    show = """
        1. 创建学校
        2. 查看学校
        3. 创建老师
        4. 创建课程
        5. 查看课程
        6. 创建老师课程对应关系
        7. 创建班级
    """
    print(show)


def main():
    choice_dict = {
        '0': show_choice,
        '1': create_school,
        '2': show_school,
        '3': create_teacher,
        '4': create_course,
        '5': show_course,
        '6': create_course_teacher,
        '7': create_class,
    }
    show_choice()
    while True:
        inp = input('请输入选项：')
        if inp not in choice_dict:
            print('选项错误，请重新选择')
            continue
        func = choice_dict[inp]
        result = func()