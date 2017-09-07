import requests
import sys,os
sys.path.append("..")
from connectMysql import Mymysql
import threading
import time
import codecs,datetime
import queue


thread_num = 5
ip_count = 0
ip_url = "http://www.xdaili.cn/ipagent/greatRecharge/getGreatIp?spiderId=49595241242b4c7f80d36a119d37d245&orderno=YZ20175265966odSeF2&returnType=1&count=5"


# 锁
lock = threading.Lock()
get_lock = threading.Lock()


#队列
ip_list = queue.Queue()
img_list = queue.Queue()


def get_ip():
    global ip_url
    get_lock.acquire()
    while ip_list.empty():
        try:
            request_url = ip_url
            response = requests.get(request_url)
            time.sleep(5)
            text = response.content.decode("utf-8").strip()
            if "频繁" in text:
                time.sleep(5)
                continue
            if '暂无可用订单' in text:
                print("代理IP已经欠费")
                time.sleep(1000000)
            if '今日提取已达上限' in text:
                print ("今日提取已达上限")
                time.sleep(1000000)
            text = text.split("\r\n")
            for item in text:
                ip_list.put(item)
        except Exception as ex:
            print("get_ip", str(ex))
            if "提取数量已用完" in str(ex):
                print ("提取数量已经用完")
                time.sleep(12000)
            continue
    get_lock.release()
    return ip_list.get()


# 生产者
class Producer(threading.Thread):  
    def __init__(self):  
        threading.Thread.__init__(self)
        self.x = Mymysql()
        self.x._GetConnect()
        sql = "SELECT pic_md5,img_src,id FROM `image` where isSaved_Picture='0' limit  20000" # where id >
        self.cur = self.x.ExecQueryGetcur(sql)
        
    def run(self):
        while True:
            item = self.cur.fetchone()
            if item == None:break
            img_list.put(item)
        print("put down~")

    def __del__(self):
        self.x.EndSql()



class Customer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.y = Mymysql()
        self.y._GetConnectY()
        self.header = {'Host': 'img.alicdn.com',
                       'Upgrade-Insecure-Requests': '1',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        self.set_ip()
        print (self.name,"初始化完毕:",self.ip)


    def set_ip(self):
        global  ip_count
        self.ip = get_ip()
        self.proxies = {
            'http': self.ip,
            'https': self.ip
        }
        ip_count+=1


    def get_image(self,url,id):
        error_time = 0
        while 1:
            try:
                if error_time == 3:
                    return False
                response = requests.get(url, headers=self.header, timeout=3,proxies=self.proxies)
                if response.status_code != 200 and error_time == 1:
                   raise Exception("status_code error:" + str(response.status_code))
                elif response.status_code != 200 and error_time == 0:
                    time.sleep(3)
                    error_time = 1
                    continue
                else:
                    return response.content
            except Exception as ex:
                   self.set_ip()
                   lock.acquire()
                   print("%s encouter error %s: id=%s" % (self.name, str(ex),id))
                   lock.release()
                   error_time+=1
                
                
    def run(self):
        global lock
        while True:
            try:
              pic_md5, url, id = img_list.get()
              save_path = r"D:\image\%s.jpg" % (pic_md5)
              url = url.strip()
              if not url.startswith("http"):
                 url = "https:"+url

              try:
                  sql = "insert into img_unique(img_unique) values ('%s')" % (pic_md5)
                  self.y.ExecNonQuery(sql)
              except Exception as ex:
                  if '1062' in str(ex):
                      sql = "update image set isSaved_Picture='1' where id='%s'" % (id)
                      self.y.ExecNonQuery(sql)
                      now = datetime.datetime.now()
                      now = now.strftime('%Y-%m-%d %H:%M:%S')
                      lock.acquire()
                      print("1062 %s:%s:%s done at %s" % (self.name,pic_md5,str(id),now))
                      lock.release()
                  else:
                      print (ex,url)
                  continue
                      
              content = self.get_image(url,id)
              if not content:
                 raise Exception("no content")

              f = open(save_path,"wb")
              f.write(content)
              f.close()

              sql = "update image set isSaved_Picture='1' where id='%s'" % (id)
              self.y.ExecNonQuery(sql)
              now = datetime.datetime.now()
              now = now.strftime('%Y-%m-%d %H:%M:%S')
              lock.acquire()
              print("%s:%s:%s done at %s" % (self.name,pic_md5,str(id),now))
              lock.release()
            except Exception as ex:
                log_path = os.path.join("log", self.name + ".log")
                f = codecs.open(log_path,"a+",encoding="utf-8")
                f.write("%s:%s\n" % (url,str(ex)))
                f.write("======================\n")
                f.close()

    def __del__(self):
        self.y.EndSql()

save_path = r"D:\image"
if not os.path.exists(save_path):
   os.mkdir(save_path)
producer = Producer()
producer.start()
Customer_list = []

for i in range(thread_num):
    Customer_list.append(Customer())

for th in Customer_list:
    th.start()
    

                
                
        
        
         
