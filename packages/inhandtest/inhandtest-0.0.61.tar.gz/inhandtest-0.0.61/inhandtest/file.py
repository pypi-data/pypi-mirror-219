# -*- coding: utf-8 -*-
# @Time    : 2023/2/23 16:48:50
# @Author  : Pane Li
# @File    : file.py
"""
file

"""
import os
import random
import string
import logging


def del_file(file_path: str) -> None:
    """删除指定路径下的所有文件或单个文件

    :param file_path:
    :return:
    """
    if os.path.isdir(file_path):
        for i in os.listdir(file_path):
            c_path = os.path.join(file_path, i)
            if os.path.isdir(c_path):
                del_file(c_path)
            else:
                os.remove(c_path)
    elif os.path.isfile(file_path):
        os.remove(file_path)
    else:
        logging.debug(f"parameter file_path {file_path} is not exist")


def check_file(file_path) -> None:
    """校验文件是否存在

    :param file_path: 文件夹路径或者文件路径
    :return:  检查到文件不存在时就抛异常FileNotFoundError
    """
    if not os.path.isfile(file_path) or not os.path.exists(file_path):
        logging.exception(f"this file {file_path} not exist")
        raise FileNotFoundError(f"this file {file_path} not exist")
    else:
        logging.debug(f"check file {file_path} ok")


def check_dir(dir_path, create_dir=True) -> None:
    """

    :param dir_path:  问价夹路径
    :param create_dir:
    :return:
    """
    if os.path.exists(dir_path):
        logging.debug(f"check dir {dir_path} ok")
    else:
        if create_dir:
            os.makedirs(dir_path)
            logging.debug(f"create dir {dir_path} ok")
        else:
            logging.exception(f"this dir {dir_path} not exist")
            raise FileNotFoundError(f"this file {dir_path} not exist")


def generate_str_or_file(size: int or str = '48KB', file_path=None) -> str:
    """生成指定大小字符串或文件 1024KB=1MB  1024MB=1GB  1024GB=1TB

    :param size: int or str, int时单位为字节， str可带单位'KB'|'MB'|'GB', e.g: 49152|'48KB'...
    :param file_path: 文件全路径，ex: /$file_path/test.txt 将内容写道文件中
    :return: 返回文件内容, 即指定大小的字符串
    """
    str_ = ''

    if isinstance(size, str):
        if 'KB' in size:
            size = int(float(size.replace('KB', '')) * 1024)
        elif 'MB' in size:
            size = int(float(size.replace('MB', '')) * 1024 * 1024)
        elif 'GB' in size:
            size = int(float(size.replace('GB', '')) * 1024 * 1024 * 1024)
    elif isinstance(size, int):
        pass
    else:
        logging.exception(f'param {size} type {type(size)} error, only can be str or int!')
        raise Exception(f'param {size} type {type(size)} error, only can be str or int!')
    if size:  # 都已经转换为byte
        str_ = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
        if os.path.isfile(file_path):  # 生成文件
            with open(file_path, 'w') as file:
                file.write(str_)
            logging.debug(
                f"file {file_path} success create.Size is {os.path.getsize(file_path)}" + 'Byte')
    return str_


def file_hash(file_path_or_msg, hash_type='md5') -> str:
    """

    :param file_path_or_msg:  文件全路径 | 或者加密文件内容
    :param hash_type: 'md5'|'sha1'|'sha256'
    :return:
    """
    from hashlib import md5, sha1, sha256
    if hash_type.lower() == 'md5':
        obj = md5()
    elif hash_type.lower() == 'sha1':
        obj = sha1()
    elif hash_type.lower() == 'sha256':
        obj = sha256()
    else:
        logging.exception(f'Not support this hash_type {hash_type}')
        raise Exception(f'Not support this hash_type {hash_type}')
    if os.path.isfile(file_path_or_msg):
        with open(file_path_or_msg, 'rb') as f:
            obj.update(f.read())
    else:
        obj.update(file_path_or_msg.encode('utf-8'))
    return obj.hexdigest().upper()
