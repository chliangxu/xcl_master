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

delete_floder().getLocalSpace("D:\\")
