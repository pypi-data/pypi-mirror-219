import json
import os

from yaoys_checkin.checkin_util import file_type_json

__config_file_json_path__ = ["/ql/scripts/yaoys_checkin_config.json",
                             "./config/yaoys_checkin_config.json",
                             "./yaoys_checkin_config.json",
                             "../config/yaoys_checkin_config.json"]


def print_message(is_print=True, message=None):
    if is_print and message is not None and len(message) > 0:
        print(str(message))


def get_config_file(file_type='json'):
    config_file = None
    if file_type == file_type_json:
        json_file = open(get_config_path(file_type=file_type), encoding='utf-8', mode='r')
        config_file = json.load(json_file)
        json_file.close()

    return config_file


def get_config_path(file_type=None):
    if file_type is None:
        raise ValueError('参数错误，请联系管理员')
    config_path = None
    config_path_list = []
    config_path_array = None
    # 如果是json的配置文件
    if file_type == file_type_json:
        config_path_array = __config_file_json_path__

    for one_path in config_path_array:
        _config_path = os.path.join(os.getcwd(), one_path)
        if os.path.exists(_config_path):
            config_path = os.path.normpath(_config_path)
            break
        config_path_list.append(os.path.normpath(os.path.dirname(_config_path)))

    if config_path is None:
        print("未找到 yaoys_checkin_config.json 配置文件\n请在下方任意目录中添加「yaoys_checkin_config.json」文件:\n" + "\n".join(config_path_list))
        raise FileNotFoundError("未找到 yaoys_checkin_config.json 配置文件\n请在下方任意目录中添加「yaoys_checkin_config.json」文件:\n" + "\n".join(config_path_list))
    # print(config_path)
    return config_path
