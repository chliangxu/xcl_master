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
        file_path = os.getenv("")
        data_file = xlrd.open_workbook(r"E:\\构建手机设备管理.xlsx")
        sheet = data_file.sheets()[0]

        for row_index in range(sheet.nrows):
            if row_index != 0:
                row = sheet.row_values(row_index)
                file_list.append(row)

        return file_list


