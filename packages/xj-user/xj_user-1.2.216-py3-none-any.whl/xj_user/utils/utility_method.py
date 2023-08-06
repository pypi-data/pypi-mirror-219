import json
import sys
import time
import os
import string
import random
import pytz
import datetime
from django.utils import timezone
from dateutil.parser import parse
from dateutil.tz import tzlocal
import pandas as pd
from datetime import datetime
from decimal import Decimal


# 获取当前时间
def get_current_time():
    # TODO USE_TZ = False 时会报错 如果USE_TZ设置为True时，Django会使用系统默认设置的时区，即America/Chicago，此时的TIME_ZONE不管有没有设置都不起作用。
    tz = pytz.timezone('Asia/Shanghai')
    # 返回datetime格式的时间
    now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S.%f")
    # now = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    now = datetime.now().strptime(now_time, "%Y-%m-%d %H:%M:%S.%f")
    return now


# 时间精确到微秒
def append_microsecond_to_datetime(datetime_str: str) -> datetime:
    """
    将当前微秒追加到日期时间字符串中。如果字符串仅包含日期，当前时间也附加在微秒之前。
    """
    # Check if the datetime string contains a time
    if len(datetime_str.split(' ')) == 2:
        current_microsecond = datetime.now().strftime("%f")
        datetime_str = f'{datetime_str}.{current_microsecond}'
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
    else:
        # Get the current time and microsecond
        current_time_microsecond = datetime.now().strftime("%H:%M:%S.%f")
        datetime_str = f'{datetime_str} {current_time_microsecond}'
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
    return dt


# 数据key替换
def replace_dict_key(dictionary, old_key, new_key):
    if old_key in dictionary:
        dictionary[new_key] = dictionary.pop(old_key)
    return dictionary


# 数据字典key替换
def replace_key_in_dict(original_dict, old_key, new_key):
    copied_dict = original_dict.copy()
    if old_key in copied_dict:
        copied_dict[new_key] = copied_dict.pop(old_key)
    return copied_dict


# 数据列表key替换
def replace_key_in_list_dicts(list_dicts, old_keys, new_key):
    for d in list_dicts:
        for old_key in old_keys:
            if old_key in d:
                d[new_key] = d.pop(old_key)
    return list_dicts


# 数据列表字典key替换
def replace_key_in_list_replacement_dicts(list_dicts, replacement_dict):
    for d in list_dicts:
        for old_key, new_key in replacement_dict.items():
            if old_key in d:
                d[new_key] = d.pop(old_key)
    return list_dicts


# 字符串转列表
def parse_integers(value):
    if isinstance(value, str):
        if "," in value:
            lst = [int(num) for num in value.split(",")]
        else:
            lst = [int(value)]
    elif isinstance(value, int):
        lst = [value]
    else:
        raise TypeError("不支持的值类型。应为字符串或int")

    return lst


# 保留两位小数
def keep_two_decimal_places(str_num):
    result_num = format(float(str_num), "")

    if len(result_num.split(".")[-1]) < 2:
        result_num = result_num + "0"
    return result_num


# 生成一个长度为16的密码
def generate_password(length=16):
    # 合并所有可能的字符，包括大小写字母、数字和标点符号
    # all_chars = string.ascii_letters + string.digits + string.punctuation
    all_chars = string.ascii_letters + string.digits
    # length = random.randint(8, 12)
    # 随机选择指定数量的字符
    password = ''.join(random.choice(all_chars) for _ in range(length))

    return password


# 数字表示生成几位, True表示生成带有字母的 False不带字母的
def get_code(n=6, alpha=False):
    s = ''  # 创建字符串变量,存储生成的验证码
    for i in range(n):  # 通过for循环控制验证码位数
        num = random.randint(1, 9)  # 生成随机数字0-9
        if alpha:  # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
            upper_alpha = chr(random.randint(65, 90))
            lower_alpha = chr(random.randint(97, 122))
            num = random.choice([num, upper_alpha, lower_alpha])
        s = s + str(num)
    return s


# 检查列表字段是否存在
def find(list, keyword):
    try:
        list.index(keyword)
        return True
    except ValueError:
        return False


# 批量数据时间格式化
def format_dates(data, date_fields):
    for item in data:
        for field in date_fields:
            if field in item and item[field]:
                try:
                    # 如果字段已经是 datetime 对象，就无需解析
                    if isinstance(item[field], datetime):
                        date = item[field]
                    else:
                        # 尝试解析并格式化日期
                        date = parse(item[field])
                    # 使用 strftime 格式化日期
                    item[field] = date.astimezone(tzlocal()).strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # 如果解析失败，保留原来的值
                    pass
    return data


# 列表根据指定key计算value求和
def aggregate_data(data_list, group_field, agg_fields):
    # 将数据转换为 DataFrame
    df = pd.DataFrame(data_list)

    # 将累加字段转换为数值型
    for field in agg_fields:
        df[field] = pd.to_numeric(df[field])

    # 根据 group_field 对数据进行分组，并对 agg_fields 进行求和
    grouped = df.groupby(group_field)[agg_fields].sum().reset_index()

    # 将结果转换回字典列表
    grouped_data = grouped.to_dict('records')

    return grouped_data


# json模板替换
def replace_placeholders(data, replacements):
    # 将 data 转换为 JSON 格式的字符串
    data_str = str(data)

    # 依次替换每一个 "{{}}"
    for replacement in replacements:
        data_str = data_str.replace("{{}}", replacement, 1)

    # 将字符串重新转换为字典
    data = eval(data_str)

    return data


# 获取程序运行时间
def testRunTime():
    start = datetime.now()
    for i in range(1000):
        for j in range(500):
            m = i + j
            print(m)
    end = datetime.now()
    print(end - start)
    return end - start


# json转换
def convert_dict_to_json(data):
    def convert_values_to_str(value):
        if isinstance(value, dict):
            return {convert_values_to_str(key): convert_values_to_str(val) for key, val in value.items()}
        elif isinstance(value, list):
            return [convert_values_to_str(val) for val in value]
        elif isinstance(value, Decimal):
            return str(value)
        elif value is None:
            return value
        else:
            return str(value)

    converted_data = convert_values_to_str(data)
    json_str = json.dumps(converted_data, ensure_ascii=False)
    return json_str
