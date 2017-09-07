# coding:utf-8
import os
import codecs
import re
import json
import datetime
import uuid
from connectMysql import Mymysql
from util import get_pic_md5







def pic_jiexi(product_id, pic_content_original,update_time,thread_name):
    try:
        x = Mymysql()
        x._GetConnect()
        pic_content = pic_content_original.strip()
        #pic_content = re.findall("\((.*?)\)", pic_content)[0]
        begin_index = pic_content.index("(")
        end_index = pic_content.rindex(")")
        pic_content = pic_content[begin_index+1:end_index]
        #try:
        pic_content = json.loads(pic_content, encoding="gbk")
        #except Exception as ex:
        #    print (ex)
        #    print(pic_content)
        #    time.sleep(36000)
        max_page = pic_content['maxPage']
        comments = pic_content['comments']
        for item in comments:
            customer_name = item['user']['nick']
            rate = item['user']['displayRatePic'].split('.')[0]
            review_id = item['rateId']
            review_type = '3'
            content = item['content']
            if item['date']:
                review_info = datetime.datetime.strptime(item['date'].strip(),u'%Y年%m月%d日 %H:%M')
                review_date = review_info.date()
                review_time = review_info.time()
            else:
                review_date_info = ""
                review_date = '0000-00-00'
                review_time = '00:00:00'

            count_num = item['useful']
            refund_time = ""
            Brief_information = item['auction']['sku']

            # 图片插入
            count = 1
            photos = item['photos']
            for photo in photos:
                src = photo['url']
                img_id = uuid.uuid1()
                from_who = '2'
                position = '4'
                sequence = count
                pic_md5 = get_pic_md5(src, product_id)
                sql = """
                      insert into image(pic_md5,product_id,img_src,position,sequence,update_time,from_who,review_id)
                              values('%s','%s','%s','%s','%s','%s','%s','%s')
                      """ % (pic_md5,product_id,src,position,sequence,update_time,from_who,review_id)
                try:
                    x.ExecNonQuery(sql)
                    count +=1
                except Exception as ex:
                       print (ex)
                       print (sql)
                       print ("=============================")
                       continue
            back_comment = ""
            back_comment_day = ""
            # 追加解析
            append_list = item['appendList']
            for item_append in append_list:
                count = 0
                for item_append_photos in item_append['photos']:
                    src = item_append_photos['thumbnail']
                    img_id = uuid.uuid1()
                    from_who = '2'
                    position = '4'
                    sequence = count
                    pic_md5 = get_pic_md5(src, product_id)
                    sql = """
                                          insert into image(pic_md5,product_id,img_src,position,sequence,update_time,from_who,review_id)
                                                  values('%s','%s','%s','%s','%s','%s','%s','%s')
                                          """ % (
                        pic_md5, product_id, src, position, sequence, update_time, from_who, review_id)
                    try:
                        x.ExecNonQuery(sql)
                        count += 1
                    except Exception as ex:
                        print(ex)
                        print(sql)
                        print("=============================")
                        continue
                back_comment = item_append['content']
                back_comment_day = item_append['dayAfterConfirm']
                break
            content = content.replace("'","")
            content = content.replace("\\","")
            content = content.replace("?","")
            back_comment = back_comment.replace("'","")
            back_comment =  back_comment.replace("\\","")
            back_comment = back_comment.replace("?", "")
            sql = """
                             insert into product_comment(product_id,review_id,customer_name,rate,
                                    review_type,content,review_date,review_time,Brief_information,back_comment,
                                    back_comment_day,count_num,refund_time,update_time)
                             values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
                             """ % (product_id, review_id, customer_name, rate, review_type,
                                    content, review_date, review_time,
                                    Brief_information, back_comment, back_comment_day, count_num, refund_time,
                                    update_time)
            try:
                x.ExecNonQuery(sql)
                # print sql
            except Exception as ex:
                    print(ex)
                    print(sql)
                    print("=============================")
                    continue

        return max_page, "ok"

                
            
    except Exception as ex:
        print(product_id, "pic_jiexi", "error:", ex)
        return -1, False
    finally:
        x.EndSql()

