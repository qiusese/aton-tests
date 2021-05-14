from configparser import ConfigParser
import os

config = ConfigParser()
filename = os.path.dirname(__file__) + '/config.ini'  # 配置文件


def get_env(title, subtitle):
    """subtitle
    :param title: 配置头部
    :param subtitle: 配置内的内容
    :return:
    """

    config.read(filename)  # 读取配置文件
    if title not in config.sections():
        print('不存在该配置项目，请检查配置文件config.ini')
    elif subtitle not in config.options(title):
        print(f'该{title}配置项目下不存在{subtitle}元素，请检查配置文件config.ini')
    else:
        setting = config.get(title, subtitle)
    return setting


def iOS_cpas() -> dict:
    """
    以字典形式返回设备配置
    :return:
    """

    config.read(filename)
    return dict(config._sections['iOS_caps'])
