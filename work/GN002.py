import re
import requests
import json
import time
import random
# import CreateDsBranch as CDB
import urllib.parse
import subprocess

class ElementInfo:  # 插件信息

    def __init__(self):
        self.name = ''
        self.status = ''
        self.plugin_element_id = ''
        self.execute_count = ''

    def set_name(self, name):
        self.name = name

    def set_id(self, element_id):
        self.plugin_element_id = element_id

    def set_status(self, status):
        self.status = status

    def set_execute_count(self, execute_count):
        self.execute_count = execute_count


class StageInfo:
    def __init__(self):
        self.name = ''
        self.status = ''
        self.stage_element_id = ''
        self.stage_contains = ''

    def set_name(self, name):
        self.name = name

    def set_id(self, element_id):
        self.stage_element_id = element_id

    def set_status(self, status):
        self.status = status

    def set_stage_contains(self, contains):
        self.stage_contains = contains


class PipelineInfo:
    def __init__(self):
        self.projectId = ''
        self.pipelineId = ''
        self.pipelineBuildList = ''
        self.accessToken = ''
        self.name = ''
        self.refreshToken = 'OjvYexPqfJ3MMt8NNpdhYpgt8FhP1q'

    def set_project_id(self, project_id):
        self.projectId = project_id

    def set_custom_name(self, name):
        self.name = name

    def set_pipeline_id(self, pipeline_id):
        self.pipelineId = pipeline_id

    def set_access_token(self):
        ret = requests.get(
            'http://apigw.o.oa.com/auth_api/refresh_token/',
            params={
                'app_code': 'get-build-links',
                'refresh_token': self.refreshToken,
                'env_name': 'test',
                'grant_type': 'refresh_token'
            }
        )
        ret_json = ret.json()
        # print(ret_json)
        self.accessToken = ret_json['data']['access_token']

    def set_access_token_old(self):
        ret = requests.post(
            'http://apigw.o.oa.com/auth_api/token/',
            data={
                'app_code': 'get-build-links',
                'app_secret': '7ECoqWRFVSkI61ZmmQnFYe1tBIJQbDnmWqlDaL0JFAhoCBTqSj',
                'env_name': 'test',
                'grant_type': 'authorization_code',
                'rtx': 'v_xinnwan',
                'bk_ticket': 'qoN9URLA-MhNDIadGHOksvpFvQx-7E-YABz0Vv8GVQ8'
            }
        )
        ret_json = ret.json()
        # print(ret_json)
        # print(type(ret_json['data']['access_token']))
        self.accessToken = ret_json['data']['access_token']
        # self.accessToken = 'BXqS1HRjyqa86XME9PBMGiEVTkv59O'

    def set_pipeline_build_list(self):
        request_url = "https://devops.apigw.o.woa.com/prod/v4/apigw-user/projects/" + self.projectId + "/build_histories?pipelineId=" + self.pipelineId + '&pageSize=40'
        access_token = self.accessToken
        # print(access_token)
        x_bkapi_authorization = {"bk_app_code": "get-build-links",
                                 "bk_app_secret": "7ECoqWRFVSkI61ZmmQnFYe1tBIJQbDnmWqlDaL0JFAhoCBTqSj",
                                 "access_token": access_token, "bk_username": "v_xinnwan"}
        headers = {'content-type': 'application/json',
                   'X-DEVOPS-UID': '{X-DEVOPS-UID}',
                   'X-Bkapi-Authorization': json.dumps(x_bkapi_authorization)
                   }
        try:
            response = requests.get(request_url, headers=headers)
            # print(response)
            if response:
                ret_json = response.json()
                # print(ret_json)
                self.pipelineBuildList = ret_json
                # return ret_json
        except requests.exceptions.ConnectionError:
            print('网络错误，请重新运行')


