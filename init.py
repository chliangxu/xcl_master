# 需求：初始化删除蓝盾和P4的目录
import os



class DeleteP4:

    def get_all_path(self):
        # 1.获取到蓝盾的路径和P4的路径
        pass

        # 2。获取P4的路径
        pass


    # 获取蓝盾的路径
    def get_agent_path(self):
        # C盘
        self.scnner_file("E:\\")

    def scnner_file(self, url):
        # 对传进来的盘符进行遍历
        file_list = os.listdir(url)
        for filename in file_list:
            file_path = os.path.join(url, filename)
            print("+++")
            if filename == "GNGame":
                print(file_path)
                return file_path

            elif filename != "GNGame":
                if os.path.isfile(file_path):
                    continue

                elif os.path.isdir(file_path):
                    print("file_path", file_path)
                    self.scnner_file(file_path)

    #获取某路径下的三级目录

    def get_three_path(self, path, filename):
            #第一级目录
        for value in os.listdir(path):
            print(value)
            if value == filename:
                finally_path = os.path.join(path, value)
                print("在第一级目录找到", finally_path)
                return finally_path


            else:
                pass
                # self.get_three_path(os.path.join(path, value), filename)


print(DeleteP4().get_three_path(r"E:\\", "GNGame"))