
import re
import os
# from scripts import log

# """
# name: 通配符的后缀
# """
#
#
# def get_path(root_path="", name=""):
#     #     #取得目录
#     #     rootpath = os.path.abspath(root_path)
#     #     file_path = []
#     #     for match in glob(os.path.join(rootpath, name)):
#     #         file_path.append(match)
#     for files_path in file_path:
#         # files_path得到文件路径
#         # print(files_path)
#         return files_path


"""
distinct_warning_logs   : 集合
warning_line            : 匹配之后含有Warning的内容
warning_log_path        : 打开文件的路径
"""


def append_new_warning_to_file(distinct_warning_logs, warning_line, warning_log_path):
    # 筛选出符合的Warning信息
    if not re.match(".*LogAssetRegistryGenerator:\sWarning:\sChildChunk.*|"
                    ".*LogFastPicture:\sWarning:\sFFPAdvanceSettingOption.*|"
                    ".*LogInit:\sWarning:\sCreating.*|"
                    ".*LogShaderCompilers:\sWarning:\sCan't.*|"
                    ".*LogPluginManager:\sWarning:\sRead.*", warning_line):
        new_str_file = str(warning_line)
        print(new_str_file) #在脚本中可用log.info
        if new_str_file not in distinct_warning_logs:
            with open(warning_log_path, "a", encoding="utf-8") as out_file:
                # 写入文件内容前先清楚文件内的内容
                out_file.truncate()
                out_file.write(new_str_file + "\n")
                distinct_warning_logs.add(new_str_file)

                return distinct_warning_logs


def got_warning_log_file(log_path):
    parent_path = os.path.dirname(log_path)
    warning_log_path = os.path.join(parent_path, "Warning.log")
    # 筛选出含Warning的信息
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        file_list = f.readlines()
        distinct_warning_logs = set()
        for line_file in file_list:
            result = re.match(".*Log.*Warning:.*", line_file)
            if result:
                warning_line = result.group()
                # 用集合过滤掉相同的信息
                append_new_warning_to_file(distinct_warning_logs, warning_line, warning_log_path)


