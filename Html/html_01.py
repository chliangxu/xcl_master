def bugHtml(jsonList,localFile):
    '''
    color设置黑色字体，width比例100%自适应页面，border-collapse表格边框线合并，text-align表格内容显示居中
    background-color蓝色背景，padding内边距，border-color蓝色边框；
    '''
    #<style>定义table全局格式
    table_head="<!DOCTYPE html>\n" \
               "<html>\n" \
               "<head>\n" \
               "<meta charset='UTF-8'>\n" \
               "<title>2023年测试组</title>\n" \
               "<style type='text/css'>\n" \
               "table {color:#333333; width:100%; border-collapse:collapse; text-align:center;}\n" \
               "table th {background-color:#97CEFA; padding:8px; border-color:#97CEFA;}\n" \
               "table td {padding:8px; border-color:#97CEFA;}\n" \
               "</style>\n" \
               "</head>\n"

    #处理表头格式
    table_th=''
    for title in jsonList[0]:
        table_th = table_th + '<th>'+ str(title) + '</th>'
    table_th='<tr>' + table_th + '</tr>\n'

    #处理行格式
    table_tr = ''
    for i in range(0, len(jsonList)):
        for n,m in enumerate(jsonList[i]):
            if n == 0:
                #行首单独处理<tr>
                jsonList[i][m] = '<tr><td>' + str(jsonList[i][m])
            table_tr = table_tr + str(jsonList[i][m]) + '</td><td>'
        #行尾单独处理</tr>
        table_tr = table_tr[0:-3] + '/tr>\n'
    table_body = "<body>\n" \
                 "<table border='1'>\n" \
                 "<caption>测试组本周未解决Bug</caption>\n"
    table_body=table_body+table_th+table_tr+'</table>\n</body>\n'
    #将整个html代码组合起来
    tableCode = table_head + table_body + '</html>'

    #将html代码写入文件
    html_write=open(localFile,"w",encoding="utf-8")
    html_write.write(tableCode)

if __name__=="__main__":
    #jsonList是json数组
    jsonList=[{'BugID': 21457,'Bug标题': '新增报错','创建人': '小A'},
              {'BugID': 21484,'Bug标题': '删除报错', '创建人': '小B',},
              {'BugID': 21607,'Bug标题': '修改报错', '创建人': '小C'},
              {'BugID': 21626,'Bug标题': '查询报错', '创建人': '小D'}]
    # localFile=r'E:\Double\test.html'
    open("./test.html", "w").close()
    localFile = r"E:\xcl\xcl_master\Html\test.html"
    # print(localFile)
    bugHtml(jsonList, localFile)