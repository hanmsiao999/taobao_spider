from connectMysql import Mymysql

x = Mymysql()
#x.__init__(host='localhost',user='root',passwd='wenyuan123',db='taobao')
x._GetConnect()
sql = "select * from shop_homepage"
target_ids = x.ExecQuery(sql)
print (target_ids)
