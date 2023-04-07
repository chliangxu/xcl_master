
from mysql import Connect_mysql, db_config


def select_pipeline_by_version(version):
    db = Connect_mysql.MySql(db_config.HOST, db_config.USER, db_config.PWD, db_config.version_num_db)
    table = db.usetable(db_config.table_build_version, db_config.version_num_db)
    table_name = "build_version"
    list_name = "BuildClass"
    # print(table.get_table_list(table_name, list_name))
    select_result = table.select([{"version": version, "op": "="}])
    print("select_result", select_result)
    db.close()


def ko():
    a = select_pipeline_by_version("0.2.625.117")
    print("88888", a)

ko()
