# -*- coding: utf-8 -*-
# @FileName  :allClassParent.py
# @Time      :2023/4/16 21:57
# @Author    :yaoys
# @Desc      :

class allClassParent(object):
    def __init__(self, **kwargs):
        self.cookie = kwargs.get('cookie', None)
        # self.driver = kwargs.get('driver', None)
        self.logger = kwargs.get('logger', None)
        self.checkin_message = kwargs.get('checkin_message', [])
        self.account_index = kwargs.get('account_index', 1)
        self.config = kwargs.get('config', None)
        self.refresh_token = kwargs.get('refresh_token', None)
        self.phone = kwargs.get('phone', None)
        self.password = kwargs.get('password', None)
        self.judge_args = True
        self.is_success = True
        self.config_file = kwargs.get('config_file', None)
        self.more_time_sleep = kwargs.get('more_time_sleep', 0)

    def get_checkin_status(self):
        return self.checkin_message, self.is_success
