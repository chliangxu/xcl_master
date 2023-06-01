import os
from threading import Thread


def mstsc_link(host, user, password):
    os.system(r'cmdkey /generic:termsrv/%s /user:%s /pass:%s' % (host, user, password))
    os.popen(r'mstsc /noConsentPrompt /v:%s /admin /w 2200 /h 1200' % (host))


def switch_computer(index):

    if index == 31:
        print('host_gn_ds')
        mstsc_link("9.30.17.241", "administrator", "GNGame@202212")
    elif index == 32:
        print('host_gn_android')
        mstsc_link("9.30.18.100", "administrator", "GNGame@202212")
    elif index == 33:
        print('host_gn_editor')
        mstsc_link("9.30.18.126", "administrator", "GNGame@202212")
    elif index == 34:
        print('host_gn_win')
        mstsc_link("9.30.18.101", "administrator", "GNGame@202212")
    elif index == 35:
        print('host_gn_win')
        mstsc_link("9.19.177.28", "administrator", "GNGame@202212")

    elif index == 36:
        print('host_gn_ce_android')
        mstsc_link("9.30.19.144", "administrator", "GNGame@202212")
    elif index == 37:
        # print('host_gn_ce_android')
        mstsc_link("9.19.177.35", "administrator", "GNGame@202212")
    elif index == 38:
        print('host_gn_ce_ds')
        mstsc_link("9.30.18.80", "administrator", "GNGame@202212")
    elif index == 39:
        print('host_gn_ce_editor')
        mstsc_link("9.30.18.126", "administrator", "GNGame@202212")
    elif index == 40:
        # print('host_gn_ce_editor')
        mstsc_link("9.30.18.93", "administrator", "GNGame@202212")
    elif index == 41:
        mstsc_link("9.30.4.182", "administrator", "APGame@2022")    #PC104
    elif index == 42:
        mstsc_link("9.30.8.173", "administrator", "GNGame@202212")
    elif index == 43:
        mstsc_link("9.30.19.76", "administrator", "HPGame_2022")
    elif index == 44:
        mstsc_link("9.30.10.151", "administrator", "GNGame@202212")
    elif index == 45:
        mstsc_link("9.19.177.32", "administrator", "GNGame@202212")
    elif index == 46:
        mstsc_link("9.19.177.32", "administrator", "GNGame@202212")
    elif index == 47:
        mstsc_link("9.30.17.241", "administrator", "GNGame@202212")
    elif index == 48:
        mstsc_link("9.30.17.216", "administrator", "GNGame@202212")
    elif index == 49:
        mstsc_link("9.30.19.165", "administrator", "GNGame@202212")
    elif index == 50:
        mstsc_link("9.30.18.26", "administrator", "GNGame@202212")
    elif index == 51:
        mstsc_link("9.19.177.28", "administrator", "GNGame@202212")
    elif index == 52:
        mstsc_link("9.30.4.153", "administrator", "APGame@2022")
    elif index == 53:
        mstsc_link("9.30.4.61", "administrator", "APGame@2022")
    elif index == 54:
        mstsc_link("9.19.176.248", "administrator", "APGame@2022")

# 9.30.18.100
    elif index == 100:
        print('trunk_ugc_all')
        t = Thread(target=mstsc_link, args=(host_trunk_ugc_cook, user_computer, password_computer))
        t1 = Thread(target=mstsc_link, args=(host_trunk_ugc_editor, user_computer, password_computer))
        t2 = Thread(target=mstsc_link, args=(host_trunk_ugc_ds_dev, user_computer, password_computer))
        t3 = Thread(target=mstsc_link, args=(host_trunk_ugc_win, user_computer, password_computer))
        t.start()
        t1.start()
        t2.start()
        t3.start()
    elif index == 101:
        print('cg16_ugc_all')
        t = Thread(target=mstsc_link, args=(host_cg16_ugc_cook, user_computer, password_computer))
        t1 = Thread(target=mstsc_link, args=(host_cg16_ugc_editor, user_computer, password_branch_computer))
        t2 = Thread(target=mstsc_link, args=(host_cg16_ugc_new_pie_ds, user_computer, password_computer))
        t3 = Thread(target=mstsc_link, args=(host_cg16_ugc_win, user_computer, password_branch_computer))
        t4 = Thread(target=mstsc_link, args=(host_cg16_ugc_android, user_computer, password_branch_computer))
        t5 = Thread(target=mstsc_link, args=(host_cg16_ds_dev, user_computer, password_computer))
        t.start()
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()


if __name__ == '__main__':
    s = ""
    input_index = int(input('输入对应远程构建机序号: '))
    switch_computer(input_index)

