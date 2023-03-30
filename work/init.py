# 需求：初始化删除蓝盾和P4的目录
from scripts.common.base_node import BaseNode
from scripts import log
from scripts import utils
import os
import time


class InitP4Agent(BaseNode):

    def execute(self, context):
        start_time = time.time()
        # 1.对P4的进行的操作
        if not self.finally_P4_init():
            return False

        # 2。获取agent的路径并初始化agent的目录
        if not self.finally_agent_init():
            return False

        end_time = time.time()
        log.info(f"所需时间为{end_time - start_time}")

        return True

    # 获取蓝盾的路径
    def get_agent_path(self):
        import wmi

        wmiobj = wmi.WMI()

        services = wmiobj.Win32_Service()

        thisset = set()
        for i in services:
            # print("%d:%s -> %s [%s] %s" %(services.index(i) + 1,i.Name,i.Caption,i.State, i.PathName))
            path = i.PathName
            agent_path_split = path.split("\\")
            if agent_path_split[-1] == "devopsDaemon.exe":
                agent_path = os.path.abspath(os.path.join(path, ".."))
                log.info("agent的目录路径{}".format(agent_path))
                thisset.add(agent_path)

        if thisset is None:
            log.info('此台机器没有安装蓝盾')
            return ""

        lis = list(thisset)
        return lis

    # 获取P4的路径
    def get_P4_path(self):
        # 遍历此机器的所有盘符
        all_drive_dict = {}
        import psutil
        for drives in psutil.disk_partitions():
            drive = drives.device
            lis = self.get_dictory_path(drive, "trunk")
            log.info(f"{drive}盘", lis)
            value = {
                "path": lis
            }
            all_drive_dict[drive] = value

        return all_drive_dict

    # 获取P4的目录
    def get_dictory_path(self, url, file_name):
        # 对传进来的盘符进行遍历
        # path为第一级路径
        # 此为第二级路径
        filepaths = []
        try:
            for root, dirs, files in os.walk(url):
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    len_list = len(dir_path.split("\\"))
                    if dir.startswith("$") or root.split("\\")[-1].startswith("$"):
                        continue

                    else:
                        if len_list <= 5:
                            print(f"目录路径{dir_path}, 目录{len_list}级目录")
                            if dir_path.split("\\")[-1] == file_name:
                                filepaths.append(dir_path)
        except:
            print(f"{url}文件没有权限访问")

        return filepaths

    # 初始化文件目录
    def delete_P4_agent(self, path):

        # 再次判断P4的路径
        path_lis = path.split("\\")
        if path_lis[-2] == "GNGame":
            log.info("P4文件开始初始化")
            cmd_str = "rd/s/q " + path
            utils.call_cmd(cmd_str)
            log.info("P4文件初始化完毕")

        elif path_lis[-2] != "GNGame":
            log.info("蓝盾开始初始化")
            cmd_str = "rd/s/q " + path
            utils.call_cmd(cmd_str)
            log.info("蓝盾初始化完毕")

        else:
            log.info("路径不正确")
            return False

        return True

    # 开始获取P4的路径并初始化P4的目录
    def finally_P4_init(self):
        all_P4_dictory = self.get_P4_path()
        for drive, path in all_P4_dictory.items():
            every_path = path["path"]
            if len(every_path) != 0:
                for value in every_path:
                    log.info(f"需要初始化的路径{value}")
                    # 开始文件的初始化
                    self.delete_P4_agent(value)

        return True

    def finally_agent_init(self):
        all_agent_dictory = self.get_agent_path()
        for value in all_agent_dictory:
            log.info("需要初始化的agent目录路径{}".format(value))
            self.delete_P4_agent(value)

        return True




