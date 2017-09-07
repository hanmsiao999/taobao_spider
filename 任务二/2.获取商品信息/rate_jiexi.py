import os
import codecs, json
from lxml import etree
import re
from connectMysql import Mymysql
import uuid


def rate_jiexi(product_id, content, update_time, item_dict):
    try:
        x = Mymysql()
        x._GetConnect()
        begin_index = content.index("(")
        end_index = content.rindex(")")
        content = content[begin_index + 1:end_index]
        all_info = json.loads(content,encoding="gbk")
        data = all_info['data']
        impress_item = data['impress']
        for impress in impress_item:
            impress_type = impress['title']
            impress_count = impress['count']
            impress_id = uuid.uuid1()
            sql = """
                     insert  into product_impress(impress_id,product_id,
                                                 impress_type,impress_count,update_time) values
                                                 ('%s','%s','%s','%s','%s')
                     """ % (impress_id,product_id,impress_type,impress_count,update_time)
            try:
                   x.ExecNonQuery(sql)
            except Exception as ex:
                      print (ex)
                      print (sql)
                      print ("=============================")
                      continue
        # bar info
        comment_with_picture_num = data['count']['pic']
        append_comment_num = data['count']['additional']
        moderate_comment_num = data['count']['normal']
        negative_comment_num = data['count']['bad']
        refund_comment_num = all_info['sellerRefundCount']

        item_dict['comment_with_picture_num'] = comment_with_picture_num
        item_dict['append_comment_num'] = append_comment_num
        item_dict['moderate_comment_num'] = moderate_comment_num
        item_dict['negative_comment_num'] = negative_comment_num
        item_dict['refund_comment_num'] = refund_comment_num
        item_dict['positive_comment_num'] = data['count']['good']
        
        
            
        return "ok",comment_with_picture_num
    except Exception as ex:
        print(product_id, "rate_jiexi", "error:", ex)
        return False,-1

    finally:
        x.EndSql()
