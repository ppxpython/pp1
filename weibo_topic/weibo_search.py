import json

import requests
from lxml import etree

topic_url = 'https://s.weibo.com/weibo?q={}'


def get_search_page():

    r = requests.get('https://s.weibo.com/top/summary')
    print(r.text)
    tree_node = etree.HTML(r.text)
    content_node = tree_node.xpath('//table/tbody/tr')
    info = dict()
    for node in content_node[1:]:
        # print(node)
        info['title'] = node.xpath('*/a/text()')[0]
        info['hot'] = node.xpath('*/span/text()')[0]
        info['lable'] = node.xpath('*/i/text()')
        print(info)



def get_api_topic():
    # api_url = 'https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Dtopicband&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=filter_type%3Drealtimehot%26mi_cid%3D100103%26pos%3D0_0%26c_type%3D30%26display_time%3D1544958069&luicode=10000011&lfid=231583'
    # api_url = 'https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=filter_type%3Drealtimehot%26mi_cid%3D100103%26pos%3D0_0%26c_type%3D30%26display_time%3D1544958069&luicode=10000011&lfid=231583'
    api_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231648_-_1_-_all_-_%E8%AF%9D%E9%A2%98%E6%A6%9C_-_1&luicode=10000011&lfid=231583&page=1'
    r = requests.get(api_url)
    json_str = json.loads(r.text)
    content = json_str['data']['cards'][0]['card_group']
    topic = dict()
    for i in content:
        try:
            print('-----------------')
            topic['title'] = i['title_sub']
            topic['view'] = i['desc2']
            topic['desc'] = i['desc1']
            topic['pic'] = i['pic']
            print(topic)
        except KeyError:
            pass

# get_search_page()
get_api_topic()