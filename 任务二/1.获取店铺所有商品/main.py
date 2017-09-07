# coding:utf-8
from good_jiexi import good_jiexi
import sys
sys.path.append("..")
import requests
from lxml import etree
import codecs
import re,time,os,queue,threading
import datetime


# 配置爬取线程数
thread_num =2# 20 的整数倍
ip_count = 0
ip_url = "http://www.xdaili.cn/ipagent//greatRecharge/getGreatIp?spiderId=49595241242b4c7f80d36a119d37d245&orderno=YZ20175265966odSeF2&returnType=1&count=2"


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
                time.sleep(120)
            if '今日提取已达上限' in text:
                print("今日提取已达上限")
                time.sleep(120)
            text = text.split("\r\n")
            for item in text:
                ip_list.put(item)
        except Exception as ex:
            print("get_ip", str(ex))
            if "提取数量已用完" in str(ex):
                print("提取数量已经用完")
                time.sleep(120)
            continue
    get_lock.release()
    return ip_list.get()





class crawl(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.f_log = None
        self.header = {'Host': 'www.taobao.com',
                       'Upgrade-Insecure-Requests': '1',
                       'X-Requested-With':'XMLHttpRequest',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        self.set_ip()
        print (self.name,"初始化完毕:",self.ip)

    def find_all_link(self, html):
        link = re.findall("href=\"//(\S+\.taobao\.com/\S+\?search=y)\"", html)
        if len(link) >= 1:
            return link[0]
        link = re.findall("\"//(\S+\.taobao\.com/search.htm)\"", html)
        if len(link) >= 1:
            return link[0]
        link = re.findall("\"//(\S+search=y)\"", html)
        if len(link) >= 1:
            return link[0]
        link = re.findall("//(\S+search.htm\?search=y)\"", html)
        if len(link) >= 1:
            return link[0]
        link = re.findall("//(\S+search=y)\"", html)
        if len(link) >= 1:
            return link[0]
        return False

    def set_ip(self):
            global ip_count
            self.ip = get_ip()
            #print ("%s get ip %s" % (self.name,self.ip))
            if self.f_log != None:
                self.f_log.write("get ip:%s\n" % (self.ip))
            self.proxies = {
                'http': self.ip,
                'https': self.ip
            }
            ip_count += 1

    def get_page(self, url, host=None, reference=None):
            if host:
                self.header['Host'] = host
            if reference:
                self.header['Referer'] = reference
            error_time = 0
            while 1:
                try:
                    if error_time ==2:
                        return False,302
                    response = self.session.get(url, headers=self.header, timeout=10)#, proxies=self.proxies)
                    if response.status_code != 200 and error_time == 1:
                        raise Exception("status_code error:" + str(response.status_code))

                    elif response.status_code != 200 and error_time == 0:
                        time.sleep(3)
                        error_time = 1
                        continue
                    elif response.status_code != 200 and error_time > 1:

                        return False, response.status_code

                    else:
                        try:
                            content = response.content.decode("gbk")
                            return content, 200
                        except Exception as ex:
                            self.f_log.write("URL:%s decode Error:%s\n" % (url, str(ex)))
                            return False, response.status_code
                except Exception as ex:
                    #print (ex)
                    self.set_ip()
                    self.f_log.write("get_page Error ,ex:%s,reget IP\n" % (str(ex)))
                    self.f_log.write("URL:%s\n" % (url))

                    if "10054" in str(ex) or "10053" in str(ex) or "强迫" in str(ex) or "拒绝" in str(ex) or "403" in str(
                            ex):
                        pass
                    else:
                        error_time += 1

    def main_method(self, item):
        try:
            global update_time
            global lock

            shop_ID = re.findall("\d+", item)[0]
            host = item.replace("//", "")
            url = "https:" + item
            #header = {'Host': 'www.taobao.com',
            #          'Upgrade-Insecure-Requests': '1',
            #          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
            #header['Host'] = host
            # 访问数字主页
            content,status_code = self.get_page(url, host=host)
            if status_code == 302 or "没有找到相应的店铺信息" in content:
                self.f_log.write("%s: not exists" % (url))
                return "ok"
            if not content:
                raise Exception("get mainpage error %s:%s\n" % (url,str(status_code)))
            all_links = self.find_all_link(content)
            if all_links == False:
                raise Exception("item find_all_link false")
            shop_id = re.findall("\"shopI[dD]\":(.*?),", content)[0].strip()[1:-1]
            # 访问所有商品
            host = re.findall(".*?taobao.com", all_links)
            if not host:
                raise Exception("all_link host find error")
            host = host[0]
            main_url = "https://" + host
            url = "https://" + all_links
            page = 1
            error_time = 0
            while True:
                   content, status_code = self.get_page(url, host=host)
                   if not content:
                      raise Exception("get page error %s:%s\n" % (url, str(status_code)))
                   tree = etree.HTML(content)
                   page = 0
                   if 'pagination' in content:
                       result = good_jiexi(shop_ID, shop_id, content, page, update_time, self.name)
                       if result != 'ok':
                           raise Exception(asyn_URL + "jiexi error\n")
                       self.f_log.write("%s:%s:done\n" % (shop_ID, str(page)))
                       try:  # 下一页
                           if tree.xpath(".//div[@class='pagination']//a[last()]")[0].get("class").strip() == 'disable':
                               return "ok"
                           next_page_url = tree.xpath(".//a[@class='J_SearchAsync next']")[0].get("href")
                       except Exception as ex:
                           path_to_write = os.path.join("re_jiexi", "%s_%s_nextpage.txt" % (shop_id, str(page)))
                           f = open(path_to_write, "w+")
                           f.write(content)
                           f.close()
                           raise Exception("next page error:%s " % (str(ex)))
                       # print (next_page_url)
                       url = "https:" + next_page_url
                       if tree.xpath(".//div[@class='pagination']//a[last()]")[0].get("class").strip() == 'disable':
                          return "ok"
                       continue

                   if 'J_ShopAsynSearchURL' not in content:
                           if error_time == 0 :
                               error_time += 1
                               time.sleep(3)
                               continue
                           else:
                               self.f_log.write("AsynSearchURL not in content" + "\n")
                               path_to_write = os.path.join("re_jiexi", "%s_%s_AsynSearchURL.txt" % (shop_id, str(page)))
                               f = open(path_to_write, "w+")
                               f.write(content)
                               f.close()
                   # 得到异步网页
                   try:
                       AsynSearchURL = tree.xpath(".//input[@id='J_ShopAsynSearchURL']")
                       if AsynSearchURL:
                           AsynSearchURL = AsynSearchURL[0].get("value")
                       else:
                           AsynSearchURL = re.findall('value="(/i/asynSearch.htm.*?)"', content)
                           if AsynSearchURL:
                               AsynSearchURL = AsynSearchURL[0]
                           else:
                               raise Exception("no  find AsynSearchURL")
                       asyn_URL = main_url + AsynSearchURL
                       #print (main_url,AsynSearchURL)
                   except Exception as ex:
                      self.f_log.write("AsynSearchURL get error" + "\n")
                      self.f_log.write("%s\n" % (str(ex)))
                      path_to_write = os.path.join("re_jiexi", "%s_%s_AsynSearchURL.txt" % (shop_id, str(page)))
                      f = open(path_to_write, "w+")
                      f.write(content)
                      f.close()
                      return False

                   # 访问异步网页
                   content,status_code = self.get_page(asyn_URL,reference=url,host=host)
                   if "anti_Spider-checklogin&smCharset" in content:
                       print ("anti_Spider")
                       time.sleep(10000)
                   if status_code!=200:
                      raise Exception("asyn_URL error:%s ,stauts_code:%s" % (asyn_URL,str(status_code)))
                   content = content.replace("\\", "")
                   if 'no-result-new' in content:
                       return "ok"
                   #解析异步网页
                   result = good_jiexi(shop_ID, shop_id, content, page, update_time,self.name)
                   if result != 'ok':
                       raise Exception(asyn_URL + "jiexi error\n")
                   self.f_log.write("%s:%s:done\n" % (shop_ID, str(page)))
                   page += 1
                   try:  # 下一页
                       tree = etree.HTML(content)
                       if tree.xpath(".//div[@class='pagination']//a[last()]")[0].get("class").strip() == 'disable':
                          return "ok"
                       next_page_url = tree.xpath(".//a[@class='J_SearchAsync next']")[0].get("href")
                   except Exception as ex:
                        path_to_write = os.path.join("re_jiexi","%s_%s_nextpage.txt" % (shop_id,str(page)))
                        f=  open(path_to_write,"w+")
                        f.write(content)
                        f.close()
                        raise Exception("next page error:%s " % (str(ex)))
                   #print (next_page_url)
                   url = "https:" + next_page_url
                   time.sleep(0.5)
                   error_time = 0
            return "ok"

        except Exception as ex:
            self.f_log.write(str(ex) + "\n")
            return False

    def run(self):
        global lock
        while True:
            try:
                self.session = requests.Session()
                log_path = os.path.join("log", self.name + ".log")
                self.f_log = codecs.open(log_path, "a+", encoding="utf-8")
                if user_list.empty():
                    global a
                    self.f_log.write("%s:%s:%s\n" % (self.name, 'break', str(time.time() - a)))
                    break
                item = user_list.get()
                self.f_log.write("%s get %s\n" % (self.name,item))
                #print ("%s get %s" % (self.name,item))
                begin = time.time()
                re = self.main_method(item)

                if re == 'ok':
                    now = datetime.datetime.now()
                    now = now.strftime('%Y-%m-%d %H:%M:%S')
                    f = codecs.open("has_craw.txt", "a+", encoding="utf-8")
                    f.write("%s:%s\n" % (item, now))
                    f.close()
                    lock.acquire()
                    print(item + ":" + self.name + ":done:" + now + ":run for " + str(time.time() - begin))
                    lock.release()
                    self.f_log.write(item + ":" + self.name + ":done:" + now + "\n")

            except Exception as ex:
                self.f_log.write("%s:\n" % (str(ex)))
            finally:
                self.f_log.close()
                self.session.close()



import threading

lock = threading.Lock()
get_lock = threading.Lock()
update_time = datetime.datetime.now().strftime("%Y-%m-%d")

url_file = os.path.join("../all_url.csv")
f = open(url_file, "r+")
results = f.readlines()
f.close()

results = [item[:-1] for item in results]  # 总url

if not os.path.isfile("has_craw.txt"):
    f = open("has_craw.txt", "w+")
    f.close()
f = codecs.open("has_craw.txt", "r+", encoding="utf-8")
IDS = f.readlines()
f.close()
IDS = [item.split(":")[0] for item in IDS]

user_list = queue.Queue()
ip_list = queue.Queue()
print("put ing~")
for item in results[:2]:
    if item not in IDS:
        #user_list.put("//shop71221132.taobao.com")
        user_list.put(item)
        #break


print("put finish")

print("this time will crawl %s shops" % (str(user_list._qsize())))

a = time.time()
ths = []
for i in range(thread_num):
    ths.append(crawl())

for th in ths:
    time.sleep(2)
    th.start()

while len(ths):
    thread = ths.pop()
    if thread.isAlive():
        thread.join()
        b = time.time()

print ('use %s IP' % (str(ip_count)))
print('all end')
