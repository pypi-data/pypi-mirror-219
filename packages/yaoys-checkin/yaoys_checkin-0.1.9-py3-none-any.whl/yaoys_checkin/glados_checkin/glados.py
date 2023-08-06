# encoding=utf8
import json
import os

import requests
from requests.cookies import cookiejar_from_dict

from yaoys_checkin.checkin_util.logutil import log_info
from yaoys_checkin.checkin_util.checkin_log import get_checkin_logger
from yaoys_checkin.model.all_class_parent import allClassParent

sign_header = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-length': '26',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://glados.rocks',
    'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35'
}

status_header = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-length': '26',
    'content-type': 'application/json;charset=UTF-8',
    'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35'
}


class glados(allClassParent):
    def __init__(self, **kwargs):
        super(glados, self).__init__(**kwargs)
        if self.logger is None:
            self.logger, log_config = get_checkin_logger(config_file=self.config_file, log_name=str(os.path.basename(__file__)).split('.')[0])

        self.session = None
        self.checkin_url = "https://glados.rocks/api/user/checkin"
        self.status_url = "https://glados.rocks/api/user/status"
        self.checkin_message, self.is_success = self.glados_sign()

    # def glados_checkin(self):
    #     checkin_url = "https://glados.rocks/api/user/checkin"
    #     checkin_query = """
    #         (function (){
    #         var request = new XMLHttpRequest();
    #         request.open("POST","%s",false);
    #         request.setRequestHeader('content-type', 'application/json');
    #         request.send('{"token": "glados.network"}');
    #         return request;
    #         })();
    #         """ % checkin_url
    #     checkin_query = checkin_query.replace("\n", "")
    #     resp = self.driver.execute_script("return " + checkin_query)
    #     resp = json.loads(resp["response"])
    #     return resp["code"], resp["message"]
    #
    # def glados_status(self):
    #     status_url = "https://glados.rocks/api/user/status"
    #     status_query = """
    #         (function (){
    #         var request = new XMLHttpRequest();
    #         request.open("GET","%s",false);
    #         request.send(null);
    #         return request;
    #         })();
    #         """ % status_url
    #     status_query = status_query.replace("\n", "")
    #     resp = self.driver.execute_script("return " + status_query)
    #     resp = json.loads(resp["response"])
    #     return resp["code"], resp["data"]
    #
    # def glados(self):
    #     if self.cookie is None:
    #         raise Exception('The cookie is None')
    #
    #     if self.driver is None:
    #         driver = get_driver()
    #     # Load cookie
    #     self.driver.get("https://glados.rocks")
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
    #         if cookie["name"] in ["koa:sess", "koa:sess.sig"]:
    #             self.driver.add_cookie({
    #                 "domain": "glados.rocks",
    #                 "name": cookie["name"],
    #                 "value": cookie["value"],
    #                 "path": "/",
    #             })
    #
    #     self.driver.get("https://glados.rocks")
    #     WebDriverWait(self.driver, 240).until(
    #         lambda x: x.title != "Just a moment..."
    #     )
    #
    #     checkin_code, checkin_message = self.glados_checkin()
    #     if checkin_code == -2:
    #         checkin_message = "Login fails, please check your cookie."
    #     if self.logger is not None:
    #         log_info(f"[Checkin] {checkin_message}", my_logger=self.logger)
    #
    #     message = ''
    #     if checkin_code != -2:
    #         status_code, status_data = self.glados_status()
    #         left_days = int(float(status_data["leftDays"]))
    #
    #         if self.logger is not None:
    #             log_info(f"[Status] Left days:{left_days}", my_logger=self.logger)
    #         message = 'CheckIn time:' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ', Checkin message:' + checkin_message + ', Status: Left days ' + str(left_days)
    #     else:
    #         message = 'The account login fails, please check your cookie. '
    #
    #     close_driver(driver=self.driver)
    #
    #     return message

    def __glados_checkin_without_driver__(self):
        if self.cookie is None:
            raise Exception('The cookie is None')
        if self.cookie.startswith("cookie:"):
            self.cookie = self.cookie[len("cookie:"):]

        cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in self.cookie.split("; ")}
        self.session = requests.session()
        data = {"token": "glados.network"}
        checkin_resp = self.session.post(url=self.checkin_url, cookies=cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True),
                                         headers=sign_header, timeout=20, json=data)
        checkin_resp_json = json.loads(checkin_resp.text)
        checkin_code = checkin_resp_json["code"]
        if checkin_code == -2:
            checkin_message = "Login fails, please check your cookie."
            return checkin_message

        checkin_message = checkin_resp_json["message"]
        if 'Please Try Tomorrow' == checkin_message:
            checkin_message = '今日已签到，请明日再执行签到'
        status_resp = self.session.get(self.status_url, cookies=cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True), headers=status_header, timeout=20, json=data)
        status_resp_json = json.loads(status_resp.text)
        status_code = status_resp_json["code"]
        status_message = status_resp_json["data"]
        left_days = int(float(status_message["leftDays"]))

        message = f'签到信息: {checkin_message}, 账户剩余天数: {left_days}'
        return message

    def glados_main(self):
        # gloads 执行签到
        if self.cookie is not None and len(self.cookie) > 0:
            account_checkin_message = self.__glados_checkin_without_driver__()
            # 存在账户签到信息，说明成功执行了签到
            if account_checkin_message is not None and len(account_checkin_message) > 0:
                log_info(f"[Gloads_Account_{self.account_index}]:" + str(account_checkin_message), my_logger=self.logger)
                self.checkin_message.append(f"[Gloads_Account_{self.account_index}] :" + account_checkin_message + "    \n")

        return self.checkin_message

    def glados_sign(self):
        if self.config is None or self.config == '':
            return ''.join(self.checkin_message), False
        try:
            # 如果是字符串，说明是单个cookie
            if self.config is not None and len(self.config) > 0:
                log_info('*******************************glados checkin*******************************', my_logger=self.logger)
                if isinstance(self.config, str) is True:
                    self.cookie = self.config
                    self.account_index = 1
                    self.checkin_message = self.glados_main()
                elif isinstance(self.config, list) is True:
                    for i in range(0, len(self.config)):
                        if isinstance(self.config[i], dict) is True:
                            self.cookie = self.config[i]['cookie']
                            self.account_index = i + 1
                            self.checkin_message = self.glados_main()
                        else:
                            log_info('glados config error' + '    \n', my_logger=self.logger)
                            self.checkin_message.append('glados config error' + '    \n')
                else:
                    log_info('glados config error' + '    \n', my_logger=self.logger)
                    self.checkin_message.append('glados config error' + '    \n')
                log_info('*******************************glados checkin complete*******************************', my_logger=self.logger)
                return ''.join(self.checkin_message), True
        except Exception as e:
            self.checkin_message.append('main function: gloads checkin error, the error is ' + str(e) + '    \n')
            log_info('main function: gloads checkin error, the error is ' + str(e) + '    \n', my_logger=self.logger)
            log_info('*******************************glados error*******************************', my_logger=self.logger)

            return ''.join(self.checkin_message), False
