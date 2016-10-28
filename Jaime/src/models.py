#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import pickle
from config import settings
from src import identifier


class BaseModel:
    def save(self):
        """
        使用pickle将用户对象保存到文件
        :return:
        """
        nid = str(self.nid)
        file_path = os.path.join(self.db_path, nid)
        pickle.dump(self, open(file_path, 'wb'))


class Admin(BaseModel):
    db_path = settings.ADMIN_DB

    def __init__(self, username, password):
        """
        创建管理员对象
        :param username:
        :param password:
        :return:
        """
        self.nid = identifier.AdminNid(Admin.db_path)
        self.username = username
        self.password = password
        self.create_time = time.strftime('%Y-%m-%d')

    @staticmethod
    def login(user, pwd):
        """
        管理员登陆
        :param user: 管理员用户名
        :param pwd: 管理员密码
        :return: 如果登陆成功，获取管理员对象，否则 None
        """


class School(BaseModel):
    db_path = settings.SCHOOL_DB

    def __init__(self, name):
        self.nid = identifier.SchoolNid(School.db_path)
        self.schoolName = name
        self.income = 0

    def __str__(self):
        return self.schoolName

    @staticmethod
    def get_all_list():
        ret = []
        for item in os.listdir(os.path.join(School.db_path)):
            obj = pickle.load(open(os.path.join(School.db_path, item), 'rb'))
            ret.append(obj)
        return ret


class Teacher(BaseModel):
    db_path = settings.TEACHER_DB

    def __init__(self, name, level):
        """
        :param name: 老师姓名
        :param level: 老师级别
        """

        self.nid = identifier.TeacherNid(Teacher.db_path)
        self.teacherName = name
        self.teacherLevel = level
        self.__account = 0


class Course(BaseModel):
    db_path = settings.COURSE_DB

    def __init__(self, name, price, period, school_id):
        """
        :param name: 课程名
        :param price: 课程价格
        :param period: 课程周期
        :param school_id: 关联学校Id，学校ID具有get_obj_by_uuid方法，以此获取学校对象（其中包含学校信息）
        """
        self.nid = identifier.CourseNid(Course.db_path)
        self.courseName = name
        self.coursePrice = price
        self.coursePeriod = period
        self.schoolId = school_id

    def __str__(self):
        return "课程名：%s；课程价格：%s；课程周期：%s；所属学校：%s" % (
            self.courseName, self.coursePrice, self.coursePeriod, self.schoolId.get_obj_by_uuid().name, )

    @staticmethod
    def get_all_list():
        """
        获取所有课程对象
        """
        ret = []
        for item in os.listdir(os.path.join(Course.db_path)):
            obj = pickle.load(open(os.path.join(Course.db_path, item), 'rb'))
            ret.append(obj)
        return ret


class CourseToTeacher(BaseModel):
    db_path = settings.COURSE_TO_TEACHER_DB

    def __init__(self, course_id, teacher_id):
        self.nid = identifier.CourseToTeacherNid(CourseToTeacher.db_path)
        self.courseId = course_id
        self.teacherId = teacher_id


    @staticmethod
    def course_teacher_list():
        pass


class Classes(BaseModel):
    db_path = settings.CLASSES_DB

    def __init__(self, name, tuition, school_id, course_to_teacher_list):
        self.nid = identifier.ClassesNid(Classes.db_path)
        self.name = name
        self.tuition = tuition
        self.schoolId = school_id
        self.courseToTeacherList = course_to_teacher_list


class Score:
    """
    成绩单
    """

    def __init__(self, student_id):
        self.studentId = student_id
        self.score_dict = {}

    def set(self, course_to_teacher_nid, number):
        self.score_dict[course_to_teacher_nid] = number

    def get(self, course_to_teacher_nid):
        return self.score_dict.get(course_to_teacher_nid, None)


class Student(BaseModel):
    db_path = settings.ADMIN_DB

    def __init__(self, name, age, classes_id):
        self.nid = identifier.StudentNid(Student.db_path)
        self.name = name
        self.age = age
        self.classesId = classes_id
        self.transcript = Score(self.nid)

    @staticmethod
    def register():
        pass



