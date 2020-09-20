import requests
import json
import os
import random
import time
import math
import re


def getCbgData():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'Refer': 'https://yys.cbg.163.com/cgi/mweb/equip/11/202008232001616-11-VTGMKTV8K4VDS?view_loc=all_list%7Ctag_key%3A%7B%22sort_key%22%3A%20%22recommd%22,%20%22tag%22%3A%20%22auto-gen%22,%20%22sort_order%22%3A%20%22%22%7D&tag=auto-gen'
    }
    params = {
        'serverid': 36,
        'ordersn': '202006260801616-36-GSQPY167J8IAD',
        'view_loc': 'reco_home|tag_key:{"sort_key": "recommd", "tag": "auto-gen", "sort_order": ""}'
    }
    r = requests.get(url='https://yys.cbg.163.com/cgi/api/get_equip_detail',
                     headers=headers, params=params)
    cont = r.json()
    equip_desc = cont['equip']['equip_desc']
    equip_desc = equip_desc.encode().decode('unicode_escape')
    equip_desc_json = json.loads(equip_desc)
    return cont, equip_desc_json


def saveData(_contJson, _equip_descJson):
    # 将藏宝阁数据保存
    print('将藏宝阁数据保存')
    with open('cont.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(_contJson, indent=2, ensure_ascii=False))
        file.close()
    with open('equip_desc.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(_equip_descJson, indent=2, ensure_ascii=False))
        file.close()


def getFileData():
    file1 = open('cont.json', encoding='utf-8')
    cont = file1.read()
    file2 = open('equip_desc.json', encoding='utf-8')
    equip_desc = file2.read()
    file1.close()
    file2.close()
    js1 = json.loads(cont)
    js2 = json.loads(equip_desc)
    return js1, js2


def readData():
    if not os.path.isfile('cont.json') or not os.path.isfile('equip_desc.json'):
        os.path.join('cont.json')
        os.path.join('equip_desc.json')
        cont, equip = getCbgData()
        saveData(cont, equip)
    return getFileData()


# 当前读取的数据页数
curPage = 1
# 每页角色数量
preCount = 15
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'P_INFO=m13469982083@163.com|1585972207|0|mail163|00&99|shh&1576087873&mail_client#shh&null#10#0#0|134083&1||13469982083@163.com; mail_psc_fingerprint=7c3bc12ef1f65f007da2e589b4c95f8a; _ntes_nnid=7dc285612b827f353295ce81309cbf6f,1589114474748; _ntes_nuid=7dc285612b827f353295ce81309cbf6f; fingerprint=xzthondgyopwlwbw; reco_sid=UaRcDcsqwwtpx1-BrYQjWM4e4I92zEZTw7dF_UGG',
    'Host': 'recommd.yys.cbg.163.com',
    'Referer': 'ttps://yys.cbg.163.com/cgi/mweb/pl/role?view_loc=equip_list',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same - site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
timeInt = int(math.floor(time.time() * 1000))
timeStr = str(timeInt)
callback = 'jQuery' + '3.3.1' + str(random.random()) + '_' + timeStr
callback = callback.replace('.', '')
params = {
    'callback': callback,
    'act': 'recommd_by_role',
    'search_type': 'role',
    'count': preCount,
    'view_loc': 'equip_list',
    'order_by': '',
    'page': curPage,
    '_': timeInt + curPage
}


def GetAllUserData():
    # 获取所有上架的角色数据
    while True:
        if GetOnePageData():
            time.sleep(random.random() + 0.5)
        else:
            break
    print('结束')


def GetOnePageData():
    # 获取一页数据
    global curPage, params
    params['page'] = curPage
    params['_'] = timeInt + curPage
    r = requests.get(url='https://recommd.yys.cbg.163.com/cgi-bin/recommend.py',
                     headers=headers, params=params)
    if r.status_code != 200:
        print('请求失败！！！！')
        return False
    responseStr = str(r.content)
    responseStr = responseStr.encode().decode('unicode_escape')
    # 无用字符去掉
    responseStr = responseStr.replace('b\'' + callback + '(', '')
    responseStr = responseStr[0:-2]
    responseJson = json.loads(responseStr)
    with open('Data/RoleList/Page_' + str(curPage) + '.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(responseJson, indent=2, ensure_ascii=False))
        file.close()
    if responseJson['paging']['is_last_page']:
        print('已经是最后一页了')
        return False
    curPage = curPage + 1
    print('爬取一页数据成功')
    return True


GetAllUserData()
