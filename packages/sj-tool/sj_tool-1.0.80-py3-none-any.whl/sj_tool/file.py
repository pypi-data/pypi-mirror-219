import json
import os
import re
import shutil
import yaml


def makedir(path, delete_old=False):
    if delete_old:
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)


def sanitize_filename(filename, alter_char="_"):
    """
    将文件名中的不合法字符替换为某个合法字符
    :param filename:
    :param alter_char:
    :return:
    """
    # 定义不合法的字符正则表达式模式
    illegal_chars = r'[\/:*?"<>|]'

    # 使用"#"替换不合法字符
    sanitized_filename = re.sub(illegal_chars, alter_char, filename)

    return sanitized_filename


def load_yaml(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)


def load_json(filename):
    """加载json文件"""
    if os.path.exists(filename) and os.path.isfile(filename):
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    return None


def dump_json(obj, filename):
    """保存为json文件"""
    with open(filename, "w", encoding="utf-8") as f:
        return json.dump(obj, f, ensure_ascii=False)
