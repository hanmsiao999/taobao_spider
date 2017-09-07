# coding:utf-8
import os
import codecs
import re
import json


def detail_content_jiexi(product_id, content, update_time,item_dict):
    try:
        content = content[:-2]
        content = content.replace("onSibRequestSuccess(", "")
        if json.loads(content)['code']['message'] != 'SUCCESS':
            return False
        detail_dict = json.loads(content)['data']

        # 价格
        price = detail_dict['price']
        item_dict['price'] = price

        # 淘宝价
        price = None
        taobao_price = detail_dict['promotion']['promoData']
        for key in taobao_price:
            for item in taobao_price[key]:
                if 'price' in item:
                    if price is None or float(item['price']) < price:
                        price = float(item['price'])
        taobao_price = price if price is not None else -1
        item_dict['taobao_price'] = taobao_price

        # 库存
        amount_of_inventory  = detail_dict['dynStock']['stock']
        item_dict['amount_of_inventory'] = amount_of_inventory

        # 承诺
        promise_digital = ""
        promise = detail_dict['tradeContract']['service']
        promise = [item['title'].strip() for item in promise]
        promise = list(filter(lambda x: len(x) > 0, promise))
        if u"运费险" in promise:
            promise_digital += "01"
        if u"新品" in promise:
            promise_digital += "02"
        if u"订单险" in promise:
            promise_digital += "03"
        if u"公益宝贝" in promise:
            promise_digital += "04"
        if u"放心淘" in promise:
            promise_digital += "05"
        if u"褪色赔" in promise:
            promise_digital += "06"
        if u"质无忧" in promise:
            promise_digital += "07"
        for promise_item in promise:
            if str(promise_item).endswith(u"天退货"):
                if promise_item == "15天退货":
                    promise_digital += "10"
                else:
                    promise_digital += "08"
            if str(promise_item).endswith(u"天无理由"):
                promise_digital += "09"
            if str(promise_item).endswith(u"天无理由退货"):
                promise_digital += "11"

        if u"品牌授权" in promise:
            promise_digital += "12"
        if u"品质保证险" in promise:
            promise_digital += "13"

        if u"品质承诺" in promise:
            promise_digital += "14"

        item_dict['promise'] = promise_digital
        # 支付手段
        payment_method_digital = ""
        pay_method = detail_dict['tradeContract']['pay']
        pay_method = [item['title'].strip() for item in pay_method]
        pay_method = list(filter(lambda x: len(x) > 0, pay_method))
        if u"快捷支付" in pay_method:
            payment_method_digital += "1"
        if u"信用卡支付" in pay_method:
            payment_method_digital += "2"
        if u"余额宝支付" in pay_method:
            payment_method_digital += "3"
        if u"蚂蚁花呗" in pay_method:
            payment_method_digital += "4"
        if u"集分宝" in pay_method:
            payment_method_digital += "5"
        item_dict['payment_method'] = payment_method_digital

        item_dict['transaction_volume'] = detail_dict['soldQuantity']['confirmGoodsCount']

        # 运费相关
        deliveryfee = detail_dict['deliveryFee']['data']
        sendCity = deliveryfee['sendCity']
        if 'list' in deliveryfee['serviceInfo']:
            fee = deliveryfee['serviceInfo']['list'][0]['info']
        elif 'sku' in deliveryfee['serviceInfo']:
            fee = deliveryfee['serviceInfo']['sku']['default'][0]['info']
        else:
            fee= -1
        if "免运费" in fee:
            fee = 0
        else:
            fee = re.sub("<span.*?</span>", "", fee)
            fee = re.findall("(\d+)\.", fee)[0]
        item_dict['place_of_delivery'] = sendCity
        item_dict['express_fee'] = fee
        return "ok"




    except Exception as ex:
        print(product_id, "detail_content_jiexi", "error:", ex)
        return False
