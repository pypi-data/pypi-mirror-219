# -*- coding: utf-8 -*-
# @FileName  :gufen_checkin.py
# @Time      :2022/12/30 12:22
# @Author    :yaoys
# @Desc      :
import os
import time

import requests
import urllib3
from bs4 import BeautifulSoup

from yaoys_checkin.checkin_util.logutil import log_info
from yaoys_checkin.checkin_util.checkin_log import get_checkin_logger
from yaoys_checkin.model.all_class_parent import allClassParent


class gufenxueshu(allClassParent):
    def __init__(self, **kwargs):
        super(gufenxueshu, self).__init__(**kwargs)

        self.__gufen_checkin_url = 'http://bbs.99lb.net/plugin.php?id=are_sign:getaward&typeid=1'

        if self.logger is None:
            self.logger, log_config = get_checkin_logger(config_file=self.config_file, log_name=str(os.path.basename(__file__)).split('.')[0])

        self.checkin_message, self.is_success = self.gufen_sign()

    def __get_header(self):
        header = {
            'Host': 'bbs.99lb.net',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://bbs.99lb.net/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': self.cookie,
            'Connection': 'keep-alive',
        }
        return header

    # 解决出现警告 Adding certificate verification is strongly advised.
    urllib3.disable_warnings()

    def __gufen_checkin(self):
        header = self.__get_header()
        resp = requests.get(url=self.__gufen_checkin_url, headers=header, verify=False)
        resp_code = resp.status_code
        checkin_message = ''
        if resp_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            result = soup.find_all('div', attrs={'id': 'messagetext'})
            for res in result:
                checkin_message = res.find_next(name='p').text
                break
        else:
            checkin_message = 'checkin error,the status code is ' + str(resp_code)
        resp.close()
        return checkin_message

    def gufen_checkin_main(self):
        if self.cookie is not None and len(self.cookie) > 0:
            account_checkin_message = self.__gufen_checkin()
            # 存在账户签到信息，说明成功执行了签到
            if account_checkin_message is not None and len(account_checkin_message) > 0:
                log_info(f"[gufen_Account_{self.account_index}]:" + str(account_checkin_message), my_logger=self.logger)
                self.checkin_message.append(f"[gufen_Account_{self.account_index}] :" + str(account_checkin_message) + "      \n")
        return self.checkin_message

    def gufen_sign(self):
        if self.config is None or self.config == '':
            return ''.join(self.checkin_message), False

        try:
            # 谷粉学术签到
            log_info('*******************************gufen checkin*******************************', my_logger=self.logger)
            if isinstance(self.config, str) is True:
                self.cookie = self.config
                self.account_index = 1
                self.checkin_message = self.gufen_checkin_main()
            elif isinstance(self.config, list) is True:
                for i in range(0, len(self.config)):
                    if isinstance(self.config[i], dict) is True:
                        self.cookie = self.config[i]['cookie']
                        self.account_index = i + 1
                        self.checkin_message = self.gufen_checkin_main()
                    else:
                        log_info('gufen config error' + '    \n', my_logger=self.logger)
                        self.checkin_message.append('gufen config error' + '    \n')

                    if self.more_time_sleep > 0:
                        time.sleep(self.more_time_sleep)
            else:
                log_info('gufen config error' + '    \n', my_logger=self.logger)
                self.checkin_message.append('gufen config error' + '    \n')
            log_info('*******************************gufen checkin complete*******************************', my_logger=self.logger)
            return ''.join(self.checkin_message), True
        except Exception as e:
            self.checkin_message.append('main function: gufenxueshu checkin error, the error is ' + str(e) + '    \n')
            log_info('main function: gufenxueshu checkin error, the error is ' + str(e) + '    \n', my_logger=self.logger)
            log_info('*******************************gufen error*******************************', my_logger=self.logger)
            return ''.join(self.checkin_message), False
