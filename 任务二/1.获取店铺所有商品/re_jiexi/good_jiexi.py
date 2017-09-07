#coding:utf-8
# 格式:商品ID,URL,名称,价格
import os, re,codecs
from lxml import etree
import datetime,time

def good_jiexi(shop_ID, shop_id ,content,page,update_time,thread_name):
    try:
        
        count = 0
        tree = etree.HTML(content)
        dls = tree.xpath(".//dl[contains(@class,'item')]")
        #now = datetime.datetime.now()
        #otherStyleTime = now.strftime("%Y-%m-%d")
        path = os.getcwd()
        parent_path = os.path.dirname(path)
        count= 0
        if len(dls)!=0:
            for item in dls:
                #price = item.xpath(".//*[@class='c-price']//text()")
                #if len(price)==0:
                #   continue
                #price = price[0].strip()
                detail_a = item.xpath(".//dd[@class='detail']/a")
                if not detail_a:
                    continue
                detail_a = detail_a[0]
                #name = detail_a.xpath(".//text()")[0].strip()
                url = detail_a.get("href")
                id = re.findall("id=(\d+)",url)
                if len(id) == 0:
                    continue
                id = id[0]
                
                sale_num = item.xpath(".//*[@class='sale-num']/text()")
                if len(sale_num)==0:
                    sale_num = -1
                else:
                    sale_num = sale_num[0]
                count+=1
                sql = "insert  ignore into product_list(shop_id,product_id,total_sales_volume,update_time)\
                values('%s','%s','%s','%s')" % (shop_id,id,sale_num,update_time)
                count+=1
               
                
               
    
        div = tree.xpath(".//div[@class='item']")
        if len(div)!=0:
            for item in div:
                #price = item.xpath(".//div[@class='price']/strong/text()")[0].strip()
                #price = re.findall("\d+.?\d+",price)[0]
                sale_num = item.xpath(".//*[@class='sale-num']//text()|.//*[@class='sales-amount']//text()")
                if len(sale_num)==0:
                    sale_num = -1
                else:
                    sale_num = sale_num[0]
                    sale_num = re.findall("\d+", sale_num)
                    sale_num = sale_num[0] if len(sale_num)>0  else -1


                    
                detail_a = item.xpath(".//div[@class='desc']/a")
                if not detail_a:
                    continue
                detail_a = detail_a[0]
                #name = detail_a.xpath(".//text()")[0].strip()
                url = detail_a.get("href")
                id = re.findall("id=(\d+)",url)
                if len(id) ==0:
                    continue
                id = id [0]
                #print id,name,url,price
                count+=1
                sql = "insert  ignore into  product_list(shop_id,product_id,total_sales_volume,update_time)\
                        values('%s','%s','%s','%s')" % (shop_id,id,sale_num,update_time)
                
               
                
        return "ok"
    except Exception as ex:
           print (ex)
           save_path = os.path.join("re_jiexi","%s_%s.txt" % (shop_ID,page))
           f = codecs.open(save_path,"w+",encoding="utf-8")
           f.write(content)
           f.close()
           return False
   

if __name__=="__main__":
    f =  codecs.open("57235686_2.txt","r+",encoding="utf-8")
    content = f.read()
    f.close()
    good_jiexi(1,1,content,1,1,1)
    
        
   
    

    
    
    
    
