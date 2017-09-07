import pymysql
class Mymysql:
      def __init__(self):
          self.host = 'localhost'
          self.user = 'root'
          self.passwd = ''
          self.db='taobao_test3'
          self.port = 3306
          
      def _GetConnect(self):
          self.conn = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user=self.user,
                             password=self.passwd,
                             db=self.db,
                             charset='utf8')
          self.cur = self.conn.cursor()

      def ExecNonQuery(self,sql):
          self.cur.execute(sql)
          self.conn.commit()

      def EndSql(self):
          self.conn.close()
          self.cur.close()


      def ExecQuery(self,sql):
          self.cur.execute(sql)
          results = self.cur.fetchall()
          return results

      def ExecQueryGetcur(self, sql):
          self.cur.execute(sql)
          return self.cur

      def _GetConnectY(self):
          self.conn = pymysql.connect(host='127.0.0.1',
                                      port=3306,
                                      user=self.user,
                                      password=self.passwd,
                                      db=self.db,
                                      charset='utf8')
          # self.cur = self.conn.cursor(pymysql.cursors.SSCursor)
          self.cur = self.conn.cursor()
            

if __name__ == '__main__':
   x = Mymysql()
   x._init_(host='localhost',user='root',passwd='wenyuan123',db='taobao')
   x._GetConnect()
   sql = "select product_id from product_information"
   target_ids = x.ExecQuery(sql)
  
      


