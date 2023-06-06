import os
from threading import Thread


class remote_computer:

    def __init__(self):
        self.user = "administrator"
        self.first_password = "GNGame@202212"
        self.two_password = "APGame@2022"

    def mstsc_link(self, host, user, password):
        os.system(r'cmdkey /generic:termsrv/%s /user:%s /pass:%s' % (host, user, password))
        os.popen(r'mstsc /noConsentPrompt /v:%s /admin /w 2200 /h 1200' % (host))

    def switch_computer(self, index):
        if index == 1:
            self.mstsc_link("9.30.18.100", self.user, self.first_password)

        elif index == 2:
            self.mstsc_link("9.30.17.241", self.user, self.first_password)

        elif index == 3:
            self.mstsc_link("9.30.18.126", self.user, self.first_password)

        elif index == 4:
            self.mstsc_link("9.30.18.101", self.user, self.first_password)

        elif index == 5:
            self.mstsc_link("9.30.4.170", self.user, self.two_password)

        elif index == 6:
            self.mstsc_link("9.30.19.72", self.user, self.first_password)

        elif index == 7:
            self.mstsc_link("9.30.18.26", self.user, self.first_password)

        elif index == 8:
            self.mstsc_link("9.30.19.165", self.user, self.first_password)

        elif index == 9:
            self.mstsc_link("9.30.4.61", self.user, self.two_password)

        elif index == 10:
            self.mstsc_link("9.19.176.248", self.user, self.two_password)

        elif index == 11:
            self.mstsc_link("9.30.19.144", self.user, self.first_password)

        elif index == 12:
            self.mstsc_link("9.30.4.182", self.user, self.two_password)

        elif index == 13:
            self.mstsc_link("9.30.18.80", self.user, self.first_password)

        elif index == 14:
            self.mstsc_link("9.30.17.216", self.user, self.first_password)

        elif index == 15:
            self.mstsc_link("9.30.18.93", self.user, self.first_password)

        elif index == 16:
            self.mstsc_link("9.30.19.140", self.user, self.first_password)

        elif index == 17:
            self.mstsc_link("9.30.7.154", self.user, self.two_password)

        elif index == 18:
            self.mstsc_link("9.30.11.144", self.user, self.two_password)

        elif index == 19:
            self.mstsc_link("9.30.7.183", self.user, self.two_password)

        elif index == 20:
            self.mstsc_link("9.30.8.173", self.user, self.first_password)

        elif index == 21:
            self.mstsc_link("9.19.176.10", self.user, self.first_password)

        elif index == 22:
            self.mstsc_link("9.30.19.21", self.user, self.first_password)

        elif index == 23:
            self.mstsc_link("9.30.10.184", self.user, self.first_password)

        elif index == 24:
            self.mstsc_link("9.19.176.165", self.user, self.two_password)

        elif index == 25:
            self.mstsc_link("9.30.6.236", self.user, self.first_password)

        elif index == 26:
            self.mstsc_link("9.19.177.32", self.user, self.first_password)

        elif index == 27:
            self.mstsc_link("9.30.10.151", self.user, self.first_password)

        elif index == 28:
            self.mstsc_link("9.30.18.37", self.user, self.first_password)

        elif index == 29:
            self.mstsc_link("9.19.177.7", self.user, self.two_password)

        elif index == 30:
            self.mstsc_link("9.30.4.180", self.user, self.two_password)

        elif index == 31:
            self.mstsc_link("9.30.4.153", self.user, self.two_password)

        elif index == 32:
            self.mstsc_link("9.19.177.28", self.user, self.first_password)

        elif index == 33:
            self.mstsc_link("9.19.177.3", self.user, self.first_password)

        elif index == 34:
            self.mstsc_link("9.30.11.166", self.user, self.two_password)

        elif index == 35:
            self.mstsc_link("9.30.17.134", self.user, self.first_password)

        elif index == 36:
            self.mstsc_link("9.30.11.218", self.user, self.first_password)

        elif index == 37:
            self.mstsc_link("9.30.10.225", self.user, self.first_password)

        elif index == 38:
            self.mstsc_link("9.30.11.47", self.user, self.first_password)

        elif index == 39:
            self.mstsc_link("9.30.16.16", self.user, self.first_password)

        elif index == 40:
            self.mstsc_link("9.30.10.75", self.user, self.first_password)

        elif index == 41:
            self.mstsc_link("9.30.8.11", self.user, self.first_password)

        elif index == 42:
            self.mstsc_link("9.30.10.96", self.user, self.first_password)

        elif index == 43:
            self.mstsc_link("9.30.11.31", self.user, self.first_password)

        elif index == 44:
            self.mstsc_link("9.30.9.222", self.user, self.first_password)

        elif index == 45:
            pass

        elif index == 50:
            self.mstsc_link("9.19.176.233", self.user, self.two_password)

    def computer_name(self):
        computer_name_dict = {}
        computer_name_dict["Computer"] = " %s以下都是PC的远程机器%s " % ("~" * 10, "~" * 10) + "\n"
        computer_name_dict["冒烟包机器"] = "{}分支主干{} ".format("-" * 15, "-" * 15)
        computer_name_dict["1"] = "冒烟包Android的机器-9.30.18.100"
        computer_name_dict["2"] = "冒烟包DS的机器-9.30.17.241"
        computer_name_dict["3"] = "冒烟包Editor的机器-9.30.18.126"
        computer_name_dict["4"] = "冒烟包WinClient的机器-9.30.18.101"
        computer_name_dict["5"] = "冒烟包WinClientOB的机器-9.30.4.170"
        computer_name_dict["6"] = "冒烟包WinclientReplay的机器-9.30.19.72" + "\n"
        computer_name_dict["ASAN包机器"] = "{}分支主干{} ".format("-" * 15, "-" * 15)
        computer_name_dict["7"] = "主干ASAN包Android的机器-9.30.18.26"
        computer_name_dict["8"] = "主干ASAN包DS的机器-9.30.19.165" + "\n"
        computer_name_dict["资源剔除机器"] = "{}分支主干{} ".format("-" * 15, "-" * 15)
        computer_name_dict["9"] = "资源剔除的机器-9.30.4.61"
        computer_name_dict["10"] = "资源剔除的机器-9.19.176.248" + "\n"
        computer_name_dict["CE包机器"] = "{}分支主干{} ".format("-" * 15, "-" * 15)
        computer_name_dict["11"] = "CE包Android的机器-9.30.19.144"
        computer_name_dict["12"] = "CE包Android的机器-9.30.4.182"
        computer_name_dict["13"] = "CE包DS的机器-9.30.18.80" + "\n"
        computer_name_dict["自动构建包机器"] = "{}分支主干{} ".format("-" * 15, "-" * 15)
        computer_name_dict["14"] = "自动构建包DS的机器-9.30.17.216"
        computer_name_dict["15"] = "自动构建包Android的机器-9.30.18.93" + "\n"
        computer_name_dict["GNT01机器"] = "{}分支GNT01{} ".format("-" * 15, "-" * 15)
        computer_name_dict["16"] = "冒烟包Android的机器-9.30.19.140"
        computer_name_dict["17"] = "冒烟包DS的机器-9.30.7.154"
        computer_name_dict["18"] = "冒烟包Editor,Winclient的机器-9.30.11.144"
        computer_name_dict["19"] = "ASAN包Android的机器-9.30.7.183"
        computer_name_dict["20"] = "ASAN包DS的机器-9.30.8.173"
        computer_name_dict["21"] = "Release包DS的机器-9.19.176.101"
        computer_name_dict["22"] = "Release包Android的机器-9.30.19.21"
        computer_name_dict["23"] = "9.30.10.184"
        computer_name_dict["24"] = "9.19.176.165" + "\n"
        computer_name_dict["IGN"] = "{}分支主干{}".format("-" * 15, "-" * 15)
        computer_name_dict["25"] = "IGN本地化机器-9.30.6.236" + "\n"
        computer_name_dict["其余机器"] = "{}分支主干{}".format("-" * 15, "-" * 15)
        computer_name_dict["26"] = "单点机器-9.19.177.32"
        computer_name_dict["27"] = "热更机器-9.30.10.151"
        computer_name_dict["28"] = "diff以及资源扫描-9.30.18.37"
        computer_name_dict["29"] = "9.19.177.7"
        computer_name_dict["30"] = "9.30.4.180"
        computer_name_dict["31"] = "9.30.4.153"
        computer_name_dict["32"] = "9.19.177.28"
        computer_name_dict["33"] = "9.19.177.35"
        computer_name_dict["34"] = "9.30.11.166" + "\n"
        computer_name_dict["部署中"] = "{}".format("=" * 30)
        computer_name_dict["35"] = "9.30.17.134"
        computer_name_dict["36"] = "9.30.11.218"
        computer_name_dict["37"] = "9.30.10.225"
        computer_name_dict["38"] = "9.30.11.47"
        computer_name_dict["39"] = "9.30.16.16"
        computer_name_dict["40"] = "9.30.10.75"
        computer_name_dict["41"] = "9.30.8.11"
        computer_name_dict["42"] = "9.30.10.96"
        computer_name_dict["43"] = "9.30.11.31"
        computer_name_dict["44"] = "9.30.9.222"
        computer_name_dict["45"] = ""
        computer_name_dict["46"] = ""
        computer_name_dict["APGame"] = "{}APGame预留机器{}".format("-" * 15, "-" * 15)
        computer_name_dict["50"] = "9.19.176.233"
        for k, v in computer_name_dict.items():
            print(k, v)

        return computer_name_dict

if __name__ == '__main__':
    RemoteDesk = remote_computer()
    remote_computer().computer_name()
    input_index = int(input('输入对应远程构建机序号: '))
    remote_computer().switch_computer(input_index)

