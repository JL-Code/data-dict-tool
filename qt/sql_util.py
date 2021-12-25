import pymysql


# 创建数据库连接
def create_db_conn(host, port, user, password, db, charset):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    cursor = conn.cursor()
    return conn, cursor


# 获取表列名
def get_index_dict(cursor):
    index_dict = dict()
    index = 0
    for desc in cursor.description:
        index_dict[desc[0]] = index
        index = index + 1
    return index_dict


# 获取 dict 格式的数据行集合
# 运行sql语句，获取结果，并根据表中字段名，转化成dict格式（默认是tuple格式）
def get_dataset(cursor, sql):
    cursor.execute(sql)
    data = cursor.fetchall()
    index_dict = get_index_dict(cursor)
    res = []
    for item in data:
        row = dict()
        for index in index_dict:
            row[index] = item[index_dict[index]]
        res.append(row)

    return res
