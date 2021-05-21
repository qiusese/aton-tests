import json
import os


def set_global_atrr(key, value,
                    filepath=os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/global_var.py')),
                    truncate=True):
    """
    写入文件
    :param key: 变量Key
    :param value: 变量Valure
    :param filepath: 文件路径
    :param truncate: 是否清空文件再写入
    :return:
    """
    with open(filepath, 'a+', encoding='utf-8') as f:
        if truncate:
            f.truncate(0)  # 清空文件内容
        else:
            f.write('\n')  # 空行
        f.write(f'{key} = '.strip("'"))
        f.write(json.dumps(value, ensure_ascii=False, indent=4))
