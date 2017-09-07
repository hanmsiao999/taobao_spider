# coding:utf-8
from lxml import etree
import re
from connectMysql import Mymysql


def first_or_zero(item):
    return -1 if len(item) == 0 else item[0]


def shop_service_jiexi(shop_id, content, update_time):
    try:
        x = Mymysql()
        x._GetConnect()
        tree = etree.HTML(content)
        items = tree.xpath(".//li[@class='service-item']//h3[@class='name']/text()")
        refund_day_for_no_reason = delivery_hour_after_payment = -1
        for item in items:
            if refund_day_for_no_reason == -1:
                refund_day_for_no_reason = first_or_zero(re.findall(u"(\d+)天无理由退货", item))
            if delivery_hour_after_payment == -1:
                delivery_hour_after_payment = first_or_zero(re.findall(u"(\d+)小时发货", item))
        sql = """
              update seller_info set refund_day_for_no_reason = '%s',
                                     delivery_hour_after_payment = '%s'
                                     where shop_id = '%s' and update_time = '%s'
              """ % (refund_day_for_no_reason, delivery_hour_after_payment, shop_id, update_time)
        try:
            x.ExecNonQuery(sql)
        except Exception as ex:
            print(ex)
            print(sql)
            print("=============================")
        x.EndSql()
        return "ok"

    except Exception as ex:
        print(shop_id, "shop_service_jiexi", "error:", ex)
        x.EndSql()
        return False