class SingPipelineInfo:
    def __init__(self):
        self.projectId = ''
        self.pipelineId = ''
        self.buildId = ''
        self.artifactList = ''
        self.pipelineUrl = ''
        self.buildNum = ''
        self.appVersion = ''
        self.startTime = 0
        self.singlePipelineInfo = ''
        self.name = ''
        self.buildTime = ''
        self.queryIntervalTime = 3600
        self.dsMessageMore = ''
        self.accessToken = ''
        self.plugin_log = ''
        self.ds_branch = ''
        self.refreshToken = 'OjvYexPqfJ3MMt8NNpdhYpgt8FhP1q'
        self.qs_url = ''
        self.package_path = ''

    def set_access_token(self):
        ret = requests.get(
            'http://apigw.o.oa.com/auth_api/refresh_token/',
            params={
                'app_code': 'get-build-links',
                'refresh_token': self.refreshToken,
                'env_name': 'test',
                'grant_type': 'refresh_token'
            }
        )
        ret_json = ret.json()
        # print(ret_json)
        self.accessToken = ret_json['data']['access_token']
        return self.accessToken

    def set_access_token_old(self):
        ret = requests.post(
            'http://apigw.o.oa.com/auth_api/token/',
            data={
                'app_code': 'get-build-links',
                'app_secret': '7ECoqWRFVSkI61ZmmQnFYe1tBIJQbDnmWqlDaL0JFAhoCBTqSj',
                'env_name': 'test',
                'grant_type': 'authorization_code',
                'rtx': 'v_xinnwan',
                'bk_ticket': 'qoN9URLA-MhNDIadGHOksvpFvQx-7E-YABz0Vv8GVQ8'
            }
        )
        ret_json = ret.json()
        # print(ret_json)
        # print(type(ret_json['data']['access_token']))
        self.accessToken = ret_json['data']['access_token']
        # self.accessToken = 'BXqS1HRjyqa86XME9PBMGiEVTkv59O'

    # 600单位是秒
    def set_query_interval_time(self, interval_time=3600):
        ret_android = re.findall(r'Android', self.name)
        ret_ios = re.findall(r'IOS', self.name)
        ret_ds = re.findall(r'DS', self.name)
        if (ret_android):
            self.queryIntervalTime = interval_time * 0.5
        if (ret_ios):
            self.queryIntervalTime = interval_time * 0.5
        if (ret_ds):
            self.queryIntervalTime = interval_time * 0.5

    def set_name(self, name):
        self.name = name

    def set_build_time(self):
        self.buildTime = time.strftime('%Y-%m-%d %H:%M', time.localtime(self.startTime / 1000))
        return self.buildTime

    def set_build_num(self):
        self.buildNum = self.singlePipelineInfo['buildNum']

    def set_pipeline_url(self):
        self.pipelineUrl = 'http://devops.woa.com/console/pipeline/' + self.projectId + '/' + self.pipelineId + '/detail/' + self.buildId
        # print(self.pipelineUrl)

    def get_pipeline_url(self):
        return self.pipelineUrl

    def set_project_id(self, project_id):
        self.projectId = project_id

    def set_pipeline_build_info(self, build_info):
        # print(build_info)
        self.singlePipelineInfo = build_info

    def set_start_time(self):
        self.startTime = self.singlePipelineInfo['startTime']

    def set_pipeline_id(self, pipeline_id):
        self.pipelineId = pipeline_id

    def set_build_id(self):
        self.buildId = self.singlePipelineInfo['id']

    def set_artifact_list(self):
        if re.findall(r'artifactList', str(self.singlePipelineInfo)):
            self.artifactList = self.singlePipelineInfo['artifactList']
        # print(self.artifactList)

    def set_app_version(self):
        # print(self.artifactList)
        for artifact in self.artifactList:
            ret_android = re.findall(r'Android', self.name)
            ret_ios = re.findall(r'IOS', self.name)
            ret_ds = re.findall(r'DS', self.name)
            ret_winclient = re.findall(r'Win', self.name)
            if (ret_android):
                package_str = re.findall(r'^GNYX_Android_Shipping.*\.apk', artifact['name'])
                # print(package_str)
                package_path_str = re.findall(r'Shipping.*\.apk', artifact['path'])
                self.package_path = artifact['path']
                # print(artifact['name'])
                # print(self.artifactList)
                # print(len(self.artifactList))

                if (package_str):
                    # print(package_str)
                    package_version = package_str[0]
                    self.appVersion = re.findall(r'\d+\.\d+\.\d+.\d+', package_version)[0]
                    break
            if (ret_ios):
                package_str = re.findall(r'Shipping.*\.ipa', artifact['name'])
                self.package_path = artifact['path']
                if (package_str):
                    package_version = package_str[0]
                    self.appVersion = re.findall(r'\d+\.\d+\.\d+.\d+', package_version)[0]
                    break
            if (ret_ds):
                self.set_access_token()
                self.get_user_build_detail()
                self.get_plugins_element_id()
                self.set_ds_version()
                # self.create_new_ds_branch()
                break
            if (ret_winclient):
                package_str = re.findall(r'.*\.gz', artifact['name'])
                if (package_str):
                    package_version = package_str[0]
                    self.appVersion = re.findall(r'\d+\.\d+\.\d+.\d+', package_version)[0]
                    break
        # print(self.appVersion)

    def set_qs_url(self):
        print(self.artifactList)
        for artifact in self.artifactList:
            ret_android = re.findall(r'Android', self.name)
            ret_ios = re.findall(r'IOS', self.name)
            if (ret_android):
                short_url = artifact['shortUrl']
                if (short_url):
                    self.qs_url = short_url
                    break

            if (ret_ios):
                short_url = artifact['shortUrl']
                if (short_url):
                    self.qs_url = short_url
                    break


    def get_v4_user_artifactory_appDownloadUrl(self):
        # import requests_cache
        import time
        # requests_cache.install_cache()
        # requests_cache.clear()
        # session = requests_cache.CachedSession()  # 创建缓存会话
        # from shell import shell
        path = urllib.parse.quote(self.package_path)
        # print(self.appVersion)
        # shipping_replace_str = 'Development_Stable_' + self.appVersion + '_Less_PSO_U_arm64_32_signed'
        # shipping_replace_str_after = 'Shipping_Stable_' + self.appVersion + '_Less_PSO_U_arm64_32_1TuoN_signed'
        # path = path.replace('Development', 'Shipping')
        # path = path.replace(shipping_replace_str, shipping_replace_str_after)
        # print(path)
        # path = '/' + self.pipelineId + '/' + self.buildId + '/' + self.package_path
        # request_url = "https://devops.apigw.o.woa.com/prod/v4/apigw-user/projects/" + self.projectId + "/artifactories/app_download_url?artifactoryType=CUSTOM_DIR&pipelineId=" + self.pipelineId + "&buildId=" + self.buildId
        # request_url = "https://devops.apigw.o.woa.com/prod/v4/apigw-user/projects/" + self.projectId + "/artifactories/app_download_url?artifactoryType=CUSTOM_DIR&path=/[P4_SVN][冒烟包]Android/464/Development/GNYX_Android_Development_Stable_0.2.648.74_Less_arm64_32_signed.apk"

        # request_url = "https://devops.apigw.o.woa.com/prod/v4/apigw-user/projects/" + self.projectId + "/artifactories/app_download_url?artifactoryType=CUSTOM_DIR&path=" + path
        request_url =  "https://devops.apigw.o.woa.com/prod/v4/apigw-user/projects/" + self.projectId + "/artifactories/app_download_url?artifactoryType=CUSTOM_DIR&path=" + path
        # print(request_url)
        # time.sleep(4)
        access_token = self.set_access_token()
        # print(access_token)
        x_bkapi_authorization = {"bk_app_code": "get-build-links",
                                 "bk_app_secret": "7ECoqWRFVSkI61ZmmQnFYe1tBIJQbDnmWqlDaL0JFAhoCBTqSj",
                                 "access_token": access_token, "bk_username": "v_xinnwan"}
        headers = {'content-type': 'application/json',
                   'X-DEVOPS-UID': '{X-DEVOPS-UID}',
                   'X-Bkapi-Authorization': json.dumps(x_bkapi_authorization),
                   }

        # curl_cmd = "curl -X GET " + request_url + " -H 'content-type: application/json' -H 'X-DEVOPS-UID :{X-DEVOPS-UID}' -H 'X-Bkapi-Authorization:" + json.dumps(x_bkapi_authorization) + "'"
        # print(curl_cmd)
        # curl = shell(curl_cmd)
        # print(curl.output())
        try:
            # time.sleep(2)
            # response = session.get(request_url, headers=headers)
            response = requests.get(request_url, headers=headers)

            # print(response)
            if response:
                ret_json = response.json()
                # print(ret_json)
                self.qs_url = ret_json['data']['url']
                # print(self.qs_url)

                # print(len(ret_json))
                # return ret_json
        except requests.exceptions.ConnectionError:
            print('网络错误，请重新运行')





    def get_user_build_detail(self):
        request_url = "https://devops.apigw.o.woa.com/prod/v4/apigw-user/projects/afgame/build_histories?pipelineId=" + self.pipelineId + '&pageSize=40'
        request_url = "http://devops.apigw.o.oa.com/prod/v2/apigw-user/artifactories/projects/afgame/userDownloadUrl?access_token={access_token}&amp;artifactoryType={artifactoryType}&amp;path={path}"
        request_url = "https://devops.apigw.o.woa.com/prod/v4/apigw-user/projects/" + self.projectId + "/build_detail?pipelineId=" + self.pipelineId + "&buildId=" + self.buildId
        access_token = self.accessToken
        # print(access_token)
        x_bkapi_authorization = {"bk_app_code": "get-build-links",
                                 "bk_app_secret": "7ECoqWRFVSkI61ZmmQnFYe1tBIJQbDnmWqlDaL0JFAhoCBTqSj",
                                 "access_token": access_token, "bk_username": "v_xinnwan"}
        headers = {'content-type': 'application/json',
                   'X-DEVOPS-UID': '{X-DEVOPS-UID}',
                   'X-Bkapi-Authorization': json.dumps(x_bkapi_authorization)
                   }

        try:
            response = requests.get(request_url, headers=headers)
            # print(response)
            if response:
                ret_json = response.json()
                # print(ret_json)
                # print(len(ret_json))
                self.userBuildDetail = ret_json
                # return ret_json
        except requests.exceptions.ConnectionError:
            print('网络错误，请重新运行')

    def get_user_log_download(self, plugin_element_id, execute_count):
        # https://devops.apigw.o.woa.com/prod/v4/apigw-user/projects/{projectId}/logs/download_logs   https://bkapigw.woa.com/docs/apigw-api/devops/apigw-api/devops/prod/v4_user_log_download/doc?stage=prod
        request_url = "https://devops.apigw.o.woa.com/prod/v4/apigw-user/projects/" + self.projectId + "/logs/download_logs?pipelineId=" + self.pipelineId + "&buildId=" + self.buildId + "&tag=" + str(
            plugin_element_id) + "&executeCount=" + str(execute_count)
        access_token = self.accessToken
        x_bkapi_authorization = {"bk_app_code": "get-build-links",
                                 "bk_app_secret": "7ECoqWRFVSkI61ZmmQnFYe1tBIJQbDnmWqlDaL0JFAhoCBTqSj",
                                 "access_token": access_token, "bk_username": "v_xinnwan"}
        headers = {'content-type': 'application/json',
                   'X-DEVOPS-UID': '{X-DEVOPS-UID}',
                   'X-Bkapi-Authorization': json.dumps(x_bkapi_authorization)
                   }

        try:
            response = requests.get(request_url, headers=headers)

            if response:
                response.encoding = 'utf-8'
                # print(response.text)
                # ret_json = response.json()
                # print(ret_json)
                ret_tex = response.text
                self.plugin_log = ret_tex

        except requests.exceptions.ConnectionError:
            print('网络错误，请重新运行')

    def get_plugins_element_id(self, plugins_element_name='写入ds版本号标记'):
        for stage_element in self.userBuildDetail['data']['model']['stages']:
            stageInfo = StageInfo()
            stageInfo.set_stage_contains(stage_element['containers'])
            stageInfo.set_name(stageInfo.stage_contains[0]['name'])
            # print(len(stageInfo.stage_contains))
            for job in stageInfo.stage_contains:
                # print(job)
                for plugins_element in job['elements']:
                    elementInfo = ElementInfo()
                    elementInfo.set_name(plugins_element['name'])
                    if re.findall(plugins_element_name, elementInfo.name):
                        elementInfo.set_id(plugins_element['id'])
                        elementInfo.set_execute_count(plugins_element['executeCount'])
                        # print(elementInfo.plugin_element_id)
                        # print(elementInfo.execute_count)
                        self.get_user_log_download(elementInfo.plugin_element_id, elementInfo.execute_count)
                        return

    def set_ds_version(self):
        pattern_str = r"\[DS_Information.*"
        list_pat = re.findall(pattern_str, self.plugin_log)
        ds_version_pat = r"\d+\.\d+\.\d+\.\d+"
        ds_branch_pat = r"DSBranch.*"
        # print("set_ds_version")
        for match_pat in list_pat:
            match_pat = match_pat.replace('[DS_Information] ', '')
            ds_version_match = re.findall(ds_version_pat, match_pat)
            ds_branch_match = re.findall(ds_branch_pat, match_pat)
            if ds_version_match:
                # print(ds_version_match[0])
                self.appVersion = ds_version_match[0]
            if ds_branch_match:
                # print(ds_branch_match[0].replace('DSBranch:', ''))
                self.ds_branch = ds_branch_match[0].replace('DSBranch:', '')

            self.dsMessageMore = match_pat + '\n' + self.dsMessageMore

    def create_new_ds_branch(self):
        ProjectId = '210954'  # AGame_DS_ProjectId
        # branch_name = 'Dev_V1.3'
        branch_name = self.ds_branch
        data_title = time.strftime('%Y{Y}%m{m}%d{d}').format(Y='', m='', d='')
        new_branch_name = "xn_ds" + data_title + '01'
        create_branch_version = self.appVersion
        if CDB.execute_create_branch(ProjectId, branch_name, create_branch_version, new_branch_name):
            self.dsMessageMore = self.dsMessageMore + "NewCreateDSBranchName:\n" + new_branch_name

    # def __str__(self):
    #     # if re.findall(r'DS', self.name):
    #     #     return self.name + '\n' + '[流水线：链接]' + '(' + self.pipelineUrl + ')' + '\n构建号：#' + str(
    #     #         self.buildNum) + '\n构建时间：' + self.buildTime + '\n版本号: ' + self.appVersion + '\n\n' + self.dsMessageMore
    #     # else:
    #     #     return self.name + '\n' + '[流水线：链接]' + '(' + self.pipelineUrl + ')' + '\n构建号：#' + str(
    #     #         self.buildNum) + '\n构建时间：' + self.buildTime + '\n版本号: ' + self.appVersion + '\n'
    #     return self.name + '\n' + '[流水线：链接]' + '(' + self.pipelineUrl + ')' + '\n构建号：#' + str(
    #         self.buildNum) + '\n构建时间：' + self.buildTime + '\n版本号: ' + self.appVersion + '\n'
    def __str__(self):
        if re.findall(r'DS', self.name):
            return self.name + '\n' + '[流水线：链接]' + '(' + self.pipelineUrl + ')' + '\n构建号：#' + str(
                self.buildNum) + '\n构建时间：' + self.buildTime + '\n版本号: ' + self.appVersion + '\n'
        else:
            return self.name + '\n' + '[流水线：链接]' + '(' + self.pipelineUrl + ')' + '\n' + '[二维码：链接]'+ '(' + self.qs_url + ')'  + '\n构建号：#' + str(
                self.buildNum) + '\n构建时间：' + self.buildTime + '\n版本号: ' + self.appVersion + '\n'
            # return self.name + '\n' + '[流水线：链接]' + '(' + self.pipelineUrl + ')'  + '\n构建号：#' + str(
            #     self.buildNum) + '\n构建时间：' + self.buildTime + '\n版本号: ' + self.appVersion + '\n'


