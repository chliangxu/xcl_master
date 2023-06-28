# -*- coding: utf-8 -*-

import platform
import os
import sys
import hashlib
import subprocess
import shutil
import re
# import requests
# import json

if platform.system().lower() == 'windows':
    if platform.python_version().split('.')[0] != '3':
        import _winreg as winreg
    else:
        import winreg


def ExecutCommand(command, exit_when_failed=True):
    # command = command + " 2>&1"
    print('Execute command: {0}'.format(command))

    sys.stdout.flush()
    rst = os.system(command)
    sys.stdout.flush()

    if exit_when_failed and rst != 0:
        print('Execute command failed with result: {0}'.format(rst))
        sys.exit(1)


def ExecuteCommandEx(command, exit_when_failed=True):
    try:
        print('Execute command: {0}'.format(command))

        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as error:
        print('Execute command failed with result: {0}'.format(error.returncode))
        if exit_when_failed:
            sys.exit(1)


def IsWidnows():
    return (platform.system().lower() == 'windows')


def OutputStepInfo(message):
    if not hasattr(OutputStepInfo, "counter"):
        OutputStepInfo.counter = 0

    OutputStepInfo.counter += 1

    print('\n-------------------------------------------------------------------------------------------------------')
    print('Step {0}: {1}'.format(OutputStepInfo.counter, message))
    print('-------------------------------------------------------------------------------------------------------\n')


def CreatePerforceWorkspace(workspace_name, workspace_path, branch_path, owner, host):
    OutputStepInfo('Create Perforce Workspace')

    f = open('WorkspaceDesc.txt', 'w')
    f.write('Client: {0}\n'.format(workspace_name))
    f.write('Owner: {0}\n'.format(owner))
    f.write('Host: {0}\n'.format(host))
    f.write('Options: allwrite clobber nocompress unlocked nomodtime normdir\n')
    f.write('Description: Auto created by {0}.\n'.format(owner))
    f.write('Root: {0}\n'.format(workspace_path))
    f.write('View:\n')
    f.write('\t{0}/... //{1}/...\n'.format(branch_path, workspace_name))

    if os.environ.get('TargetPlat', 'Android') == 'Android' or os.environ.get('TargetPlat', 'Android') == 'IOS':
        f.write('\t{0}/AClient_Pak/... //{1}/AClient_Pak/...\n'.format(branch_path, workspace_name))
        f.write('\t{0}/AClient_Pak/WindowsNoEditor/... //{1}/AClient_Pak/WindowsNoEditor/...\n'
                .format(branch_path, workspace_name))
    else:
        f.write('\t{0}/AClient_Pak/WindowsNoEditor/... //{1}/AClient_Pak/WindowsNoEditor/...\n'
                .format(branch_path, workspace_name))

    if os.environ.get('TargetPlat', 'Android') == 'DS':
        f.write('\t{0}/AClient_Pak/tgz/... //{1}/AClient_Pak/tgz/...\n'.format(branch_path, workspace_name))
        f.write('\t{0}/AClient_Pak/tgz/DSDevelopment/... //{1}/AClient_Pak/tgz/DSDevelopment/...\n'
                .format(branch_path, workspace_name))
        f.write('\t{0}/AClient_Pak/tgz/DSDevelopment_ASAN/... //{1}/AClient_Pak/tgz/DSDevelopment_ASAN/...\n'
                .format(branch_path, workspace_name))
        f.write(
            '\t{0}/AClient_Pak/tgz/DSDevelopment_CE/... //{1}/AClient_Pak/tgz/DSDevelopment_CE/...\n'
                .format(branch_path, workspace_name))
        f.write('\t{0}/AClient_Pak/tgz/DSDevelopment_ES/... //{1}/AClient_Pak/tgz/DSDevelopment_ES/...\n'
                .format(branch_path, workspace_name))

    f.close()

    ExecutCommand('{0} WorkspaceDesc.txt'.format('type' if IsWidnows() else 'cat'))
    ExecuteCommandEx('{0} WorkspaceDesc.txt | p4 client -i'.format('type' if IsWidnows() else 'cat'))


def UpdatePerforceWorkspace(is_remove_workspace, workspace_path, branch_path):
    if is_remove_workspace and os.path.exists(workspace_path):
        OutputStepInfo('Remove workspace folder: {0}'.format(workspace_path))
        # shutil.rmtree(workspace_path)
        if os.path.exists(workspace_path):
            shutil.rmtree(workspace_path)

    OutputStepInfo('Update Perforce Workspace, branch_path: {0}'.format(branch_path))

    ExecutCommand('p4 -C utf8 revert -a -c default')
    ExecutCommand('p4 -C utf8 sync {0} {1}/...#head'.format('-f' if is_remove_workspace else '', branch_path))


