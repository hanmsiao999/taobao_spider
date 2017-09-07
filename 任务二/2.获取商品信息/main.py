import requests
import sys
sys.path.append("..")
import codecs, re, time, queue
import datetime, threading, os
from connectMysql import Mymysql
from main_page_jiexi import main_page_jiexi
from detail_content_jiexi import detail_content_jiexi
from descContent_jiexi import descContent_jiexi
from extend_information_jiexi import extend_information_jiexi
from rate_jiexi import rate_jiexi
from pic_jiexi import pic_jiexi


thread_num = 2
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


class crawl(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.f_log = None
        self.header = {'Host': 'www.taobao.com',
                       'Upgrade-Insecure-Requests': '1',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        self.set_ip()
        print (self.name,"初始化完毕:",self.ip)

    def set_ip(self):
        global  ip_count
        self.ip = get_ip()
        if self.f_log!=None:
            self.f_log.write("get ip:%s\n" % (self.ip))
        self.proxies = {
            'http': self.ip,
            'https': self.ip
        }
        ip_count+=1

    def get_page(self, url, host=None, reference=None):
            if host:
                self.header['Host'] = host
            if reference:
                self.header['Referer'] = reference
            error_time = 0
            while 1:
                  try:
                       if error_time == 3:
                           return False
                       response = self.session.get(url, headers=self.header, timeout=30, proxies=self.proxies)
                       if response.status_code != 200 and error_time == 1:
                          raise Exception("status_code error:" + str(response.status_code))

                       elif response.status_code != 200 and error_time == 0:
                             time.sleep(3)
                             error_time = 1
                             continue
                       elif response.status_code != 200 and error_time > 1:
                             return False

                       else:

                             try:
                                 content =  response.content.decode("gbk")
                                 return content,200
                             except Exception as ex:
                                 self.f_log.write("URL:%s decode Error:%s\n" % (url,str(ex)))
                                 return False, response.status_code
                  except Exception as ex:
                        self.set_ip()
                        self.f_log.write("get_page Error ,ex:%s,reget IP\n" % (str(ex)))
                        self.f_log.write("URL:%s\n" % (url))

                        if "10054" in str(ex) or "10053" in str(ex) or "强迫" in str(ex) or "拒绝" in str(ex) or "403" in str(ex):
                            pass
                        else:
                            error_time+=1

    def get_picture_comment(self, product_id, sellerId, update_time):
        try:
            current_page = 1
            while True:
                #print ("current_page:",current_page)
                #if current_page>=5:
                #    return "ok"
                pic_url = "https://rate.taobao.com/feedRateList.htm?auctionNumId=%s&userNumId=%s&currentPageNum=%s&pageSize=20&rateType=3&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&callback=jsonp_tbcrate_reviews_list" % (
                product_id, sellerId, str(current_page))
                pic_content, status_code = self.get_page(pic_url, host='rate.taobao.com')
                if not pic_content:
                    self.f_log.write("get_picture_comment error,status_code:%s \n" % status_code)
                    raise Exception("get_picture_comment error ")
                maxPage, pic_jiexi_re = pic_jiexi(product_id, pic_content, update_time,self.name)
                if pic_jiexi_re != 'ok':
                    self.f_log.write("pic_jiexi current_page error:" + str(current_page) + "\n")
                    raise Exception("pic_jiexi current_page:", str(current_page))
                else:
                    self.f_log.write("get_picture_comment succeed current_page:" + str(current_page) + "\n")
                if int(maxPage) == current_page:
                    return "ok"
                current_page += 1
                time.sleep(0.2)
        except Exception as ex:
            self.f_log.write("get_picture error:%s:current_page:%s\n" % (str(ex), str(current_page)))
            return False

    def main_method(self, product_id, total_sales_volume, shop_id):
        try:
            update_time = datetime.datetime.now().strftime("%Y-%m-%d")
            main_url = "https://item.taobao.com/item.htm?id=%s" % (product_id)

            # 获取主页内容
            mainPageConent, status_code = self.get_page(main_url, host="item.taobao.com")
            if status_code == 'no':
                self.f_log.write("%s can not crawl\n" % (main_url))
                return "ok"
            self.header['Referer'] = main_url
            if not mainPageConent:
                self.f_log.write(" get mainPageConent fail status_code:%s\n" % status_code)
                raise Exception("mainPageConent error")
            else:
                self.f_log.write("get mainPageConent succeed\n")
            if '下架' in mainPageConent:
                return 'ok'

            # 获取categroy_id，sellerId，descUrl
            categroy_id = re.findall('data-catid="(\d+)"', mainPageConent)
            if not categroy_id:
                raise Exception("categroy_id out of  index")
            else:
                categroy_id = categroy_id[0]
            sellerId = re.findall("sellerId\s*:\s*'(\d+)',", mainPageConent)
            if not sellerId:
                raise Exception("sellerId out of  index")
            else:
                sellerId = sellerId[0]
            descUrl = re.findall("location.protocol===(.*),", mainPageConent)
            if not descUrl:
                raise Exception("descUrl out of  index")
            else:
                descUrl = descUrl[0]

            # 申明商品字典
            product_information_Item_dict = {}
            product_information_Item_dict['shop_id'] = shop_id
            product_information_Item_dict['product_id'] = product_id
            product_information_Item_dict['update_time'] = update_time
            product_information_Item_dict['total_sales_volume'] = total_sales_volume
            self.f_log.write("categroy_id，sellerId，descUrl succeed\n")
            # 解析主页内容
            main_page_jiexi_re = main_page_jiexi(product_id, mainPageConent, update_time, product_information_Item_dict,self.name)
            if main_page_jiexi_re != 'ok':
                self.f_log.write("main_page_jiexi_fail\n")
                raise Exception("main_page_jiexi_re error")
            else:
                self.f_log.write("main_page_jiexi_succeed\n")

            # 获取detail页面
            detail_url = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=%s&sellerId=%s&modules=dynStock,qrcode,viewer,price,contract,duty,xmpPromotion,delivery,upp,activity,fqg,zjys,amountRestriction,couponActivity,soldQuantity,tradeContract&callback=onSibRequestSuccess" % (
                product_id, sellerId)
            detail_content, satus_code = self.get_page(detail_url, host="detailskip.taobao.com")
            if not detail_content:
                self.f_log.write("get detail_content fail %s\n" % str(satus_code))
                self.f_log.write(detail_url + "\n")
                raise Exception("detail_content error")
            else:
                self.f_log.write("get detail_content succeed\n")

            # 解析detail 页面
            detail_content_jiexi_re = detail_content_jiexi(product_id, detail_content, update_time,
                                                           product_information_Item_dict)
            if detail_content_jiexi_re != 'ok':
                self.f_log.write("detail_content_jiexi_re fail\n")
                raise Exception("detail_content_jiexi_re error")
            else:
                self.f_log.write("detail_content_jiexi_re succeed\n")

            # 获取描述内容
            descUrl = "https:" + descUrl.split(":")[2].strip()[1:-1]
            descContent, status_code = self.get_page(descUrl, host="desc.alicdn.com")
            if not descContent:
                self.f_log.write("get descContent fail,status_code:%s\n" % status_code)
                raise Exception("descContent Error")
            else:
                self.f_log.write("get descContent succeed\n")

            # 解析描述内容
            descContent_jiexi_re = descContent_jiexi(product_id, descContent, update_time,
                                                     product_information_Item_dict,self.name)
            if descContent_jiexi_re != 'ok':
                self.f_log.write("get descContent_jiexi fail\n")
                raise Exception("descContent_jiexi_re error")
            else:
                self.f_log.write("get descContent_jiexi succeed\n")

            # 累计评论获取
            detailCounturl = "https://rate.taobao.com/detailCount.do?itemId=%s" % (product_id)
            detailCountContent, status_code = self.get_page(detailCounturl, host="rate.taobao.com")
            if not detailCountContent:
                self.f_log.write("get detailCountContent fail,status_code:%s\n" % status_code)
                raise Exception("detailCount_Content Error")
            else:
                self.f_log.write("get detailCountContent succeed\n")
            detailCount = re.findall("\d+", detailCountContent)
            if not detailCount:
                self.f_log.write("detailCount index out of range\n")
                raise Exception("detailCount index out of range")
            else:
                self.f_log.write("detailCount succeed\n")
            product_information_Item_dict['cumulative_review'] = detailCount[0]

            # 看了还看了获取
            recommend_one_url = "https://tui.taobao.com/recommend?&callback=detail_recommend_viewed&appid=9&count=12&sellerid=%s&itemid=%s&categoryid=%s" % (
                sellerId, product_id, categroy_id)
            recommend_oneContent, status_code = self.get_page(recommend_one_url, host="tui.taobao.com")
            if not recommend_oneContent:
                self.f_log.write("get recommend_oneContent fail,status_code:%s\n" % status_code)
                raise Exception("recommend_oneContent Error")

            # 还买了
            recommend_two_url = "https://tui.taobao.com/recommend?callback=detail_recommend_bought&appid=11&" + "count=12&sellerid=%s&itemid=%s&categoryid=%s" % (
                sellerId, product_id, categroy_id)
            recommend_twoContent, status_code = self.get_page(recommend_two_url, host="tui.taobao.com")
            if not recommend_twoContent:
                self.f_log.write("get recommend_twoContent fail, status_code:%s\n" % status_code)
                raise Exception("recommend_twoContent Error")

            # 邻家好货
            recommend_third_url = "https://tui.taobao.com/recommend?itemid=%s&sellerid=%s&callback=jsonp1524&appid=3066" % (
                product_id, sellerId)
            recommend_thirdContent, status_code = self.get_page(recommend_third_url, host="tui.taobao.com")
            if not recommend_thirdContent:
                self.f_log.write("get recommend_thirdContent fail,status_code:%s\n" % status_code)
                raise Exception("recommend_thirdContent Error")

            # 拓展信息解析
            extend_information_jiexi_re = extend_information_jiexi(product_id, recommend_oneContent,
                                                                   recommend_twoContent, recommend_thirdContent,
                                                                   update_time)
            if not extend_information_jiexi_re:
                self.f_log.write("extend_information_jiexi_re fail\n")
                raise Exception("extend_information_jiexi error")
            else:
                self.f_log.write("extend_information_jiexi succeed\n")

            # 大家印象 及 评论数量
            rate_url = "https://rate.taobao.com/detailCommon.htm?auctionNumId=%s&userNumId=%s&callback=json_tbc_rate_summary" % (
                product_id, sellerId)
            rate_content, status_code = self.get_page(rate_url, host='rate.taobao.com')
            if not rate_content:
                self.f_log.write("get rate_content fail,status_code:%s\n" % (status_code))
                raise Exception("rate_content error")
            else:
                self.f_log.write("get rate_content succeed\n")
            # rate 解析
            rate_jiexi_re, comment_with_picture_num = rate_jiexi(product_id, rate_content, update_time,
                                                                 product_information_Item_dict)
            if not rate_jiexi_re:
                self.f_log.write("get rate_jiexi_re error\n")
                raise Exception("rate_jiexi_re error")
            else:
                self.f_log.write("rate_jiexi succeed\n")

            # 收藏数量获取
            collectcount_URL = "https://count.taobao.com/counter3?callback=jsonp87&keys=ICCP_1_%s" % (product_id)
            collectcount_Content, status_code = self.get_page(collectcount_URL, host='count.taobao.com')
            if not collectcount_Content:
                self.f_log.write("get collectcount_Content fail,status_code:%s\n" % (status_code))
                raise Exception("collectcount_Content error")
            else:
                self.f_log.write("get collectcount_Content succeed\n")
            # 解析收藏数量
            product_information_Item_dict['collection_number'] = re.findall("\d+", collectcount_Content.split(":")[1])[
                0]

            # 图片获取
            if str(comment_with_picture_num) != '0':
                get_picture_comment_re = self.get_picture_comment(product_id, sellerId, update_time)
                if get_picture_comment_re == 'ok':
                    self.f_log.write("get_picture_comment succeed\n")
                else:
                    raise Exception("get_picture_comment_re ERROR" % ())
            else:
                self.f_log.write("not exist picture\n")

            # 插入产品信息
            sql = """
                          insert  into product_information(
            			                        shop_id,
                                                total_sales_volume,
            	                                product_name,
            	                                product_profile,
                                                cumulative_review,
                                                transaction_volume,
                                                price,
                                                taobao_price,
                                                place_of_delivery,
                                                express_fee,
                                                amount_of_inventory,
                                                promise,
                                                payment_method,
                                                collection_number ,
                                                note,
                                                update_time,
            				                    product_id,comment_with_picture_num,
            				                    append_comment_num,moderate_comment_num,negative_comment_num,
            				                    refund_comment_num,positive_comment_num
            	                                  ) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
                   """ % (
                shop_id, total_sales_volume, product_information_Item_dict['product_name'],
                product_information_Item_dict['product_profile'], product_information_Item_dict['cumulative_review'],
                product_information_Item_dict['transaction_volume'],
                product_information_Item_dict['price'],
                product_information_Item_dict['taobao_price'],
                product_information_Item_dict['place_of_delivery'], product_information_Item_dict['express_fee'],
                product_information_Item_dict['amount_of_inventory'],
                product_information_Item_dict['promise'], product_information_Item_dict['payment_method'],
                product_information_Item_dict['collection_number'], product_information_Item_dict['note'], update_time,
                product_id,
                product_information_Item_dict['comment_with_picture_num'],
                product_information_Item_dict['append_comment_num'],
                product_information_Item_dict['moderate_comment_num'],
                product_information_Item_dict['negative_comment_num'],
                product_information_Item_dict['refund_comment_num'],
                product_information_Item_dict['positive_comment_num']
            )
            x = Mymysql()
            x._GetConnect()
            try:
                x.ExecNonQuery(sql)
            except:
                print(sql)
                raise Exception("product information insert error")
            finally:
                x.EndSql()

            return "ok"







        except Exception as ex:
            self.f_log.write("main method error:%s:%s\n" % (str(ex), self.name))
            return False

    def run(self):
        global lock
        log_path = os.path.join("log", self.name + ".log")
        while True:
            try:
                self.f_log = codecs.open(log_path, "a+", encoding="utf-8")
                self.f_log.write("=======================================\n")
                self.session = requests.Session()
                if product_Q.empty():
                    self.f_log.write("%s:%s:%s\n" % (self.name, 'break', str(time.time() - a)))
                    break
                item = product_Q.get(timeout=20)
                product_id = item[0]
                #lock.acquire()
                #print("%s:%s:%s" % (product_id, "begin", self.name))
                #lock.release()
                self.f_log.write("%s:%s\n" % (product_id, ":begin"))
                begin = time.time()
                re_main = self.main_method(item[0], item[1], item[2])  # product_id total_sales_volume shop_id
                if re_main == 'ok':
                    now = datetime.datetime.now()
                    now = now.strftime('%Y-%m-%d %H:%M:%S')
                    lock.acquire()
                    f = codecs.open("has_craw.txt", "a+", encoding="utf-8")
                    f.write("%s|%s\n" % (product_id, now))
                    f.close()
                    print(product_id, self.name, "done", now, ":run for ", round(time.time() - begin, 4), 's')
                    lock.release()
                    self.f_log.write(product_id + ":" + self.name + ":done:" + now + "\n")
                    time.sleep(1)

            except Exception as ex:
                self.f_log.write("%s:%s:%s\n" % ("fucntion run error", str(ex), self.name))
            finally:
                self.f_log.close()
                self.session.close()


import threading

lock = threading.Lock()
get_lock = threading.Lock()
his_ip = []
a = time.time()
# 获取带爬商品ID 列表
x = Mymysql()
x._GetConnect()
sql = "SELECT product_id,total_sales_volume,shop_id FROM `product_list`; "
target_ids = x.ExecQuery(sql)
x.EndSql()

print("loading...end")
#f = codecs.open("thisTurn.txt", "r+", encoding="utf-8")
#target_ids = f.readlines()
#target_ids = [item[:-1].strip().split(":") for item in target_ids]
#target_ids = list(filter(lambda x: len(x) == 3, target_ids))
#f.close()
print("商品数:", len(target_ids))

# has crawl
if not os.path.isfile("has_craw.txt"):
    f = open("has_craw.txt", "w+")
    f.close()
f = codecs.open("has_craw.txt", "r+", encoding="utf-8")
has_crawl_IDS = f.readlines()
f.close()
IDS = [item.split("|")[0] for item in has_crawl_IDS]
has_crawl_IDS_num = len(IDS)

product_Q = queue.Queue()
ip_list = queue.Queue()
for item in target_ids[has_crawl_IDS_num:]:
    #if item[0] not in IDS:
        product_Q.put(item)
        #break



print("loading end")

print("This time will crawl %s " % (str(product_Q._qsize())))
thread_num = product_Q._qsize() if product_Q._qsize() < thread_num else thread_num
ths = []
for i in range(thread_num):
    ths.append(crawl())

for item in ths:
    # time.sleep(3)
    item.start()

while len(ths):
    thread = ths.pop()
    if thread.isAlive():
        thread.join()

print ("共使用ip %s 个" % str(ip_count))
print("all done")
