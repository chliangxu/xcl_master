# p4 revert -C gnbuild_v_yangyyca-PC0_727 //...
#     cmd = 'p4 revert -C gnbuild_v_xinnwan-PC90 //...'
import subprocess
import os

def call_cmd(cmd_str):
    p = subprocess.Popen(args=cmd_str, shell=True, stdout=subprocess.PIPE)
    read = str(p.stdout.read().decode('gb2312', 'ignore'))
    # print(type(read))
    print(read)

def revert_perforce():
    # cmd = 'p4 revert -C gnbuild_v_xinnwan-PC90 //...'  v_linjjyang_v_linjjyan-67001
    cmd = 'p4 revert -C witcherwang_WH //...'


    call_cmd(cmd)



if __name__ == '__main__':
    # updataLocalProject()
    project_path = r"C:\GN\GNYXGame\trunk\AClient"
    engine_path = r"C:\GN\GNYXGame\trunk\AEngine\Engine\Source"
    os.environ['P4CLIENT'] = 'v_xinnwan-PC91'
    os.environ['P4USER'] = 'devindzhang'
    os.environ['P4PORT'] = 'apgamep4.woa.com:8667'
    os.environ['P4CHARSET'] = 'utf8'
    os.environ['P4COMMANDCHARSET'] = 'utf8'
    spec_path = [r'//GNGame_depot/GNYXGame/trunk/AClient',
                 r'//GNGame_depot/GNYXGame/trunk/AEngine']
    revert_perforce()