def get_information(project_id, pipeline_id_dict, need_query_build_time):
    # pipeline_num = len(pipeline_id_dict)
    single_pipeline_list = []
    if need_query_build_time != '':
        this_year = time.strftime("%Y-", time.localtime())
        query_build_time = this_year + need_query_build_time
        query_build_time_float = time.mktime(time.strptime(query_build_time, '%Y-%m-%d %H:%M'))
        # print(query_build_time_float)

    for pipeline_custom_name in pipeline_id_dict.keys():
        # print(pipeline_id_dict[pipeline_custom_name])
        build_time = ''
        pipelineInfo = PipelineInfo()
        pipelineInfo.set_access_token()
        pipelineInfo.set_project_id(project_id)
        pipelineInfo.set_custom_name(pipeline_custom_name)
        pipelineInfo.set_pipeline_id(pipeline_id_dict[pipeline_custom_name])
        pipelineInfo.set_pipeline_build_list()
        build_count = pipelineInfo.pipelineBuildList['data']['count']
        # print(build_count)
        if need_query_build_time != '':
            for i in range(build_count):
                # print(i)
                if i > 38:
                    break
                singlePipelineInfo = SingPipelineInfo()
                singlePipelineInfo.set_pipeline_build_info(pipelineInfo.pipelineBuildList['data']['records'][i])
                singlePipelineInfo.set_start_time()
                # print(singlePipelineInfo.startTime)
                singlePipelineInfo.set_name(pipeline_custom_name)
                singlePipelineInfo.set_query_interval_time()
                if abs(singlePipelineInfo.startTime / 1000 - query_build_time_float) < singlePipelineInfo.queryIntervalTime:
                    singlePipelineInfo.set_name(pipeline_custom_name)
                    singlePipelineInfo.set_project_id(project_id)
                    singlePipelineInfo.set_pipeline_id(pipeline_id_dict[pipeline_custom_name])
                    singlePipelineInfo.set_build_id()
                    singlePipelineInfo.set_pipeline_url()
                    singlePipelineInfo.set_artifact_list()
                    singlePipelineInfo.set_app_version()
                    singlePipelineInfo.set_build_num()
                    build_time = singlePipelineInfo.set_build_time()
                    # singlePipelineInfo.set_qs_url()
                    singlePipelineInfo.get_v4_user_artifactory_appDownloadUrl()
                    single_pipeline_list.append(singlePipelineInfo)
                    break

        else:
            singlePipelineInfo = SingPipelineInfo()
            singlePipelineInfo.set_pipeline_build_info(pipelineInfo.pipelineBuildList['data']['records'][0])
            singlePipelineInfo.set_start_time()
            singlePipelineInfo.set_name(pipeline_custom_name)
            singlePipelineInfo.set_project_id(project_id)
            singlePipelineInfo.set_pipeline_id(pipeline_id_dict[pipeline_custom_name])
            singlePipelineInfo.set_build_id()
            singlePipelineInfo.set_pipeline_url()
            singlePipelineInfo.set_artifact_list()
            singlePipelineInfo.set_app_version()
            singlePipelineInfo.set_build_num()
            build_time = singlePipelineInfo.set_build_time()
            # singlePipelineInfo.set_qs_url()
            singlePipelineInfo.get_v4_user_artifactory_appDownloadUrl()

            single_pipeline_list.append(singlePipelineInfo)

    # data_title = time.strftime('%m{m}%d{d}').format(m='月', d='日')
    # data_title_num = time.strftime('%Y{Y}%m{m}%d{d}').format(Y='', m='', d='')

    name = (build_time.split(' ')[0]).split('-')
    data_title = name[1] + "月" + name[2] + "日"


    # append_info = '【GN_Dev_Stable】\n' + data_title + 'GN冒烟包版本信息' + '\n' + 'Stable分支：AClient: GNYX_Stable_' + data_title_num + '; AEngine: GNYX_Stable_' + data_title_num + '; AClient_Content: GNYX_Stable_' + data_title_num
    append_info = '【GN_分支_GN002】\n' + data_title + ' GN002冒烟包版本信息'
    print(append_info)
    for single_pipeline in single_pipeline_list:
        print(single_pipeline)

    # print("服务器：主干_冒烟服(Dev)")
    print("服务器：GN002分支_稳定服(Dev)")
    # print("服务器：主干_稳定服(Shipping)")
    # print("[美术策划“拉取编辑器”请使用“UGS工具”](https://doc.weixin.qq.com/doc/w3_ABgAPAZ8ACoK00jKpVEQKut1wWg1v?scode=AJEAIQdfAAo45j2suMABgAPAZ8ACo&version=4.1.0.6015&platform=win)")
    return single_pipeline_list


