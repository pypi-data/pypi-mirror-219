from zcb_dbutils import DBConnection
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d ] %(levelname)s %(message)s',
                    datefmt='%d %b %Y,%a %H:%M:%S', #日 月 年 ，星期 时 分 秒
                    )

dbconn = DBConnection(host='localhost', port=3306, user='root', password='mysql', database='basic')

ret = dbconn.fetch_one("select * from tb_user1 where id = 1000")
print(ret)

ret = dbconn.showtable('basic', 'tb_user')
print(pd.DataFrame.from_dict(ret))

ret = dbconn.show_table_index('basic', 'tb_user')
print(pd.DataFrame.from_dict(ret))

rows = dbconn.fetch_list('select user_id,id from tb_user')
print(rows)

# id = dbconn.insert('insert into tb_role (org_id,role_no,role_name,role_type,remark_info,created,updated) value (1,1,%s,1,%s,0,0)',('xxx', 'xxxx'))
# dbconn.commit()
# print(id)

ret1 = []
ret2 = []
dbconn.batch_exec("select * from tb_user;select * from tb_role;", [])
print(ret1)
print(ret2)