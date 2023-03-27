import os
import platform
import ctypes


class delete_floder:

    def getLocalSpace(self, folder):
        """
        获取磁盘剩余空间
        :param folder: 磁盘路径 例如 D:\\
        :return: 剩余空间 单位 G
        """
        folderTemp = folder
        if not os.path.exists(folderTemp):
            folderTemp = os.getcwd()
        if platform.system() == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folderTemp), None, None, ctypes.pointer(free_bytes))
            return self.convert_size(free_bytes.value)
        else:
            st = os.statvfs(folderTemp)
            return self.convert_size(st.f_bavail * st.f_frsize)

    def convert_size(self, size):
        # size = get_size(os.getcwd())
        units = ["B", "kB", "MB", "GB", "TB", "PB"]
        sizes = 1024.0
        for i in range(len(units)):
            if (size / sizes) < 1:
                # print("%.2f%s" % (size, units[i]))
                return "%.2f%s" % (size, units[i])
            size = size / sizes

    def get_dictory_size(self, floder):
        """
        获取某个目录的大小
        :param floder: 目录名称 ：”E:\\GNGame“
        :return: 剩余单位：MB
        """
        # 本函数是获取目录的大小
        # getsize是获取单个文件的大小
        catalogue_size = 0
        doc_list = os.listdir(floder)
        for doc in doc_list:
            if os.path.isfile(os.path.join(floder, doc)):
                catalogue_size += os.path.getsize(os.path.join(floder, doc))

            if os.path.isdir(os.path.join(floder, doc)):
                catalogue_size += self.get_dictory_size(os.path.join(floder, doc))

        return catalogue_size


    def get_finally(self, floder):
        len_floder = len(os.listdir(floder))
        if len_floder == 0:
            # 盘符的大小
            self.getLocalSpace(floder)

        else:
            # 目录的大小
            print(self.convert_size(self.get_dictory_size(floder)))

delete_floder().get_finally(r"E:\xcl\xcl_master")