def send_request_bot_planning_developping_group_project(content_all, mentioned_list=''):
    color_list_second = ['navy', 'pink', 'orange', 'olive', 'yellow', 'gray', 'gray', 'olive']
    color_list_third = ['navy', 'pink', 'orange', 'olive', 'yellow', 'gray', 'gray', 'olive', 'silver', 'red', 'maroon',
                        'green', 'maroon', 'olive', 'pink', 'teal', 'red']

    number_color = random.randint(0, 16)
    number_color2 = random.randint(0, 6)

    robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=77784edf-3a2c-4868-9e53-b22797c4fe94'  # 大群
    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c7787c75-ba14-461a-a6d4-3a2777785718'

    # robot_url = 'http://in.qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34895f6c-ac79-41fd-9014-023c58515ced&save=0'
    # robot_url = 'http://9.140.150.207:8777/send_build_info'
    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6e7688ef-5eca-41db-9ec4-0f1f5d677675'         #版本构建小群
    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=55520ba1-9e20-4355-84e8-c321952aa0c5'         #对外包构建参数对齐群
    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=976e0e43-11fd-4853-b7aa-d97e88483d48'         #每日冒烟小群-yonggangwei/yuefengliu
    mentioned_list = ['<@' + str(i) + '>' for i in mentioned_list]
    mentioned_list_str = ','.join(mentioned_list)
    data_title = time.strftime('%m{m}%d{d}').format(m='月', d='日')
    ugc_game_name = '【GN_P4_SVN】\n' + data_title + 'GN冒烟包版本信息'
    # ugc_game_name = '【GN_P4_SVN】\n' + '04月11日GN冒烟包版本信息(仅测试推送接口,勿下载)'

    # content_all = "<font color=" + color_list_second[
    #     number_color2] + " >" + ugc_game_name + "</font>" + '\n>' + "<font color=" + color_list_third[
    #                   number_color] + ">" + content_all + "</font>" + mentioned_list_str \
    #               + "服务器：主干_稳定服(Dev)\n" + "服务器：主干_稳定服(Shipping)\n" \
    #               + "[美术策划“拉取编辑器”请使用“UGS工具”](https://doc.weixin.qq.com/doc/w3_ABgAPAZ8ACoK00jKpVEQKut1wWg1v?scode=AJEAIQdfAAo45j2suMABgAPAZ8ACo&version=4.1.0.6015&platform=win)"

    content_all = "<font color=" + color_list_second[
        number_color2] + " >" + ugc_game_name + "</font>" + '\n>' + content_all + mentioned_list_str \
                  + "服务器：分支_稳定服(Dev)\n"  \
                  + "[美术策划“拉取编辑器”请使用“UGS工具”](https://doc.weixin.qq.com/doc/w3_ABgAPAZ8ACoK00jKpVEQKut1wWg1v?scode=AJEAIQdfAAo45j2suMABgAPAZ8ACo&version=4.1.0.6015&platform=win)"

    send_data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content_all,
        }
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url=robot_url, headers=headers, json=send_data)

