# -*- coding: utf-8 -*-
# 不依赖MySql库的数据库接口
import json
import requests

_default_database   = 'hpjy_cggamestuidio'
_gloabl_typemap     = {}



class MysqlService(object):
    # 数据库接口，持续更新

    _get_url        = "https://9.134.82.73:8443/clientfetchdata"
    _post_url       = "https://9.134.82.73:8443/client_modify_data"
    _get_header     = {
        "Content-Type":     "application/json",
        "X-API-Key":        "AJEAIQdfAAoV8TGv0WAFkARwbdAFw_C2_2f",
    }
    _post_header    = {
        "Content-Type":     "application/json",
        "X-API-Key":        "tfoaRql5UEBVafSM1ivfPLU7GfXKw5ybRlKXgMVY0WY="
    }

    @staticmethod
    def get(sql_string: str):
        '''
        最原生的sql接口，管读操作
        调用示例：
            sql_string = 'SELECT * FROM hpjy_cggamestuidio.demo_table LIMIT 10'
            res = MysqlService.get(sql_string)
            print(res)  # 完整response
            print(res.get('data', [])) # 只关心获取到的数据
            print(res.get('success', False)) # 只关心是否成功
        res结果示例：
            {'data': [{'age': 15, 'birthday': 'Mon, 31 Dec 1990 04:45:50 GMT', 'description': 'a member', 'id': 1, 'name': 'zhangsan', 'weight': 123.4}, ...], 'message': '查询成功', 'row_count': 1, 'success': True}
        '''
        data = {"sql": str(sql_string)}
        response = requests.post(MysqlService._get_url, headers=MysqlService._get_header, data=json.dumps(data), verify=False)
        return json.loads(response.content)

    @staticmethod
    def post(sql_string: str):
        '''
        最原生的sql接口，管写操作
        示例：
            sql_string = 'INSERT INTO hpjy_cggamestuidio.demo_table (name, description, age, weight, birthday) VALUES ("zhangsan", "a member", 15, 123.4, "1990-12-31 04:45:50")'
            sql_string = 'UPDATE hpjy_cggamestuidio.demo_table SET name = "lisi" WHERE name = "zhangsan"'
            res = MysqlService.post(sql_string)
            print(res)  # 完整response
            print(res.get('success', False)) # 只关心是否成功
        res结果示例：
            {'data': {'affected_rows': 1}, 'message': '操作成功', 'row_count': 1, 'success': True}
        '''
        data = {"sql": str(sql_string)}
        response = requests.post(MysqlService._post_url, headers=MysqlService._post_header, data=json.dumps(data), verify=False)
        return json.loads(response.content)
    
    @staticmethod
    def insert(table_name: str, datas: dict, database: str = _default_database):
        '''
        Insert操作封装
        @ 参数 table_name:  需要将数据插入哪张表中
        @ 参数 datas:       需要插入的键值对，不能为空
        @ 参数 database:    数据库名，默认使用_default_database
        使用示例：
            datas = {
                'name':         'caochong',
                'description':  'ertongjie',
                'age':          10,
                'weight':       25,
                'birthday':     '1980-01-01 12:34:56',
            }
            res = MysqlService.insert('demo_table', datas)
        '''
        assert len(datas), 'Empty datas passed to MysqlService.insert !'
        global _gloabl_typemap
        typemap = _gloabl_typemap.get(table_name, {})
        if len(typemap) == 0:
            sample_datas = MysqlService.select(table_name, limit = 1, database=database).get('data', [])
            if len(sample_datas):
                sample_data = sample_datas[0]
                for key, value in sample_data.items():
                    typemap[key] = type(value)
            _gloabl_typemap[table_name] = typemap.copy()
        sql_string = f'INSERT INTO {database}.{table_name} ('
        keys = list(datas.keys())
        sql_string += ', '.join([str(x) for x in keys])
        sql_string += ') VALUES ('
        is_first = True
        for key, value in datas.items():
            if not is_first:
                sql_string += ', '
            valuetype = typemap.get(key, None)
            if valuetype is str:
                sql_string += f'"{value}"'
            else:
                if valuetype:
                    value = valuetype(value)
                sql_string += f'{value}'
            is_first = False
        sql_string += ")"
        return MysqlService.post(sql_string)

    @staticmethod
    def update(table_name: str, datas: dict, options: str = '', database: str=_default_database):
        '''
        Update操作封装
        @ 参数 table_name:  需要更新哪张数据库表
        @ 参数 datas:       需要更新的数据键值对，不能为空
        @ 参数 options:     条件语句，目前需要自己先写一下，比如'name = "zhangsan" OR age = 15'默认是没有条件
        @ 参数 database:    数据库名，默认使用_default_database
        使用示例：
            datas = {
                'age': 11, 
                'weight': 30
            }
            options = 'name = "caochong"'
            res = MysqlService.update('demo_table', datas, options)
        '''
        assert len(datas), 'Empty datas passed to MysqlService.update !'
        global _gloabl_typemap
        typemap = _gloabl_typemap.get(table_name, {})
        if len(typemap) == 0:
            sample_datas = MysqlService.select(table_name, limit = 1, database=database).get('data', [])
            if len(sample_datas):
                sample_data = sample_datas[0]
                for key, value in sample_data.items():
                    typemap[key] = type(value)
            _gloabl_typemap[table_name] = typemap.copy()
        sql_string = f'UPDATE {database}.{table_name} SET '
        is_first = True
        for key, value in datas.items():
            if not is_first:
                sql_string += ', '
            valuetype = typemap.get(key, None)
            if valuetype is str:
                sql_string += f'{key} = "{value}"'
            else:
                if valuetype:
                    value = valuetype(value)
                sql_string += f'{key} = {value}'
            is_first = False
        if len(options) > 0:
            sql_string += f' WHERE {options}'
        return MysqlService.post(sql_string)
    
    @staticmethod
    def select(table_name: str, keys: list = [], options: str = '', limit: int = 10, database: str = _default_database):
        '''
        Select操作封装
        @ 参数 table_name:  需要从哪张表获取数据
        @ 参数 keys:        需要获取哪些列，如果为空，则获取所有列，默认为空
        @ 参数 options:     条件语句，目前需要自己先写一下，比如'name = "zhangsan" OR age = 15'默认是没有条件
        @ 参数 limit:       限制多少条数据，默认为10
        @ 参数 database:    数据库名，默认使用_default_database
        使用示例:
            keys = ['name', 'description', 'age']
            options = 'name = "caochong"'
            limit = 1
            res = MysqlService.select('demo_table', keys, options, limit)
        '''
        sql_string = 'SELECT '
        if len(keys) == 0:
            sql_string += '* '
        else:
            sql_string += ', '.join([str(x) for x in keys]) + ' '
        sql_string += f'FROM {database}.{table_name} '
        if len(options):
            sql_string += f'WHERE {options} '
        if limit >= 1:
            sql_string += f'LIMIT {limit} '
        return MysqlService.get(sql_string)
    
    @staticmethod
    def delete(table_name: str, options: str, database: str = _default_database):
        '''
        Delete操作封装
        @ 参数 table_name:  需要从哪张表删除数据
        @ 参数 options:     条件语句，目前需要自己先写一下，比如'name = "zhangsan" OR age = 15'，不允许为空（否则相当于删除整张表）
        @ 参数 database:    数据库名，默认使用_default_database
        '''
        assert len(options) > 0, f'Not support on deleting table without options, this will lead to fully-deletion of the current table !'
        sql_string = f'DELETE FROM {database}.{table_name} WHERE {options}'
        return MysqlService.post(sql_string)