import os
import shutil
import time


class MOVEFILE:
    """
    1.移动文件的双方路径
    2.
    """
    def move_file(self):
        from_path = os.getcwd()
        start = time.perf_counter()
        self.Visual(from_path)

        end = time.perf_counter()

    def Visual(self, from_path):
        """
        进行移动
        :param from_path: 需要移动的文件路径
        :param to_path: 往哪里移动的路径
        :return:
        """

        #总文件数
        all_file_num = len(os.listdir(from_path))

        # t = 60
        # print("**************带时间的进度条**************")
        # start = time.perf_counter()
        # for i in range(t + 1):
        #     finsh = "▓" * i
        #     need_do = "-" * (t - i)
        #     progress = (i / t) * 100
        #     dur = time.perf_counter() - start
        #     print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(progress, finsh, need_do, dur), end="")
        #     time.sleep(0.05)


MOVEFILE().move_file()