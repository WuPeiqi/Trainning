#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import os


class Field:

    def __init__(self):

        self.is_valid = False
        self.name = None
        self.value = None
        self.error = None

    def match(self, name, value):
        self.name = name

        if not self.required:
            self.is_valid = True
            self.value = value
        else:
            if not value:
                if self.custom_error_dict.get('required', None):
                    self.error = self.custom_error_dict['required']
                else:
                    self.error = "%s is required" % name
            else:
                ret = re.match(self.REGULAR, value)
                if ret:
                    self.is_valid = True
                    self.value = value
                else:
                    if self.custom_error_dict.get('valid', None):
                        self.error = self.custom_error_dict['valid']
                    else:
                        self.error = "%s is invalid" % name


class StringField(Field):

    REGULAR = "^.*$"

    def __init__(self, custom_error_dict=None, required=True):

        self.custom_error_dict = {}  # {'required': 'IP不能为空', 'valid': 'IP格式错误'}
        if custom_error_dict:
            self.custom_error_dict.update(custom_error_dict)

        self.required = required

        super(StringField, self).__init__()


class IPField(Field):

    REGULAR = "^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$"

    def __init__(self, custom_error_dict=None, required=True):

        self.custom_error_dict = {}  # {'required': 'IP不能为空', 'valid': 'IP格式错误'}
        if custom_error_dict:
            self.custom_error_dict.update(custom_error_dict)

        self.required = required
        super(IPField, self).__init__()


class EmailField(Field):

    REGULAR = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"

    def __init__(self, custom_error_dict=None, required=True):

        self.custom_error_dict = {}  # {'required': 'IP不能为空', 'valid': 'IP格式错误'}
        if custom_error_dict:
            self.custom_error_dict.update(custom_error_dict)

        self.required = required
        super(EmailField, self).__init__()


class IntegerField(Field):

    REGULAR = "^\d+$"

    def __init__(self, custom_error_dict=None, required=True):

        self.custom_error_dict = {}  # {'required': 'IP不能为空', 'valid': 'IP格式错误'}
        if custom_error_dict:
            self.custom_error_dict.update(custom_error_dict)

        self.required = required
        super(IntegerField, self).__init__()


class CheckBoxField(Field):

    REGULAR = "^\d+$"

    def __init__(self, custom_error_dict=None, required=True):

        self.custom_error_dict = {}  # {'required': 'IP不能为空', 'valid': 'IP格式错误'}
        if custom_error_dict:
            self.custom_error_dict.update(custom_error_dict)

        self.required = required
        super(CheckBoxField, self).__init__()

    def match(self, name, value):
        self.name = name

        if not self.required:
            self.is_valid = True
            self.value = value
        else:
            if not value:
                if self.custom_error_dict.get('required', None):
                    self.error = self.custom_error_dict['required']
                else:
                    self.error = "%s is required" % name
            else:
                if isinstance(name, list):
                    self.is_valid = True
                    self.value = value
                else:
                    if self.custom_error_dict.get('valid', None):
                        self.error = self.custom_error_dict['valid']
                    else:
                        self.error = "%s is invalid" % name


class FileField(Field):

    REGULAR = "^(\w+\.pdf)|(\w+\.mp3)|(\w+\.py)$"

    def __init__(self, custom_error_dict=None, required=True):

        self.custom_error_dict = {}  # {'required': 'IP不能为空', 'valid': 'IP格式错误'}
        if custom_error_dict:
            self.custom_error_dict.update(custom_error_dict)

        self.required = required

        super(FileField, self).__init__()

    def match(self, name, file_name_list):
        flag = True
        self.name = name

        if not self.required:
            self.is_valid = True
            self.value = file_name_list
        else:
            if not file_name_list:
                if self.custom_error_dict.get('required', None):
                    self.error = self.custom_error_dict['required']
                else:
                    self.error = "%s is required" % name
                flag = False
            else:
                for file_name in file_name_list:
                    if not file_name or not file_name.strip():
                        if self.custom_error_dict.get('required', None):
                            self.error = self.custom_error_dict['required']
                        else:
                            self.error = "%s is required" % name
                        flag = False
                        break
                    else:
                        ret = re.match(self.REGULAR, file_name)
                        if not ret:
                            if self.custom_error_dict.get('valid', None):
                                self.error = self.custom_error_dict['valid']
                            else:
                                self.error = "%s is invalid" % name
                            flag = False
                            break

            self.is_valid = flag

    def save(self, request, upload_to=""):

        file_metas = request.files[self.name]
        for meta in file_metas:
            file_name = meta['filename']
            file_path_name = os.path.join(upload_to, file_name)
            with open(file_path_name, 'wb') as up:
                up.write(meta['body'])

        upload_file_path_list = map(lambda path: os.path.join(upload_to, path), self.value)
        self.value = list(upload_file_path_list)


