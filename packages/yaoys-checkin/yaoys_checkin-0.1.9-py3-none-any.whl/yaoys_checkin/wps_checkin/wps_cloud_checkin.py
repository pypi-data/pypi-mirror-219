# encoding=utf8
import json
import os

import requests
from requests.cookies import cookiejar_from_dict

from yaoys_checkin.checkin_util.logutil import log_info
from yaoys_checkin.checkin_util.checkin_log import get_checkin_logger
from yaoys_checkin.model.all_class_parent import allClassParent

cloud_header = {

    'content-length': '10',
    'accept': '*/*',
    'content-type': 'application/x-www-form-urlencoded',
    'csrf-token': '3dEhhfhdXZiqDlQ7ttrTiQZ7YZP27jkQ',
    'origin': 'https://zt.wps.cn',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://zt.wps.cn/spa/2019/vip_mobile_sign_v2/?csource=pc_cloud_membercenter&position=pc_cloud_sign',
    'accept-encoding': 'gzip, deflate, br',
}


class wps_cloud(allClassParent):
    def __init__(self, **kwargs):
        super(wps_cloud, self).__init__(**kwargs)
        if self.logger is None:
            self.logger, log_config = get_checkin_logger(config_file=self.config_file, log_name=str(os.path.basename(__file__)).split('.')[0])

        self.session = None
        self.cloud_url = "https://vip.wps.cn/sign/v2"
        self.checkin_message, self.is_success = self.wps_cloud_sign()

    def __wps_checkin_get_cloud__(self):
        if self.cookie is None:
            raise Exception('The cookie is None')
        if self.cookie.startswith("cookie:"):
            self.cookie = self.cookie[len("cookie:"):]

        cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in self.cookie.split("; ")}
        data = {
            'platform': '8'
        }
        self.session = requests.session()
        cloud_resp = self.session.post(url=self.cloud_url, cookies=cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True),
                                       headers=cloud_header, timeout=20, data=data, verify=False)
        cloud_resp_json = json.loads(cloud_resp.text)

        is_success = True
        if 'result' in cloud_resp_json and cloud_resp_json['result'] == 'ok':
            checkin_message = f'签到成功，已成功获取云空间\t'
        elif 'result' in cloud_resp_json and cloud_resp_json['result'] == 'error':
            if cloud_resp_json["msg"] == 'need_captcha':
                checkin_message = f'签到失败，此次签到需要验证码,请手动签到\t'
                is_success = False
            else:
                checkin_message = f'签到失败，请手动签到\t'
                is_success = False
        else:
            checkin_message = '获取cloud 云空间异常\t'
            is_success = False
        message = f'签到信息: {checkin_message}'
        return message, is_success

    def wps_cloud_main(self):
        is_success = True
        # 执行签到
        if self.cookie is not None and len(self.cookie) > 0:
            account_checkin_message, is_success = self.__wps_checkin_get_cloud__()
            # 存在账户签到信息，说明成功执行了签到
            if account_checkin_message is not None and len(account_checkin_message) > 0:
                log_info(f"[Wps_cloud_Account_{self.account_index}]:" + str(account_checkin_message), my_logger=self.logger)
                self.checkin_message.append(f"[Wps_cloud_Account_{self.account_index}] :" + account_checkin_message + "    \n")

        return self.checkin_message, is_success

    def wps_cloud_sign(self):
        if self.config is None or self.config == '':
            return ''.join(self.checkin_message), False
        try:
            is_success = True
            # 如果是字符串，说明是单个cookie
            if self.config is not None and len(self.config) > 0:
                log_info('*******************************Wps cloud checkin*******************************', my_logger=self.logger)
                if isinstance(self.config, str) is True:
                    self.cookie = self.config
                    self.account_index = 1
                    self.checkin_message, is_success = self.wps_cloud_main()
                elif isinstance(self.config, list) is True:
                    for i in range(0, len(self.config)):
                        if isinstance(self.config[i], dict) is True:
                            self.cookie = self.config[i]['cookie']
                            self.account_index = i + 1
                            self.checkin_message, is_success = self.wps_cloud_main()
                        else:
                            log_info('Wps cloud config error' + '    \n', my_logger=self.logger)
                            self.checkin_message.append('Wps vip config error' + '    \n')
                            is_success = False
                else:
                    is_success = False
                    log_info('Wps cloud config error' + '    \n', my_logger=self.logger)
                    self.checkin_message.append('Wps cloud config error' + '    \n')
                log_info('*******************************Wps cloud checkin complete*******************************', my_logger=self.logger)
                return ''.join(self.checkin_message), is_success
        except Exception as e:
            self.checkin_message.append('main function: Wps cloud checkin error, the error is ' + str(e) + '    \n')
            log_info('main function: Wps cloud checkin error, the error is ' + str(e) + '    \n', my_logger=self.logger)
            log_info('*******************************Wps cloud error*******************************', my_logger=self.logger)
            is_success = False
            return ''.join(self.checkin_message), is_success
