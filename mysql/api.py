

from mysql import Connect_mysql, db_config


def select_pipeline_by_version(table_name, limit):
    """查询相应版本号对应流水线"""

    # db = Connect_mysql.MySql(db_config.HOST, db_config.USER, db_config.PWD, db_config.version_num_db)
    # 操作表类
    # table = db.usetable(db_config.table_build_version, db_config.version_num_db)
    print(Connect_mysql.Table.select([table_name, limit]))
    # print("111", select_result)
    # db.close()



select_pipeline_by_version(table_name, limit)