def send_request_bot_planning_developping_group_build(content_all, mentioned_list=''):
    color_list_second = ['navy', 'pink', 'orange', 'olive', 'yellow', 'gray', 'gray', 'olive']
    color_list_third = ['navy', 'pink', 'orange', 'olive', 'yellow', 'gray', 'gray', 'olive', 'silver', 'red', 'maroon',
                        'green', 'maroon', 'olive', 'pink', 'teal', 'red']

    number_color = random.randint(0, 16)
    number_color2 = random.randint(0, 6)

    robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5257c2a2-5882-496a-bf0d-c74eb7cd90c0'  # 大群
    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c7787c75-ba14-461a-a6d4-3a2777785718'

    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=e6f8386c-22c3-4c13-9b81-9dcdd81c2ab0'  # 【高能英雄】构建问题讨论群
    # robot_url = 'http://in.qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34895f6c-ac79-41fd-9014-023c58515ced&save=0'
    # robot_url = 'http://9.140.150.207:8777/send_build_info'
    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6e7688ef-5eca-41db-9ec4-0f1f5d677675'         #版本构建小群
    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=55520ba1-9e20-4355-84e8-c321952aa0c5'         #对外包构建参数对齐群
    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=976e0e43-11fd-4853-b7aa-d97e88483d48'         #每日冒烟小群-yonggangwei/yuefengliu
    mentioned_list = ['<@' + str(i) + '>' for i in mentioned_list]
    mentioned_list_str = ','.join(mentioned_list)
    data_title = time.strftime('%m{m}%d{d}').format(m='月', d='日')
    ugc_game_name = '【GN_P4_SVN】\n' + data_title + 'GN冒烟包版本信息'
    # ugc_game_name = '【GN_P4_SVN】\n' + '04月11日GN冒烟包版本信息(仅测试推送接口,勿下载)'

    # content_all = "<font color=" + color_list_second[
    #     number_color2] + " >" + ugc_game_name + "</font>" + '\n>' + "<font color=" + color_list_third[
    #                   number_color] + ">" + content_all + "</font>" + mentioned_list_str \
    #               + "服务器：主干_稳定服(Dev)\n" + "服务器：主干_稳定服(Shipping)\n" \
    #               + "[美术策划“拉取编辑器”请使用“UGS工具”](https://doc.weixin.qq.com/doc/w3_ABgAPAZ8ACoK00jKpVEQKut1wWg1v?scode=AJEAIQdfAAo45j2suMABgAPAZ8ACo&version=4.1.0.6015&platform=win)"

    content_all = "<font color=" + color_list_second[
        number_color2] + " >" + ugc_game_name + "</font>" + '\n>' + content_all + mentioned_list_str \
                  + "服务器：分支_稳定服(Dev)\n"  \
                  + "[美术策划“拉取编辑器”请使用“UGS工具”](https://doc.weixin.qq.com/doc/w3_ABgAPAZ8ACoK00jKpVEQKut1wWg1v?scode=AJEAIQdfAAo45j2suMABgAPAZ8ACo&version=4.1.0.6015&platform=win)"

    send_data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content_all,
        }
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url=robot_url, headers=headers, json=send_data)

