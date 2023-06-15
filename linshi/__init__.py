from scripts.common.base_node import BaseNode
from scripts import patch_utils
from scripts.custom_environment import custom_env
from scripts import log
from scripts import command_param
import os
import shutil
import zipfile
import requests
import json


class GetStiff(BaseNode):
    """
    # 1.获取文件的路径
    # 2.获取下载链接
    # 3.最后下载bugly文件
    """

    def __init__(self):
        super().__init__()
        self.build_info = None

    # 参数优先级别：命令行参数，custom_env参数，构建信息参数
    def get_param(self, param_name):
        param_value = command_param.parse_arg("-" + param_name)
        print("param_value", param_value)
        if param_value is None:
            param_value = custom_env.get(param_name)

        if param_value is None:
            if param_name == "BuildMode":
                param_value = self.get_build_info()["build_mode"]
            elif param_name == "target":
                # 从构建信息BuildClass 映射取 target
                build_class = self.get_build_info()["BuildClass"]
                if build_class == "ipa" or build_class == "ios_pak" or build_class == "ios_patch":
                    param_value = "ios"
                elif build_class == "apk" or build_class == "android_pak" or build_class == "android_patch":
                    param_value = "android"
            elif param_name == "ARM":
                # 没有指定,默认返回64位
                param_value = "arm64"
        return param_value

    def execute(self, context):
        # 1.获取文件的路径
        bugly_file = self.get_bugly_file()
        log.info("bugly_file", bugly_file)
        log.info("输入的版本号不是一个整包或编译模式不正确，请重新输入")

        # 2.获取下载链接
        if not self.get_user_download_url(bugly_file):
            log.error("None URL, please check your piplineId and buildId, file name")
            return False

        # 3.最后下载bugly文件
        # from scripts import utils
        working_dir = os.getcwd()
        stiff_root_path = os.path.join(working_dir, "stiff")
        # 初始化
        if os.path.exists(stiff_root_path):
            keep_stiff = self.get_param("KeepStiff")
            if not keep_stiff:
                shutil.rmtree(stiff_root_path)
                log.info("进行文件夹的初始化")

        if not os.path.exists(stiff_root_path):
            os.mkdir(stiff_root_path)

        app_version = self.get_param("APPVersion")
        print("app_version", app_version)
        if app_version is None:
            log.error("pass in app_version is None")
            return False

        work_path = stiff_root_path
        # 子目录
        stiff_subPath = self.get_param("StiffSubPath")
        if stiff_subPath is not None:
            work_path = os.path.join(stiff_root_path, stiff_subPath)
            if not os.path.exists(work_path):
                os.mkdir(work_path)
        log.info("work_path", work_path)
        build_mode = self.get_param("BuildMode")
        stiff_file_name = bugly_file.split("/")[-1]
        stiff_file_name = r"%s_%s_%s" % (app_version, build_mode, stiff_file_name)
        stiff_path = os.path.abspath(os.path.join(work_path, stiff_file_name))

        if os.path.exists(stiff_path):
            log.info("stiff_exists", stiff_path)
            return True
        self.download_largefile_by_package(self.get_user_download_url(bugly_file), work_path, stiff_file_name)
        log.info("stiff_path", stiff_path)
        z = zipfile.ZipFile(r"%s" % stiff_path)

        z.extract(z.namelist()[0], work_path)
        log.info("stiff文件", stiff_file_name)
        log.info("stiff目录", work_path)
        log.info("下载完成")
        return True

    # 获取bugly文件
    def get_bugly_file(self):
        target = self.get_param("target")
        log.info("平台", target)
        pipline_url = self.get_build_info()["pipeline"]
        log.info("pipline_url", pipline_url)
        ARM = self.get_param("ARM")
        log.info("ARM", ARM)
        BUildMode = self.get_param("BuildMode")
        log.info("BuildMode", BUildMode)
        get_target_filename_path = self.get_all_product(pipline_url)
        if target == "android":
            for dict_file in get_target_filename_path:
                if dict_file["name"] == "libUE4.so.zip":
                    android_bugly_name_path = dict_file["fullName"]
                    if android_bugly_name_path.split("/")[-2] == f"{ARM}" and android_bugly_name_path.split("/")[
                        -3] == f"{BUildMode}":
                        log.info(f"下载{ARM}位的文件路径名称", android_bugly_name_path, type(android_bugly_name_path))
                        return android_bugly_name_path

                    elif android_bugly_name_path.split("/")[-2] == f"{BUildMode}":
                        log.info(f"下载的bug文件路径名称", android_bugly_name_path, type(android_bugly_name_path))
                        return android_bugly_name_path

        elif target == "ios":
            for dict_file in get_target_filename_path:
                if BUildMode == "Shipping" or BUildMode == "Test":
                    if dict_file["name"] == f'AClient-IOS-{BUildMode}.dSYM.zip':
                        log.info("IOS的文件", dict_file["fullName"])
                        return dict_file["fullName"]

                elif BUildMode == "Development":
                    if dict_file["name"] == "AClient.dSYM.zip":
                        log.info("IOS的Development文件", dict_file["fullName"])
                        return dict_file["fullName"]

    # 获取所有的构建产物
    def get_all_product(self, piplineUrl):
        all_parameter = All_parameter()
        projectId = all_parameter.projectId
        access_token = all_parameter.access_token
        pageSize = "100"

        url_infos = piplineUrl.split("/")
        for info in url_infos:
            if info.startswith("p-"):
                pipelineId = info
                continue
            if info.startswith("b-"):
                buildId = info

        print("pipline_id: " + pipelineId)
        print("build_id: " + buildId)
        url = f"https://devops.apigw.o.woa.com/prod/v3/apigw-user/projects/{projectId}/artifactories?access_token={access_token}&pipelineId={pipelineId}&buildId={buildId}&pageSize={pageSize}"
        log.info("url", url)
        response = requests.get(url, headers=self.get_header())
        log.info(response.status_code)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            if len(response_data["data"]["records"]) > 0:
                product = response_data["data"]["records"]
                print("product", product)
                return product
            else:
                log.info("None product, please check your piplineId and buildId")
                return False

    # 获取最原始的下载链接
    def get_build_info(self):
        if not self.build_info:
            app_version = self.get_param("APPVersion")
            log.info("app_version", app_version)
            # app_version = "0.2.628.14"
            # Android
            # app_version = "0.2.625.117"
            # app_version = "0.1.0.8928"
            self.build_info = patch_utils.get_build_info_by_version(app_version)
        return self.build_info

    def get_header(self):
        all_parameter = All_parameter()
        bk_app_code = all_parameter.bk_app_code
        bk_app_secret = all_parameter.bk_app_secret
        access_token = all_parameter.access_token
        bk_username = all_parameter.user_id
        x_bkapi_authorization = {"bk_app_code": bk_app_code,
                                 "bk_app_secret": bk_app_secret,
                                 "access_token": access_token, "bk_username": bk_username}
        headers = {'content-type': 'application/json',
                   'X-DEVOPS-UID': '{X-DEVOPS-UID}',
                   'X-Bkapi-Authorization': json.dumps(x_bkapi_authorization)
                   }
        return headers

    # 获取用户的下载链接
    def get_user_download_url(self, get_diffence_target):
        all_parameter = All_parameter()
        projectId = all_parameter.projectId
        access_token = all_parameter.access_token
        artifactoryType = "CUSTOM_DIR"
        download_url = f"http://devops.apigw.o.oa.com/prod/v2/apigw-user/artifactories/projects/{projectId}/thirdPartyDownloadUrl" \
                       f"?access_token={access_token}&artifactoryType={artifactoryType}&path={get_diffence_target}"
        log.info("download_url", download_url)
        response = requests.get(download_url, headers=self.get_header())
        if response.status_code == 200:
            response_data = json.loads(response.text)
            url = response_data["data"][0]
            log.info(url)

            return url

    # 开始下载
    def download_largefile_by_package(self, url, local_path, file_name):
        import requests
        log.info("downloading :" + url)
        res = requests.get(url, stream=True)
        log.info(res.status_code, res.headers)
        total_size = int(res.headers['Content-Length'])
        download_size = 0
        count = 0
        local_path = r"%s" % (os.path.join(local_path, file_name))
        log.info("local_path", local_path)
        with open(local_path, "wb") as package_file:
            for chunk in res.iter_content(chunk_size=1024):
                count = count + 1
                if chunk:
                    if count > 1024:
                        download_size += 1
                        count = 0
                        log.info("下载中，泡杯茶等等。。。。。。%sMB" % download_size)
                    package_file.write(chunk)
        return package_file


