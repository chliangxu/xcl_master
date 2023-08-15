# 旧代码
import xlrd
import requests
import os


class xlsx_datatable:

    def __init__(self):
        self.xlsx_dic = {}
        self.user_list = []
        self.robot_key = "41757ab9-1285-419d-9386-08372b258a85"

    def user_list_phone(self):
        for users in self.xlsx_file():
            self.user_list.append(users[-3])

        set1 = set(self.user_list)
        self.user_list = list(set1)
        return self.user_list

    def phone_info(self):
        for file_list in self.xlsx_file():
            self.xlsx_dic[file_list[-3]] = {}

        for file_list in self.xlsx_file():
            count = len(self.user_list_phone())
            for i in range(count):
                if file_list[-3] == self.user_list_phone()[i]:
                    a = {
                        file_list[1]:file_list[0]
                    }
                    self.xlsx_dic[self.user_list_phone()[i]].update(a)

        return self.xlsx_dic


    def send_with_user_to_wx_robot_report(self, message_str, robot_key, user_list):
        # 企业微信发送的信息@对应的人或一群人 --> user_list(支持一个或多人)
        import json
        # 企业微信机器人发送消息
        webhook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=%s' % robot_key

        # 推送消息时，可能存在消息内容过长情况，这里分批发送
        content_list = []
        MAX_LEN = 4096
        while len(message_str) >= MAX_LEN:
            add_content = message_str[0:MAX_LEN]
            content_list.append(add_content)
            cur_msg_len = len(message_str)
            message_str = message_str[MAX_LEN + 1:cur_msg_len]
        content_list.append(message_str)

        for content_str in content_list:
            headers = {
                'Content-Type': 'application/json',
            }

            data = {
                "msgtype": "text",
                "text": {
                    "content": content_str,
                    "mentioned_list": user_list,
                }
            }
            response = requests.post(url=webhook_url, data=json.dumps(data), headers=headers)
            print(response)

    def finally_send(self):
        for k,v in self.phone_info().items():
            msg = str(v) + "\n"
            msg += "这个是提示构建组的手机是否还在手里，以免时间过长，不知道手机在哪，提示语：前面是资产编码，后面是具体手机"
            print(msg, type(msg))
            user_list = []
            user_list.append(k)
            user_list.append("v_chliangxu")
            self.send_with_user_to_wx_robot_report(msg, self.robot_key, user_list)

    @staticmethod
    def xlsx_file():
        file_list = []
        # file_path = os.getenv("")
        data_file = xlrd.open_workbook(r"E:\\构建手机设备管理.xlsx")
        sheet = data_file.sheets()[0]

        for row_index in range(sheet.nrows):
            if row_index != 0:
                row = sheet.row_values(row_index)
                file_list.append(row)

        return file_list


# if __name__ == '__main__':
#     print(xlsx_datatable().phone_info())

# 新代码
import xlrd
import os
import datetime
from scripts import log
from scripts.common.base_node import BaseNode
from scripts.common.new_database.create_table import DatabaseOperation
from scripts.pipeline import all_parameter


class PHONESENDFILE(BaseNode):
    """
    1.创建数据表以及导入数据
    2.发送信息到对应的群
    """

    def __init__(self):
        super(PHONESENDFILE, self).__init__()
        self.user_list = []
        self.robot_key = "41757ab9-1285-419d-9386-08372b258a85"

    def execute(self, context):
        if not self.create_info():
            log.info("数据库文件导入失败")
            return False

        self.user_list = ["v_jffchen"]
        msg = "手机状态刷新了 \n"
        msg += "请点击网址查看 http://9.135.94.3:8080/phone_info \n"
        msg += "流水线https://devops.woa.com/console/pipeline/gngame/p-d5908c1bf741450ca0836e3011883f95/detail/b-60ab9e46542e4ef0a96470fc6cc9f960/executeDetail"
        all_parameter.send_with_user_to_wx_robot_report(msg, self.robot_key, self.user_list)

        return True

    # 创建数据表以及导入数据
    def create_info(self):
        cnn = DatabaseOperation(ip="9.135.94.3", pwd="123456789", user="root", database="web")
        cnn.truncate("phone_info")  # 需要清空表从新存储数据，因为机器名字可能会修改，导致与数据库中的名字不一样
        for lis_info in self.xlsx_file():
            phone_info_dict = dict()
            phone_info_dict["phone"] = lis_info[0]
            phone_info_dict["phone_decode"] = lis_info[1]
            phone_info_dict["phone_user"] = lis_info[2]
            phone_info_dict["borrow_in_people"] = lis_info[3]
            phone_info_dict["borrow_date"] = self.covert_time(lis_info[4])
            phone_info_dict["is_return"] = lis_info[5]
            phone_info_dict["return_date"] = lis_info[6]
            phone_info_dict["borrow_out_people"] = lis_info[7]
            phone_info_dict["remark"] = lis_info[-1]
            print(type(phone_info_dict), phone_info_dict)
            cnn.insert(table_name="phone_info", need_insert_fiels_and_data=phone_info_dict)
        cnn.close_db()
        return True

    # excel中的时间转换
    def covert_time(self, time_int):
        """
        time_int:excel转换的时间戳
        """
        if time_int is "":
            return time_int
        else:
            py_date = datetime.date.fromordinal(datetime.datetime(1900, 1, 1).toordinal() + int(time_int) - 2)
            py_date_str = py_date.strftime('%Y-%m-%d')

            return py_date_str

    @staticmethod
    def xlsx_file():
        file_list = []
        workspeace = os.getenv("WorkSpace")
        # workspeace = r"E:\构建手机设备管理.xlsx"
        file_path = os.path.abspath(os.path.join(workspeace, "Buildphone.xlsx"))
        data_file = xlrd.open_workbook(file_path)
        sheet = data_file.sheets()[0]

        for row_index in range(sheet.nrows):
            if row_index != 0:
                row = sheet.row_values(row_index)
                file_list.append(row)

        return file_list
