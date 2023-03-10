
import os
path = r"E:\landun\agent"

# for i in os.listdir(path):
#     file_path = os.path.join(path, i)
#     if os.path.isfile(file_path):
#         # print(file_path)
#         if i == "devopsDaemon.exe":
#             print(file_path)


import wmi

wmiobj = wmi.WMI()

services = wmiobj.Win32_Service()

for i in services:

    # print("%d:%s -> %s [%s] %s" %(services.index(i) + 1,i.Name,i.Caption,i.State, i.PathName))

    path = i.PathName
    print(type(i.PathName), path)
    print(path.split("\\"))


