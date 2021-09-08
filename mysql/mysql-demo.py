import pymysql

#  https://www.py.cn/jishu/jichu/12706.html
# 1. 导入 pymysql 模块
# 2. 打开数据库连接
# 3. 创建游标对象，用于执行脚本
# 4. 使用游标对象执行脚本
# 5. 关闭数据库

if __name__ == '__main__':
    # 打开数据库连接
    # 注意：这里已经假定存在数据库 information_schema，db指定了连接的数据库，当然这个参数也可以没有
    db = pymysql.connect(host='192.168.1.32', port=3306, user='dev', passwd='Cqhz.2020', db='information_schema',
                         charset='utf8')

    # 使用cursor方法创建一个游标
    cursor = db.cursor()

    cursor.execute("select version()")
    data = cursor.fetchone()
    print(" Database Version:%s" % data)

    cursor.execute("""SELECT @serial_num := @serial_num + 1
                        AS '序号',
       upper
           (TABLE_NAME) as '表名称',
       TABLE_COMMENT    as '中文名称',
       ''               as '数据量',
       ''               as '平均日增量',
       ''               as '平均月增量',
       ''               as '平均年增量',
       ''               as '备注'
FROM information_schema.TABLES,
     (SELECT @serial_num := 0) serial_num
WHERE TABLE_SCHEMA = 'highzap_ebs_0715'
  AND TABLE_NAME LIKE 'ebs_%'
order by TABLE_NAME;""")

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    db.close()
