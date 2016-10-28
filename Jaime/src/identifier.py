#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pickle
from lib import commons


class Nid:
    def __init__(self, role, db_path):
        """
        该对象用于标识唯一ID
        :param role: 角色：school,teacher,
        :return:
        """
        role_list = [
            'admin', 'school', 'teacher', 'course', 'course_to_teacher', 'classes', 'student'
        ]
        if role not in role_list:
            raise Exception('用户角色定义错误，选项为：%s' % ','.join(role_list))
        self.role = role
        self.uuid = commons.create_uuid()
        self.db_path = db_path

    def __str__(self):
        return self.uuid

    def get_obj_by_uuid(self):
        """
        获取当前id对应的对象
        :return:
        """
        for name in os.listdir(os.path.join(self.db_path)):
            if name == self.uuid:
                return pickle.load(open(os.path.join(self.db_path, self.uuid),'rb'))


class AdminNid(Nid):
    def __init__(self, db_path):
        super(AdminNid, self).__init__('admin', db_path)


class SchoolNid(Nid):
    def __init__(self, db_path):
        super(SchoolNid, self).__init__('school', db_path)


class TeacherNid(Nid):
    def __init__(self, db_path):
        super(TeacherNid, self).__init__('teacher', db_path)


class CourseNid(Nid):
    def __init__(self, db_path):
        super(CourseNid, self).__init__('course', db_path)


class CourseToTeacherNid(Nid):
    def __init__(self, db_path):

        super(CourseToTeacherNid, self).__init__('course_to_teacher', db_path)

    def get_course_teacher_by_uuid(self):
        """
        获取课程对象和老师对象
        :return:
        """
        for name in os.listdir(os.path.join(self.db_path)):
            if name == self.uuid:
                obj = pickle.load(os.path.join(self.db_path, self.uuid))
                return [obj.courseId.get_obj_by_uuid(), obj.teacherId.get_obj_by_uuid(), ]
        return [None, None]


class ClassesNid(Nid):
    def __init__(self, db_path):
        super(ClassesNid, self).__init__('classes', db_path)


class StudentNid(Nid):
    def __init__(self, db_path):
        super(StudentNid, self).__init__('student', db_path)


