
import os
import shutil

def main():
    # Workspace = os.getenv("Workspace")
    Workspace = r"D:\GNGame\trunk"
    need_path = Workspace.split("/")[-1]
    os.system("rd /s /q %s" % need_path)
    exe_delete_path_list = os.listdir(Workspace)
    for delete_path in exe_delete_path_list:
        abs_delete_path = os.path.join(Workspace, delete_path)
        os.system("del /s /f /q %s" % abs_delete_path)


    while len(os.listdir(Workspace)) != 0:
        os.system("rd /s /q %s" % need_path)

    # print("删除母目录")
    # shutil.rmtree(Workspace)

if __name__ == '__main__':
    main()