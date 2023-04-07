import pymysql


class MySql(object):
    def __init__(self, host, db_user, pwd, db_name):
        self.host = host
        self.db_user = db_user
        self.pwd = pwd
        self.db_name = db_name
        self.db = self._connect_db(self.host, self.db_user, self.pwd, self.db_name)

    def _connect_db(self, host, db_user, pwd, db_name):
        try:
            db = pymysql.connect(host=f"{host}", user=f"{db_user}", password=f"{pwd}", db=f"{db_name}", port=3306, charset='utf8')
        except Exception:
            raise Exception("connect failed。")
        return db

    def usetable(self, table_name, db_name):
        if self.istable(table_name):
            return Table(self.db, table_name, db_name)
        else:
            raise ValueError(f"传入的表:{table_name}不存在")


    def close(self):
        self.db.commit()
        self.db.close()

    def istable(self, table_name):
        cursor = self.db.cursor()
        sql = "show tables;"
        cursor.execute(sql)
        filter_tag = cursor.fetchall()
        tables = []
        for i in filter_tag:
            tables.append(i[0])
        if table_name in tables:
            return True
        else:
            return False

class Table(object):
    def __init__(self, db, table_name, db_name):
        self.db = db
        self.table = table_name
        self.db_name = db_name
        self.filename = self._field(self.db_name, self.table)



    def get_table_list(self, table_name, list_name):
        """
        返回数据库中的某一个表中的所有种类
        :param table_name: 表名
        :param list_name: 列名
        :return:
        """
        sql = f"select {list_name},count(*) from {table_name} group by {list_name} limit 20;"
        print("[SQL-sentence]:", sql)
        cursor = self.db.cursor()
        cursor.execute(sql)
        slet = cursor.fetchall()
        print("11", slet, type(slet))
        # 给数据处理成键值对，然后返回
        # dc = {}
        # for i in slet:
        #     for j in range(len(i)):
        #         dc[fields[j]] = i[j]
        # result = dc
        # return result

    def select(self, arr):
        sql = isql(arr)
        sql = f"select * from {self.table} where {sql};"
        print("[SQL-sentence]:", sql)
        fi = self.filename
        fields = []
        # 得到所有的字段名
        for ih in fi:
            fields.append(ih[1])
        cursor = self.db.cursor()
        cursor.execute(sql)
        slet = cursor.fetchall()
        # 给数据处理成键值对，然后返回
        dc = {}
        for i in slet:
            for j in range(len(i)):
                dc[fields[j]] = i[j]
        result = dc
        return result

    def _field(self, dbname, tablename):
        # 获取表结构
        sql = "select  table_name,column_name,column_comment  from " \
              f"information_schema.columns where table_schema ='{dbname}'  and table_name = '{tablename}';"
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
        except:
            raise ValueError(f"Please confirm {dbname},{tablename} does it exist.")
        key = cursor.fetchall()
        return key


def isql(arr):
    # 处理sql语句，并组装成相应sql执行语句
    sql, op = "", 0
    for ar in arr:
        if type(ar) is str:
            kl = ar
            if op < len(arr)-1:
                sql = sql + f"{kl}" + " and "
            else:
                sql = sql + kl
        else:
            if len(ar) != 2:
                raise ValueError(f"{ar},非法格式")
            try:
                ar["op"]
            except:
                print(f"{ar}, 格式非法，请输入操作符‘op’。")
            kl, k = "", 0
            # 处理字符类型是否加单引号
            for ke in ar.keys():
                if ke != 'op' and type(ar[ke]) is int:
                    kl = f"{ke}{ar['op']}{ar[ke]}"
                elif ke != 'op':
                    kl = f"{ke}{ar['op']}'{ar[ke]}'"
                    print(kl)
                k += 1
            if op < len(arr)-1:
                sql = sql + f"{kl}" + " and "
            else:
                sql = sql + kl
        op += 1
    return sql


