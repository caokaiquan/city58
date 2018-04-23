from pyquery import PyQuery
import numpy as np
import pandas as pd


def parse(response):
    jpy = PyQuery(response.text)
    tr_list = PyQuery('#infolist > div.listwrap > table > tbody > tr').items()
    result = set()
    for i in tr_list:
        url = tr_list('td.info > ul < li.tli1 < a').attr('href')
        result.add(url)
    return result

def xiaoqu_parse(response):
    result = dict()
    jpy = PyQuery(response.text)
    result['name'] = jpy('body > div.bodyItem.bheader > div.fr.bhright > h1.xiaoquh1 > span').text()
    result['reference_price'] = jpy('body > div.bodyItem.bheader > div.fr.bhright > dl > dd:nth-child(1) > span.moneyColor').text()
    result['address'] = jpy('body > div.bodyItem.bheader > div.fr.bhright > dl > dd:nth-child(3) > span.ddinfo').text().replace('查看地图','')
    result['time'] = jpy('body > div.bodyItem.bheader > div > dl > dd:nth-child(5)').text().split()
    result['time'] = result['time'][2]
    return result

def get_ershou_price_list(response):
    jpy = PyQuery(response.text)
    price_list = [i[:-3] for i in jpy('#infolist > div.listwrap > table > tbody > tr > td.tc > span:nth-child(3)').text().split()]
    return price_list

def chuzu_list_pag_get_detail_url(response):
    jpy = PyQuery(response.text)
    a_list = jpy('#infolist > div.listwrap > table > tbody > tr:nth-child(1) > td.t < a ').items()
    url_list = [i.attr('href') for i in a_list]
    return url_list


def get_chuzu_house_info(response):
    jpy = PyQuery(response.text)
    result =dict()
    result['name'] = jpy('body > div.main-wrap > div.house-title > h1').text()
    result['zu_price'] = jpy('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > div > span.c_ff552e > b').text()
    result['type'] = jpy('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-child(2) > span:nth-child(2)').text()
    result['type'], result['mianji'], *_ = result['type'].split()
    return result