def send_request_bot_planning_developping_group_build_problem(content_all, mentioned_list=''):
    color_list_second = ['navy', 'pink', 'orange', 'olive', 'yellow', 'gray', 'gray', 'olive']
    color_list_third = ['navy', 'pink', 'orange', 'olive', 'yellow', 'gray', 'gray', 'olive', 'silver', 'red', 'maroon',
                        'green', 'maroon', 'olive', 'pink', 'teal', 'red']

    number_color = random.randint(0, 16)
    number_color2 = random.randint(0, 6)

    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5257c2a2-5882-496a-bf0d-c74eb7cd90c0'  # 大群
    robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=e6f8386c-22c3-4c13-9b81-9dcdd81c2ab0'  # 【高能英雄】构建问题讨论群
    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c7787c75-ba14-461a-a6d4-3a2777785718'

    # robot_url = 'http://in.qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34895f6c-ac79-41fd-9014-023c58515ced&save=0'
    # robot_url = 'http://9.140.150.207:8777/send_build_info'
    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6e7688ef-5eca-41db-9ec4-0f1f5d677675'         #版本构建小群
    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=55520ba1-9e20-4355-84e8-c321952aa0c5'         #对外包构建参数对齐群
    # robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=976e0e43-11fd-4853-b7aa-d97e88483d48'         #每日冒烟小群-yonggangwei/yuefengliu
    mentioned_list = ['<@' + str(i) + '>' for i in mentioned_list]
    mentioned_list_str = ','.join(mentioned_list)
    data_title = time.strftime('%m{m}%d{d}').format(m='月', d='日')
    ugc_game_name = '【GN_P4_SVN】\n' + data_title + 'GN冒烟包版本信息'
    # ugc_game_name = '【GN_P4_SVN】\n' + '04月11日GN冒烟包版本信息(仅测试推送接口,勿下载)'

    # content_all = "<font color=" + color_list_second[
    #     number_color2] + " >" + ugc_game_name + "</font>" + '\n>' + "<font color=" + color_list_third[
    #                   number_color] + ">" + content_all + "</font>" + mentioned_list_str \
    #               + "服务器：主干_稳定服(Dev)\n" + "服务器：主干_稳定服(Shipping)\n" \
    #               + "[美术策划“拉取编辑器”请使用“UGS工具”](https://doc.weixin.qq.com/doc/w3_ABgAPAZ8ACoK00jKpVEQKut1wWg1v?scode=AJEAIQdfAAo45j2suMABgAPAZ8ACo&version=4.1.0.6015&platform=win)"

    content_all = "<font color=" + color_list_second[
        number_color2] + " >" + ugc_game_name + "</font>" + '\n>' + content_all + mentioned_list_str \
                  + "服务器：分支_稳定服(Dev)\n"  \
                  + "[美术策划“拉取编辑器”请使用“UGS工具”](https://doc.weixin.qq.com/doc/w3_ABgAPAZ8ACoK00jKpVEQKut1wWg1v?scode=AJEAIQdfAAo45j2suMABgAPAZ8ACo&version=4.1.0.6015&platform=win)"

    send_data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content_all,
        }
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url=robot_url, headers=headers, json=send_data)



