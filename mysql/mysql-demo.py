import functools

import pymysql


#  https://www.py.cn/jishu/jichu/12706.html
# 1. 导入 pymysql 模块
# 2. 打开数据库连接
# 3. 创建游标对象，用于执行脚本
# 4. 使用游标对象执行脚本
# 5. 关闭数据库

def test():
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

    cursor.execute("""SELECT c.ORDINAL_POSITION         AS '序号',
           c.TABLE_NAME                   AS '数据表',
           t.TABLE_COMMENT                AS '数据表中文名',
           upper
    (c.COLUMN_NAME)           AS '字段名称',
           c.COLUMN_COMMENT               AS '中文名称',
           upper
    (c.COLUMN_TYPE)           AS '字段类型',
           c.CHARACTER_MAXIMUM_LENGTH     AS '长度（字符）',
           c.NUMERIC_PRECISION            AS '长度（数值）',
           c.NUMERIC_SCALE                AS '精度（数值）',
           CASE

               WHEN c.COLUMN_KEY = 'PRI' THEN
                   '是'
               ELSE '否'
    END                        AS '是否主键',
           CASE

               WHEN c.IS_NULLABLE = 'NO' THEN
                   '是'
               ELSE '否'
    END                        AS '是否必须',
           c.column_comment               AS '备注'
    FROM information_schema.COLUMNS c
           left join information_schema.TABLES t on c.TABLE_NAME = t.TABLE_NAME and c.TABLE_SCHEMA=t.TABLE_SCHEMA
    WHERE c.TABLE_SCHEMA =
    (SELECT SCHEMA_NAME
           FROM information_schema.SCHEMATA
           WHERE SCHEMA_NAME = 'highzap_ebs_0715')
           and c.TABLE_NAME like 'ebs_%'
    ORDER BY c.TABLE_NAME;""")

    columns = cursor.fetchall()

    db.close()

    # 获取表标题
    titles = list(map(lambda m: m[2], rows))

    # 以 tableName 为 key ， columns 为 value。
    # 构建 dict （ title:[{序号,}]）
    # // 提取对应表的字段列
    # let
    # items = data.filter((d) = > d.数据表中文名 == = key);
    #
    # // 按照字段在表中的序号排序
    #
    # items.sort((firstEl, secondEl) = > firstEl.序号 - secondEl.序号);
    #
    # // 移除数据表、数据表中文名字段
    # items.forEach((item) = > {
    #     delete
    # item.数据表;
    # delete
    # item.数据表中文名;
    # });
    #
    # hashmap[key] = items;
    dict = {}

    print("column:", columns[0])

    for title in titles:
        # 提取对应表的字段列
        items = list(filter(lambda c: c[2] == title, columns))
        print("items:", items)
        # 按照字段在表中的序号排序
        items = sorted(items, key=functools.cmp_to_key(lambda first, second: first[0] - second[0]))

        # 移除数据表、数据表中文名字段
        # items.forEach((item) = > {
        #     delete
        # item.数据表;
        # delete
        # item.数据表中文名;
        # });

        records = []

        for item in items:
            item = list(item)
            item.pop(1)
            item.pop(1)
            records.append(item)

        print(records)

        dict[title] = records

    print(len(dict))


if __name__ == '__main__':
    test()
