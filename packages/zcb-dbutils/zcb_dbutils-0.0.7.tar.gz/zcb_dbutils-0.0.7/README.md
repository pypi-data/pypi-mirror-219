# dbutils

使用方法

```python
from zcb_dbutils import DBConnection
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d ] %(levelname)s %(message)s',
                    datefmt='%d %b %Y,%a %H:%M:%S', #日 月 年 ，星期 时 分 秒
                    )

dbconn = DBConnection(host='localhost', port=3306, user='root', password='', database='basic')

ret = dbconn.fetch_one("select * from tb_user1 where id = 1000")
print(ret)

ret = dbconn.showtable('basic', 'tb_user')
print(pd.DataFrame.from_dict(ret))

ret = dbconn.show_table_index('basic', 'tb_user')
print(pd.DataFrame.from_dict(ret))

rows = dbconn.fetch_list('select user_id,id from tb_user')
print(rows)

id = dbconn.insert('insert into tb_role (role_name,role_type,remark_info,created,updated) value (%s,1,%s,0,0)',('xxx', 'xxxx'))
dbconn.commit()
print(id)
```