class All_parameter:

    def __init__(self):
        self.bk_app_code = "gngame-new"
        self.bk_app_secret = "djf4tgGCTYrclQQmNAEZWpnXUfx4leeY43Mb"
        self.projectId = "gngame"
        self.user_id = "v_chliangxu"
        self.refresh_token = "mDBmnlzSs6e2KmwKoteoqXhGYooHkM"
        self.access_token = "MKg5NcVmliYgpmjUFizJU4ePF7m9PI"
        self.bk_tickets = "3a-311ZNGtrAhcx_Qa0-3KQPasQckWxVq8RbKJnektU"


# 刷新access_token
def refresh_access_token():
    url = 'http://apigw.o.oa.com/auth_api/refresh_token/'
    app_code = All_parameter().bk_app_code
    print("app", app_code)
    refresh_token = All_parameter().refresh_token
    print("refresh_token", refresh_token)
    env_name = "test"
    grant_type = "refresh_token"
    data = {"app_code": app_code, "refresh_token": refresh_token, "env_name": env_name, "grant_type": grant_type}
    print(type(data))
    response = requests.get(url, params=data)
    log.info("response", response)

    if response.status_code == 200:
        print("-------")
        response_data = json.loads(response.text)
        data = response_data
        log.info("data", data)


def get_access_token():
    import requests

    ret = requests.post(
        'http://apigw.o.oa.com/auth_api/token/',
        data={
            'app_code': 'gngame-new',
            'app_secret': 'djf4tgGCTYrclQQmNAEZWpnXUfx4leeY43Mb',
            'env_name': 'prod',
            'grant_type': 'authorization_code',
            'rtx': 'v_chliangxu',
            'bk_ticket': '3a-311ZNGtrAhcx_Qa0-3ImjFddRgYbW2ABu54iHZEU'
        }
    )
    print(ret, ret)
    response_data = json.loads(ret.text)
    data = response_data
    log.info("data", data)

# if __name__ == '__main__':
# refresh_access_token()
# get_access_token()
