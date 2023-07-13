from scripts.common.base_node import BaseNode
from scripts.common.nodes.bugly_download import BuglyDownload
from scripts.pipeline.get_stiff import GetStiff
from scripts.custom_environment import custom_env
from scripts import log
from devops_tool import DevopsTool
from scripts import fpath
import re
import subprocess
import os
import codecs
import shutil


# library = "libUE4.so"
# sym_library = "D:/libUE4.so"

# source_name = "E:\\APGameProfiles\\2023v11Crash-8A\\FS\\data\\tombstones\\tombstone_03"
# dest_name = "E:\\APGameProfiles\\2023v11Crash-8A\\FS\\data\\tombstones\\tombstone_03.sym.txt"

# bias = "0x0"

class ADDRLINE(BaseNode):

    def __init__(self):
        super(ADDRLINE, self).__init__()
        self.bias = custom_env.get("bias", "0x0")
        self.library = "libUE4.so"
        self.workspeace_path = os.getenv("WorkSpace")
        self.buildmode = ''
        self.android32 = ''

    def execute(self, context):

        super(ADDRLINE, self).execute(ADDRLINE)

        target = GetStiff().get_param("target")
        log.info("Target", target)

        self.buildmode = GetStiff().get_param("BuildMode")
        # self.buildmode = "Development"
        log.info("BuildMode", self.buildmode)

        self.android32 = custom_env.get("Android32", "false")

        pipline_url = GetStiff().finally_info()["pipeline"]
        log.info("pipline_url", pipline_url)

        sym_library = self.download_res(pipline_url)
        if pipline_url is "":
            log.error("appversion is invalid")
            return False
        if not sym_library:
            return False

        # self.main(self.get_source_name(), sym_library[0])

        return True

    def main(self, source_name, sym_library):
        output = []
        state = 0
        with codecs.open(source_name, "r", encoding="utf-8") as sourceFile:
            #    with codecs.open(source_name, "r") as sourceFile:
            for line in sourceFile.readlines():
                output.append(line)
                address = self.get_address(line)
                log.info("bias", self.bias)
                if address is not None:
                    new_addr = hex(int(address, 16) + int(self.bias, 16))[2:]
                    print("parsing line " + address + "->" + new_addr + ": " + line)

                    source = self.get_source_line(sym_library, new_addr)
                    if source is not None:
                        state = 1
                        temp = source.read()
                        output.append(temp)
                        print(temp)

        if state == 0:
            print('No addresses found')
            return
        else:
            with codecs.open(self.get_dest_name(), "w", encoding="utf-8") as writeFile:
                #        with codecs.open(dest_name, "w") as writeFile:
                writeFile.writelines(output)

    def get_address(self, line):
        # #02 pc 0000000004e987d8  /data/app/com.ea.gp.apexlegendsmobilefps-Tv8r39-7V4uBm80sPEwAlg==/lib/arm64/libUE4.so (offset 0x4373000)
        search = re.search(r'#[0-9]{1,3}\s+pc\s+([0-9A-Fa-f]+)\s+/data.+' + self.library, line)  # offset

        # search = re.search(r'#[0-9]{1,3}:\s+(0x[0-9A-Fa-f]+)\s+/data.+' + library, line) # offset
        # search = re.search(r'#[0-9]{1,3}:\s' + library + r'(0x\w+)', line) # offset

        # #1 0x776f587f2f  (/data/app/com.ea.gp.apexlegendsmobilefps-1/lib/arm64/libUE4.so+0x10c12f2f)
        # search = re.search(r'#[0-9]+\s+.*' + library + r'\+([0-9A-Fa-fx]+)\)', line) #asan    #02

        # search = re.search(r"/lib/\w+/" + library + r"\+(0x\w+)\)", line) # address
        if search is None:
            return None
        else:
            return search.groups(1)[0]

    def get_source_line(self, library, address):
        # return os.popen(
        #     "C:/NVPACK/android-ndk-r16b/toolchains/x86-4.9/prebuilt/windows-x86_64/bin/i686-linux-android-addr2line.exe -aCpife %s %s" % (
        #         library, address))
        addr2line_path = r"C:/NVPACK/android-ndk-r16b/toolchains/x86-4.9/prebuilt/windows-x86_64/bin"
        lsdir = os.listdir(addr2line_path)
        for file in lsdir:
            if file.endswith("addr2line.exe"):
                finally_addr2line_path = os.path.join(addr2line_path, file)
                log.info("finally_addr2line_path", finally_addr2line_path)
                return os.popen(("%s -aCpife %s %s") % (finally_addr2line_path, library, address))

    def get_source_name(self):
        source_name_path = os.path.abspath(os.path.join(self.workspeace_path, "tombstone_03"))
        log.info("source_name_path", source_name_path)
        return source_name_path

    def get_dest_name(self):
        dest_name_path = os.path.abspath(os.path.join(self.workspeace_path, "tombstone_03.sym.txt"))
        return dest_name_path

    def download_res(self, pipeline):
        devops_tool = DevopsTool()
        pipline_id = ''
        build_id = ''
        path = []
        url_infos = pipeline.split("/")
        for info in url_infos:
            if info.startswith("p-"):
                pipline_id = info
                continue
            if info.startswith("b-"):
                build_id = info
        # 获取下载链接
        file_list = devops_tool.get_pipline_products_path_list(pipline_id, build_id)
        download_list = []
        for file in file_list:
            path_item = file.split("/")
            if self.buildmode in path_item and ("libUE4.so" in path_item or path_item[-1].endswith(".dSYM")):
                if "IOS" in path_item[1]:
                    download_list.append(file)
                    break
                if self.android32 == 'false':
                    if "arm64" in path_item:
                        download_list.append(file)
                        break
                else:
                    if "arm32" in path_item:
                        download_list.append(file)
                        break

        log.info("download_list:", download_list)
        # 下载资源
        root = fpath.FPath().get_backup_dir()
        self.appversion = GetStiff().get_param("APPVersion")
        bugly_name = r"%s_%s" % (self.appversion, self.buildmode)
        root_path = os.path.abspath(
            os.path.join(root, "..", "..", "AClient", "Build", "BuildTool", "Addrline", bugly_name))
        # 文件夹的初始化
        root_path_init = os.path.abspath(os.path.join(root_path, ".."))
        if os.path.exists(root_path_init):
            shutil.rmtree(root_path_init)
            log.info("进行文件夹的初始化")

        log.info("path:", root_path)
        if not os.path.exists(root_path):
            os.makedirs(root_path)

        for item in download_list:
            url = BuglyDownload().get_user_download_url(item)
            if url is None:
                log.error("url or file is invalid!")
                return None
            local_path = os.path.join(root_path, item.split("/")[-1])
            log.info("local_path:", local_path)
            if not os.path.exists(local_path):
                GetStiff().download_largefile_by_package(url, root_path, item.split("/")[-1])
            if os.path.exists(local_path):
                path.append(local_path)
                log.info("%s download succeed!" % item)
            else:
                log.info("download failed!" % item)
        return path

