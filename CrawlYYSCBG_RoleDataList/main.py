import json
import os
import requests


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
    with open('../cont.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(_contJson, indent=2, ensure_ascii=False))
        file.close()
    with open('../equip_desc.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(_equip_descJson, indent=2, ensure_ascii=False))
        file.close()


def getFileData():
    file1 = open('../cont.json', encoding='utf-8')
    cont = file1.read()
    file2 = open('../equip_desc.json', encoding='utf-8')
    equip_desc = file2.read()
    file1.close()
    file2.close()
    js1 = json.loads(cont)
    js2 = json.loads(equip_desc)
    return js1, js2


def readData():
    if not os.path.isfile('../cont.json') or not os.path.isfile('../equip_desc.json'):
        os.path.join('../cont.json')
        os.path.join('../equip_desc.json')
        cont, equip = getCbgData()
        saveData(cont, equip)
    return getFileData()