'''
host_trunk_ugc_cook = '9.30.16.90'  # index == 1
host_trunk_ugc_editor = '9.30.16.69'  # index == 2
host_trunk_ugc_ds_dev = '9.30.0.58'  # index == 3
host_trunk_ugc_win = '9.30.0.44'  # index == 4

host_cg16_ugc_cook = '9.30.0.15'  # index == 5
host_cg16_ugc_editor = '9.30.1.149'  # index == 6
host_cg16_ugc_new_pie_ds = '9.30.0.151'  # index == 7
host_cg16_ugc_win = '9.30.1.182'  # index == 8
host_cg16_ugc_android = '9.30.1.244'  # index == 9
host_cg16_ds_dev = '9.30.11.221'  # index == 10

host_cg16_ugc_cook = '9.30.2.216'  # index == 11
host_cg16_ugc_editor = '9.30.1.185'  # index == 12
host_cg16_ugc_new_pie_ds = '9.30.0.151'  # index == 13
host_cg16_ugc_win = '9.30.1.182'  # index == 14
host_cg16_ugc_android = '9.30.0.185'  # index == 15
host_cg16_ds_dev = '9.30.11.221'  # index == 10

host_cg17_ugc_cook = '9.30.2.216'   # index == 11
host_cg17_ugc_editor = '9.30.1.185'     # index == 12
host_cg17_ugc_new_pie_ds = '9.30.0.151'  # index == 13
host_cg17_ugc_win = '9.30.1.169'  # index == 14
host_cg17_ugc_android = '9.30.0.185'    # index == 15
host_cg17_ds_dev = '9.30.2.217'  # index == 16

trunk_ugc_all index == 100
cg16_ugc_all index == 101

'''

"""
    def mstsc_link(self, host, user, password):
        os.system(r'cmdkey /generic:termsrv/%s /user:%s /pass:%s' % (host, user, password))
        os.popen(r'mstsc /noConsentPrompt /v:%s /admin /w 2200 /h 1200' % (host))

    def switch_computer(self, index):

        if index == 31:
            print('host_gn_ds')
            self.mstsc_link("9.30.17.241", "administrator", "GNGame@202212")
        elif index == 32:
            print('host_gn_android')
            self.mstsc_link("9.30.18.100", "administrator", "GNGame@202212")
        elif index == 33:
            print('host_gn_editor')
            self.mstsc_link("9.30.18.126", "administrator", "GNGame@202212")
        elif index == 34:
            print('host_gn_win')
            self.mstsc_link("9.30.18.101", "administrator", "GNGame@202212")
        elif index == 35:
            print('host_gn_win')
            self.mstsc_link("9.19.177.28", "administrator", "GNGame@202212")

        elif index == 36:
            print('host_gn_ce_android')
            self.mstsc_link("9.30.19.144", "administrator", "GNGame@202212")
        elif index == 37:
            # print('host_gn_ce_android')
            self.mstsc_link("9.19.177.35", "administrator", "GNGame@202212")
        elif index == 38:
            print('host_gn_ce_ds')
            self.mstsc_link("9.30.18.80", "administrator", "GNGame@202212")
        elif index == 39:
            print('host_gn_ce_editor')
            self.mstsc_link("9.30.18.126", "administrator", "GNGame@202212")
        elif index == 40:
            # print('host_gn_ce_editor')
            self.mstsc_link("9.30.18.93", "administrator", "GNGame@202212")
        elif index == 41:
            self.mstsc_link("9.30.4.182", "administrator", "APGame@2022")  # PC104
        elif index == 42:
            self.mstsc_link("9.30.8.173", "administrator", "GNGame@202212")
        elif index == 43:
            self.mstsc_link("9.30.19.76", "administrator", "HPGame_2022")
        elif index == 44:
            self.mstsc_link("9.30.10.151", "administrator", "GNGame@202212")
        elif index == 45:
            self.mstsc_link("9.19.177.32", "administrator", "GNGame@202212")
        elif index == 46:
            self.mstsc_link("9.19.177.32", "administrator", "GNGame@202212")
        elif index == 47:
            self.mstsc_link("9.30.17.241", "administrator", "GNGame@202212")
        elif index == 48:
            self.mstsc_link("9.30.17.216", "administrator", "GNGame@202212")
        elif index == 49:
            self.mstsc_link("9.30.19.165", "administrator", "GNGame@202212")
        elif index == 50:
            self.mstsc_link("9.30.18.26", "administrator", "GNGame@202212")
        elif index == 51:
            self.mstsc_link("9.19.177.28", "administrator", "GNGame@202212")
        elif index == 52:
            self.mstsc_link("9.30.4.153", "administrator", "APGame@2022")
        elif index == 53:
            self.mstsc_link("9.30.4.61", "administrator", "APGame@2022")
        elif index == 54:
            self.mstsc_link("9.19.176.248", "administrator", "APGame@2022")

"""