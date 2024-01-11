import requests
import json
import os
import sys

file_title = []


class TAPDREQUIREMENT():
    """
    1. 获取提缺陷单的数据
    2.整合数据，并传入
    3.开始提单
    """

    def __init__(self):
        super(TAPDREQUIREMENT, self).__init__()
        # self.version_report = os.getenv("version_report", "GN3.0")
        self.WorkSpeace = os.getcwd()
        # self.branch = os.getenv("P4_Branch", "主干")
        # self.reporter = os.getenv("reporter", "v_vvllchen")
        self.web = "cd7e8e32-e01c-430b-a173-5e824fc4afe3"
        self.user_list = []

    # 开始执行函数
    def start_tapd(self):
        default_lis = self.get_default()
        if len(default_lis) == 3:
            # 单子中参数的分支
            version_report = default_lis[0]
            # 标题中的分支
            branch = default_lis[1]
            # 创建单的人
            reporter = default_lis[2]
            for dic_key, dic_value in self.get_database().items():
                file_tapd = dic_key.split("_")[0] + "_" + dic_key.split("_")[1]
                title_tapd = f"【GN{branch}】【不合规Excel资源路径检查】" + file_tapd
                # # 提给何人
                user_tapd = dic_key.split("_")[-1]
                self.create_tapd(title_tapd, version_report, reporter, user_tapd, dic_value)
                msg = "123456" + "\n"
                msg += "测试忽略"
                print("789", type(msg), msg)
                # self.send_with_user_to_wx_robot_report(msg, self.web, self.user_list)
                # self.user_list = []

        else:
            print("请输入对应的参数，以确保运行")
            return

    def get_default(self):
        default_lis = []
        default_path = os.path.join(self.WorkSpeace, "必要参数.txt")
        if os.path.exists(default_path):
            with open(default_path, "r", encoding="utf-8") as f:
                for file in f.readlines():
                    default_lis.append(file.split("-")[0])
            return default_lis

        else:
            print(f"缺少必要参数，路径{default_path}")
            return

    # 获取提取缺陷单的必要数据
    def get_database(self):
        for file_name in os.listdir(self.WorkSpeace):
            if "不合规表格详情内容" in file_name:
                print("缺陷单的数据文件名称", file_name)

                file_path = os.path.join(self.WorkSpeace, file_name)
                with open(file_path, "r", encoding="utf-8") as files:
                    file_dic = {}
                    file_title = []
                    file_lis = []
                    num = 0
                    for file in files.readlines():

                        if "最近提交人" in file:
                            if num == 0:
                                title = file.split(" ")[0]
                                user = file.split(" ")[1].split(":")[-1]
                                title_user = title + "_" + user
                                file_lis.append(file)

                            if num >= 1:
                                file_lis = []
                                title = file.split(" ")[0]
                                user = file.split(" ")[1].split(":")[-1]
                                title_user = title + "_" + user
                                file_lis.append(file)

                            num += 1

                        else:
                            file_lis.append(file)

                        file_dic[title_user] = file_lis
                print("最后的字典文件", file_dic)
        return file_dic

    # 创建tapd的缺陷单
    def create_tapd(self, title_tapd, version_report, reporter, user_tapd, description):
        tapd_stories_url = f"http://apiv2.tapd.woa.com/bugs"

        value = ""
        for i in description:
            value = value
            value += i

        data = {
            "title": f"{title_tapd}",
            "workspace_id": "69990352",
            "version_report": f"{version_report}",
            "severity": "严重",
            "priority": "high",
            "reporter": f"{reporter}",
            "current_owner": f"{user_tapd}",
            "module": "GG-YCSB-异常上报",
            "custom_field_21": "100%",
            "description": f"{value}",
        }
        # response = requests.post(tapd_stories_url, json=data,
        #                          auth=('UGC_Request_2022', '4772919B-0455-88FB-821D-95047A741BEF'))
        #
        # response.encoding = "UTF-8"
        # print("response.status_code", response.status_code)
        # if response.status_code == 200:
        #     response_data = json.loads(response.text)
        #     print("product", response_data["data"])

    # 获取缺陷
    def get_tapd_user(self, user):

        url = f"http://apiv2.tapd.woa.com/bugs?workspace_id=69990352&limit=5&reporter={user}&order=created%20desc"
        response = requests.get(url, auth=('UGC_Request_2022', '4772919B-0455-88FB-821D-95047A741BEF'))

        response.encoding = "UTF-8"
        print("response.status_code", response.status_code)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            print("product", response_data["data"][0]["Bug"]["id"])
            id = response_data["data"][0]["Bug"]["id"]
            urls = f"https://tapd.woa.com/69990352/bugtrace/bugs/view?bug_id={id}"
            return urls

    # 获取项目的自定义参数
    # def get_custom(self):
    #     tapd_stories_url = f"http://apiv2.tapd.woa.com/bugs/custom_fields_settings?workspace_id=69990352"
    #     response = requests.get(tapd_stories_url, auth=('UGC_Request_2022', '4772919B-0455-88FB-821D-95047A741BEF'))
    #
    #     response.encoding = "UTF-8"
    #     if response.status_code == 200:
    #         response_data = json.loads(response.text)
    #         print("product", response_data["data"])

    def send_with_user_to_wx_robot_report(self, message_str, robot_key, user_list=None):
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


if __name__ == '__main__':
    start_func = TAPDREQUIREMENT()
    start_func.start_tapd()