def CheckoutSVN(branch_path, user, passwd, workspace_path):
    OutputStepInfo('Checkout SVN, branch_path: {0}'.format(branch_path))

    survive_path = os.path.join(workspace_path, 'AClient')

    BranchName = os.getenv("BranchName", "trunk")

    if BranchName != "trunk":
        BranchName = "/branches/%s" % (BranchName)
        print("不是trunk的分支", BranchName)

    ExecutCommand('svn cleanup {0}'.format(survive_path), False)
    ExecutCommand(
        'svn checkout --force https://svn.woa.com/GNGame/GNClient/{0}/AClient {1} --username {2} --password {3}'.format(
            BranchName, survive_path, user, passwd,
        ))
    ExecutCommand('svn revert --depth=infinity {0}'.format(survive_path))

    engine_path = os.path.join(workspace_path, "AEngine")
    source_svn_path = os.path.join(workspace_path, "AEngine", "Engine", "Source")
    ExecutCommand('svn cleanup {0}'.format(source_svn_path), False)
    ExecutCommand(
        'svn checkout --force https://svn.woa.com/GNGame/GNClient/{0}/AEngine/Source {1} --username {2} --password {3}'.format(
            BranchName, source_svn_path, user, passwd,
        ))
    ExecutCommand('svn revert --depth=infinity {0}'.format(source_svn_path))


def send_message_to_wx_robot_report(message_str, robot_key, user_list):
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

def send_file_with_user():
    user = os.getenv("SendUser", "v_chliangxu")
    robot_key = "41757ab9-1285-419d-9386-08372b258a85"
    msg = "流水线{}".format("https://devops.woa.com/console/pipeline/gngame/p-5b9a4f5e31024ceda8ab1ff514e85dfc/history")
    msg += "机器{}，WorkspacePath{}， WorkspaceName{}".format(os.getenv('PC'), os.getenv('WorkspacePath'), os.getenv('WorkspaceName'))
    send_message_to_wx_robot_report(msg, robot_key, user)




def Run():
    p4ticket = os.getenv('P4Ticket', '')
    ExecutCommand('p4 set P4TICKETS={0}'.format(p4ticket))
    print('System info:', platform.uname())
    print('Python version:', platform.python_version())

    p4_user = os.getenv('SODA_P4USER')
    p4_passwd = os.getenv('SODA_P4PASSWD')
    svn_user = os.getenv('SODA_SVNUSER')
    svn_passwd = os.getenv('SODA_SVNPASSWD')
    workspace_name = os.getenv('WorkspaceName')
    workspace_path = os.getenv('WorkspacePath')
    main_branch_name = os.getenv('MainBranchName')
    branch_name = os.getenv('BranchName') if os.getenv('BranchName') else "trunk"
    is_remove_workspace = (os.getenv('IsRemoveWorkspace').lower() == 'true')

    print(
        'p4_user: {0}\np4_passwd: {1}\nsvn_user: {2}\nsvn_passwd: {3}\nworkspace_name: {4}\nworkspace_path: {5}\nmain_branch_name: {6}\nbranch_name: {7}\n'.format(
            p4_user, p4_passwd, svn_user, svn_passwd, workspace_name, workspace_path, main_branch_name, branch_name))

    # Step 1: Setup Perforce Environment
    OutputStepInfo('Setup Perforce Environment')

    os.environ['P4CHARSET'] = 'utf8'
    os.environ['P4USER'] = p4_user
    os.environ['P4CLIENT'] = workspace_name
    if p4_passwd:
        os.environ['P4PASSWD'] = hashlib.md5(p4_passwd.encode()).hexdigest().upper()

    print('P4CHARSET: {0}\nP4PORT: {1}\nP4USER: {2}\nP4PASSWD: {3}\nP4CLIENT: {4}\n'.format(os.getenv('P4CHARSET'),
                                                                                            os.getenv('P4PORT'),
                                                                                            os.getenv('P4USER'),
                                                                                            os.getenv('P4PASSWD'),
                                                                                            os.getenv('P4CLIENT')))

    if p4_passwd and not IsWidnows():
        ExecuteCommandEx('echo {0} | p4 login'.format(p4_passwd))

    if branch_name != "trunk":
        branch_name = "branches/%s" % (branch_name)
        print("不是trunk的分支", branch_name)

    p4_branch_path = '//GNGame_depot/{0}/{1}'.format(main_branch_name, branch_name)
    svn_branch_path = 'https://svn.woa.com/GNGame/GNClient/{0}/AClient'.format(
        branch_name)

    # Step 2: Create Perforce Workspace
    CreatePerforceWorkspace(workspace_name, workspace_path, p4_branch_path, p4_user, platform.node())

    # Step 3: Update Perforce Workspace And Remove Worksapce Folder If Necessary
    UpdatePerforceWorkspace(is_remove_workspace, workspace_path, p4_branch_path)

    # Step 4: Checkout SVN
    CheckoutSVN(svn_branch_path, svn_user, svn_passwd, workspace_path)

    # Step 5：

    # Step 6: 发送消息到企业微信群@对应的人
    # send_file_with_user()




if __name__ == '__main__':
    Run()
