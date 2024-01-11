
import requests

import os
import xlwt

def out(bugstorylist):
    ws = xlwt.Workbook(encoding='UTF-8')
    if bugstorylist[0]['url'][-3:] =='bug':
        w = ws.add_sheet(u'bug单查询')
        filename = 'bugfile.xls'
    else:
        w = ws.add_sheet(u'story单查询')
        filename = 'storyfile.xls'
    pwd = os.getcwd()

    style = xlwt.XFStyle()
    sty = xlwt.Alignment()
    sty.horz = 0x02
    sty.vert = 0x01
    style.alignment=sty

    #设置标题列底色
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 5
    style.pattern = pattern
    #status状态;reporter创建人;created创建时间;priority优先级
    title_lis = ['P4','SVN','Git','id','title','状态','创建时间','创建人','优先级','url']
    for i in range(len(title_lis)):
        w.write(0,i,title_lis[i],style)
    w.col(0).width = 20 * 256
    w.col(1).width = 20 * 256
    w.col(2).width = 40 * 256
    w.col(3).width = 20 * 256
    w.col(4).width = 90 * 256
    w.col(5).width = 30 * 256
    w.col(6).width = 20 * 256
    w.col(7).width = 20 * 256
    w.col(8).width = 30 * 256
    w.col(9).width = 50 * 256

    excel_row = 1
    for iwrite in bugstorylist:
        w.write(excel_row , 0, iwrite['p4'])
        w.write(excel_row, 1, iwrite['svn'])
        w.write(excel_row, 2, iwrite['git'])
        w.write(excel_row, 3, iwrite['id'])
        w.write(excel_row, 4, iwrite['title'])
        w.write(excel_row, 5, iwrite['status'])
        w.write(excel_row, 6, iwrite['created'])
        w.write(excel_row, 7, iwrite['reporter'])
        w.write(excel_row, 8, iwrite['priority'])
        w.write(excel_row, 9, iwrite['url'])
        excel_row += 1

    for iheight in range(excel_row):
        w.row(iheight).height = True
        w.row(iheight).height_mismatch = True
        w.row(iheight).height = 400

    try:
        exist_file = open(pwd + '\\' + filename, 'wb')
        ws.save(exist_file)
        exist_file.close()
        print(filename,'文件已生成')
    except Exception as e:
        print(e)
        print('----文件已打开，请先另存后关闭----')

def GetBugStory(type,limit,page):
    son_url = 'https://tapd.woa.com/r/t?id=%s&type=%s'
    bugstory_lis = []
    auth = ('UGC_Request_2022', '4772919B-0455-88FB-821D-95047A741BEF')
    if type =='bugs':
        getkey = 'Bug'
        titlename = 'title'
        reporter = 'reporter'   #创建人
    elif type == 'stories':
        getkey = 'Story'
        titlename = 'name'
        reporter = 'creator' #创建人
    else:
        print('-----请传入type=bugs或stories-----')
        return ''
    #获取需求单/Bug单
    url = 'http://apiv2.tapd.woa.com/%s'%type+'?workspace_id=69990352&order=created%20desc'+'&limit=%s&page=%s'%(limit,page)
    try :res = requests.get(url=url,auth=auth)
    except Exception as e:
        print(e)
    res.encoding = 'utf-8'
    print('加载中......')
    for i in res.json()['data']:
        BugStory = {}
        BugStory['id'] = (i[getkey]['id'][10:])
        BugStory['title'] = (i[getkey][titlename])
        BugStory['status'] = (i[getkey]['status'])
        BugStory['created'] = (i[getkey]['created'])   #创建时间
        BugStory['reporter'] = (i[getkey][reporter])   #创建人
        BugStory['priority'] = (i[getkey]['priority']) #优先级
        BugStory['url'] = son_url%(i[getkey]['id'][10:],getkey.lower())
        com_p4 = []
        com_git = []
        com_svn = []
        commit_url = 'http://apiv2.tapd.woa.com/code_commit_infos?workspace_id=69990352&type=%s&object_id=%s'%(getkey,i[getkey]['id'])
        try: commit_res = requests.get(url=commit_url,auth=auth)
        except Exception as ex:
            print(ex)
        #P4 Git提交记录
        if len(commit_res.json()['data']) != 0 :  #提交次数不为0
            for icount in commit_res.json()['data']:
                if icount['git_env'] =='P4':
                    com_p4.append(icount['commit_id']+'、')  #p4提交号

                elif icount['git_env'] == 'CodeGit':
                    com_git.append(icount['commit_id']+'、')  #git提交号
        # elif len(commit_res.json()['data']) ==0:  #提交次数为0

        BugStory['p4'] = com_p4
        BugStory['git'] = com_git

        #SVN提交记录
        svn_url = 'http://apiv2.tapd.woa.com/svn_commits?workspace_id=69990352&type=%s&object_id=%s'%(getkey,i[getkey]['id'])
        res_svn = requests.get(url=svn_url,auth=auth)

        if len(res_svn.json()['data']) != 0: #svn提交次数不为0
            for isvn in res_svn.json()['data']:
                com_svn.append(isvn['revision']+'、')
        # elif len(res_svn.json()['data']) ==0:  #提交次数为0
        BugStory['svn'] = com_svn
        bugstory_lis.append(BugStory)
    sorted_list = sorted(bugstory_lis,key=lambda  x: (x['p4'],x['svn'],x['git']),reverse=True)
    out(sorted_list)

if __name__ == '__main__':

    limit = '100'  #查询条数  (每页最大返回200)
    page = '2'   #页数
    type= 'stories' #选填 bugs / stories

    GetBugStory(type=type,limit=limit,page=page)