if __name__ == '__main__':
    # https://devops.woa.com/console/pipeline/afgame/p-a2b6d794d23f48eab24dc78f4304f082/history   afgame是projectid,
    # pipelineId是p-a2b6d794d23f48eab24dc78f4304f082
    project_id = 'gngame'
    # pipeline_id_dict = {
    #     'Android': 'p-e99b004654974079a19600843ca8276e',
    #     'IOS': 'p-8e677110a871423da93c7ac30c630539',
    #     # 'WinClient': 'p-efd73cc2a661486a92d09e66588231ec',
    #     'DS': 'p-3814917ef7494953a2604c8c83d3553c',
    #     '【ASAN】IOS': 'p-d7479389af4c41c797d84084fbeafb6f',
    #     '【ASAN】Android': 'p-1ea83f82e07d41fc95bb3ff6ab2571a5',
    #     '【ASAN】DS': 'p-d13ae084fa384823abb25ce06a1a1af8'
    # }

    pipeline_id_dict = {
        'GN002_Android': 'p-b31b3b4bf3974d9badd88b0ab5b01746',
        'GN002_IOS': 'p-a3c1e6260145444f84a792e6a0edaa74',
        # 'WinClient': 'p-efd73cc2a661486a92d09e66588231ec',
        'GN002_DS': 'p-f21f4aeb2f304096962a1d1b3e7d16be',
        '【GN002_ASAN】IOS': 'p-e7f48e5fe4674c9fb8821042199a5cfc',
        '【GN002_ASAN】Android': 'p-ddcb500f02934ba4b31a92e4eac4f7a1',
        '【GN002_ASAN】DS': 'p-d70fec6f28534112a92a8c35ee777066'
    }



    # need_query_build_time = '04-11 23:04'  # 例子,该值可为空字符串,表示查询最新的构建流水线信息
    need_query_build_time = ''   #例子,该值可为空字符串,表示查询最新的构建流水线信息

    single_pipline_list = get_information(project_id, pipeline_id_dict, need_query_build_time)
    content_all = ''
    for content in single_pipline_list:
        content_all = content_all + str(content)
    # print(content_all)
    # send_request_bot_planning_developping_group_project(content_all)
    # send_request_bot_planning_developping_group_build(content_all)
    # send_request_bot_planning_developping_group_build_problem(content_all)