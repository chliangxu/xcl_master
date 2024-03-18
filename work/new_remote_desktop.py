
import os

first_password_computer_pool = [
    "9.30.18.100", "9.30.17.241", "9.30.18.126", "9.30.18.101", "9.30.19.72",
    "9.30.18.26", "9.30.19.165", "9.30.19.144", "9.30.18.80", "9.30.17.216", "9.30.18.93", "9.30.19.140", "9.30.8.173",
    "9.19.176.101", "9.30.19.21", "9.30.10.184", "9.30.6.236", "9.19.177.32", "9.30.10.151", "9.30.18.37", "9.19.177.28",
    "9.19.177.3", "9.30.17.134", "9.30.11.218", "9.30.10.225", "9.30.11.47", "9.30.16.16", "9.30.10.75", "9.30.8.11",
    "9.30.10.96", "9.30.11.31", "9.30.9.222", "9.30.1.242", "9.30.6.160", "9.30.15.217", "9.30.16.146", "9.19.177.35",
]
two_password_computer_pool = [
    "9.30.4.170", "9.30.4.61", "9.19.176.248", "9.30.4.182", "9.30.7.154",
    "9.30.11.144", "9.30.7.183", "9.19.176.165", "9.19.177.7", "9.30.4.180",
    "9.30.4.153", "9.30.11.166", "9.19.176.233",
]

three_password_computer_pool = [
    "9.30.15.235", "9.30.15.202", "9.30.10.175", "9.30.10.190", "9.19.176.121",
    "9.19.176.85", "9.19.176.119", "9.19.176.236", "9.30.9.246", "9.30.9.220",
    "9.19.176.74", "9.19.176.107", "9.30.15.213", "9.30.16.133", "9.30.15.196",
    "9.30.16.141",  "9.30.16.166",
]

class remote_computer:

    def __init__(self):
        self.user = "administrator"
        self.first_password = "GNGame@202212"
        self.two_password = "APGame@2022"
        self.three_password = "ProjectP-2024#"

    def mstsc_link(self, host, user, password):
        os.system(r'cmdkey /generic:termsrv/%s /user:%s /pass:%s' % (host, user, password))
        os.popen(r'mstsc /noConsentPrompt /v:%s /admin /w 2200 /h 1200' % (host))


    def switch_computer(self, input_ip):
        if input_ip is not None:
            input_ip = str(input_ip)
            self.mstsc_link(input_ip, self.user, self.output_password(input_ip))

    def output_password(self, ip):
        if ip:
            for first_finally_ip in first_password_computer_pool:
                if ip == first_finally_ip:
                    return self.first_password

            for two_finally_ip in two_password_computer_pool:
                if ip == two_finally_ip:
                    return self.two_password

            for three_finally_ip in three_password_computer_pool:
                if ip == three_finally_ip:
                    return self.three_password

            print("输入ip不正确， 请重新输入")


if __name__ == '__main__':
    RemoteDesk = remote_computer()
    input_ip = (input('输入对应远程构建机序ip: '))
    remote_computer().switch_computer(input_ip)