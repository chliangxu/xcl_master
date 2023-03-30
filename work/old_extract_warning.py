import os
# for root, dirs, files in os.walk(".", topdown=False):
#     for name in files:
#         print(os.path.join(root, name))
#     for name in dirs:
#         print(os.path.join(root, name))

#旧版提取cook日志
import re
import os
from glob import *


def get_path(root_path="", pattern=""):
    rootpath = os.path.abspath(root_path)
    file_path = []
    for root, dirs, files in os.walk(rootpath):
        for match in glob(os.path.join(root, pattern)):
            file_path.append(match)
    for out_path in file_path:
        father_path = os.path.dirname(out_path)
        son_path = os.path.join(father_path, "Warning.log")
        # 筛选出含Warning的信息
        with open(out_path, "r", encoding="utf-8", errors="ignore")as f:
            file_list = f.readlines()
            for line_file in file_list:
                result = re.match(".*Log.*Warning:.*", line_file)

                # 筛选出符合的Warning信息
                if result:
                    group = result.group()
                    # condition_list = [
                    #     ".*LogAssetRegistryGenerator:\sWarning:\sChildChunk.*",
                    #     ".*LogFastPicture:\sWarning:\sFFPAdvanceSettingOption.*",
                    #     ".*LogInit:\sWarning:\sCreating.*",
                    #     ".*LogShaderCompilers:\sWarning:\sCan't.*",
                    #     ".*LogPluginManager:\sWarning:\sRead.*",
                    # ]
                    if not re.match(".*LogAssetRegistryGenerator:\sWarning:\sChildChunk.*", group):

                        if not re.match(".*LogFastPicture:\sWarning:\sFFPAdvanceSettingOption.*", group):

                            if not re.match(".*LogInit:\sWarning:\sCreating.*", group):

                                if not re.match(".*LogShaderCompilers:\sWarning:\sCan't.*", group):

                                    if not re.match(".*LogPluginManager:\sWarning:\sRead.*", group):
                                        str_file = str(group)
                                        print(str_file)
                                        with open(son_path, "a", encoding="utf-8")as l:
                                            l.write(str_file + "\n")

        # 过滤掉相同的信息
        bro_path = os.path.join(father_path, "New_Warning.log")
        outfile = open(bro_path, "w", encoding="utf-8")
        listen = set()
        with open(son_path, "r", encoding="utf-8", errors="ignore")as x:
            for line in x:
                line = line.strip("\n")
                if line not in listen:
                    outfile.write(line + "\n")
                    listen.add(line)
                    # print(line)XQ


if __name__ == '__main__':
    get_path("", "*.txt")

