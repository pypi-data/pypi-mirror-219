# -*- coding: utf-8 -*-
# @FileName  :ableSci_checkin.py
# @Time      :2022/8/20 8:19
# @Author    :yaoys
# @Desc      :
import json
import os
import time

import requests
from requests.cookies import cookiejar_from_dict

from yaoys_checkin.checkin_util.checkin_log import get_checkin_logger
from yaoys_checkin.checkin_util.logutil import log_info
from yaoys_checkin.model.all_class_parent import allClassParent

checkin_header = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.ablesci.com/',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'pragma': 'no-cache'
}


class ableSci(allClassParent):

    def __init__(self, **kwargs):
        super(ableSci, self).__init__(**kwargs)

        if self.logger is None:
            self.logger, log_config = get_checkin_logger(config_file=self.config_file, log_name=str(os.path.basename(__file__)).split('.')[0])

        self.session = None

        self.checkin_message, self.is_success = self.able_sci_sign()

    # def __able_sci_checkin(self):
    #     checkin_url = "https://www.ablesci.com/user/sign"
    #     checkin_query = """
    #             (function (){
    #                 var request = new XMLHttpRequest();
    #                 request.open("GET","%s",false);
    #                 request.setRequestHeader('accept', 'application/json, text/javascript, */*; q=0.01');
    #                 request.setRequestHeader('x-requested-with', 'XMLHttpRequest');
    #                 request.setRequestHeader('sec-ch-ua-mobile', '?0');
    #                 request.setRequestHeader('sec-ch-ua-platform', "Windows");
    #                 request.setRequestHeader('sec-fetch-site', 'same-origin');
    #                 request.setRequestHeader('sec-fetch-mode', 'cors');
    #                 request.setRequestHeader('sec-fetch-dest', 'empty');
    #                 request.setRequestHeader('referer', 'https://www.ablesci.com/');
    #                 request.setRequestHeader('accept-encoding', 'gzip, deflate, br');
    #                 request.setRequestHeader('accept-language', 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7');
    #                 request.setRequestHeader('cache-control', 'no-cache');
    #                 request.setRequestHeader('pragma', 'no-cache');
    #                 request.send();
    #                 return request;
    #         })();
    #         """ % checkin_url
    #     checkin_query = checkin_query.replace("\n", "")
    #     resp = self.driver.execute_script("return " + checkin_query)
    #     resp = json.loads(resp["response"])
    #     code = -1
    #     msg = ''
    #     signcount = 0
    #     signpoint = 0
    #     code = resp['code']
    #     msg = resp['msg']
    #     if 'data' in resp:
    #         signcount = resp['data']['signcount']
    #         signpoint = resp['data']['signpoint']
    #
    #     return code, msg, signcount, signpoint

    # def able_sci(self):
    #     if self.cookie is None:
    #         raise Exception('The cookie is None')
    #
    #     if self.driver is None:
    #         self.driver = get_driver()
    #
    #     # Load cookie
    #     self.driver.get("https://www.ablesci.com/")
    #
    #     if self.cookie.startswith("cookie:"):
    #         self.cookie = self.cookie[len("cookie:"):]
    #     cookie_dict = [
    #         {"name": x[:x.find('=')].strip(), "value": x[x.find('=') + 1:].strip()}
    #         for x in self.cookie.split(';')
    #     ]
    #
    #     self.driver.delete_all_cookies()
    #     for cookie in cookie_dict:
    #         self.driver.add_cookie({
    #             "domain": "www.ablesci.com",
    #             "name": cookie["name"],
    #             "value": cookie["value"],
    #             "path": "/",
    #         })
    #
    #     self.driver.get("https://www.ablesci.com/")
    #     WebDriverWait(self.driver, 240).until(
    #         lambda x: x.title != "Just a moment..."
    #     )
    #
    #     checkin_code, checkin_message, signcount, signpoint = self.__able_sci_checkin()
    #     message = 'The checkin code is ' + str(checkin_code) + ',the checkin message is ' + checkin_message
    #
    #     # if self.logger is not None:
    #     #     log_info(message, my_logger=self.logger)
    #     close_driver(driver=self.driver)
    #     return message

    def __able_sci_checkin_withoutDriver__(self):
        if self.cookie is None:
            raise Exception('The cookie is None')
        if self.cookie.startswith("cookie:"):
            self.cookie = self.cookie[len("cookie:"):]

        cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in self.cookie.split("; ")}

        self.session = requests.session()
        resp = self.session.get('https://www.ablesci.com/user/sign', cookies=cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True), headers=checkin_header)
        resp_json = json.loads(resp.text)
        signcount = 0
        signpoint = 0
        code = resp_json['code']
        msg = resp_json['msg']
        if 'data' in resp_json:
            signcount = resp_json['data']['signcount']
            signpoint = resp_json['data']['signpoint']

        message = '签到信息: ' + msg
        if signcount != 0 and signpoint != 0:
            message = message + ' 签到总天数: ' + str(signcount)
        return message

    def ablesci_checkin_main(self):
        if self.cookie is not None and len(self.cookie) > 0:
            account_checkin_message = self.__able_sci_checkin_withoutDriver__()
            # 存在账户签到信息，说明成功执行了签到
            if account_checkin_message is not None and len(account_checkin_message) > 0:
                log_info(f"[Ableaci_Account_{self.account_index}]:" + str(account_checkin_message), my_logger=self.logger)
                # self.checkin_message.append(f"[Ableaci_Account_{self.account_index}] checkin message:" + str(account_checkin_message) + "      \n")
        else:
            return ''
        return f"[Ableaci_Account_{self.account_index}] " + str(account_checkin_message) + "      \n"

    def able_sci_sign(self):

        if self.config is None or self.config == '':
            return ''.join(self.checkin_message), False
        try:
            # 科研通签到
            log_info('*******************************able_sci checkin*******************************', my_logger=self.logger)
            if isinstance(self.config, str) is True:
                self.cookie = self.config
                self.account_index = 1
                self.checkin_message.append(self.ablesci_checkin_main())
            elif isinstance(self.config, list) is True:
                for i in range(0, len(self.config)):
                    if isinstance(self.config[i], dict) is True:
                        self.cookie = self.config[i]['cookie']
                        self.account_index = i + 1
                        self.checkin_message.append(self.ablesci_checkin_main())
                    else:
                        log_info('able_sci config error', my_logger=self.logger)
                        self.checkin_message.append('able_sci config error')

                    if self.more_time_sleep > 0:
                        time.sleep(self.more_time_sleep)
            else:
                log_info('able_sci config error' + '    \n', my_logger=self.logger)
                self.checkin_message.append('able_sci config error' + '    \n')

            log_info('*******************************able_sci checkin complete*******************************', my_logger=self.logger)
            return ''.join(self.checkin_message), True
        except Exception as e:
            self.checkin_message.append('main function: able_sci checkin error, the error is ' + str(e) + '    \n')
            log_info('main function: able_sci checkin error, the error is ' + str(e) + '    \n', my_logger=self.logger)
            log_info('*******************************able_sci error*******************************', my_logger=self.logger)

        return ''.join(self.checkin_message), True
