import json
import requests
import random
import os


def getCbgData(server_id, order_sn):
    # 若订单的角色在文件中已经存在了则不进行爬取
    if os.path.isfile('Data/RoleDataList/' + order_sn + '.json'):
        print('数据在文件中已经存在')
        return {}, 0
    # 根据服务器ID和角色唯一ID获取指定的角色的藏宝阁数据
    with open('user-agent.json', 'r', encoding='utf-8') as file:
        cont = file.read()
        file.close()
        cont = json.loads(cont)
        cont = cont['browsers']
        browser = random.choice(list(cont.keys()))
        user_agent = random.choice(cont[browser])
        print('随机选择的user-agent为：', user_agent)
    params = {
        'serverid': server_id,
        'ordersn': order_sn,
        'view_loc': 'reco_home|tag_key:{"sort_key": "recommd", "tag": "auto-gen", "sort_order": ""}'
    }
    proxies = {
        "http": "http://163.125.17.242:8888",
    }
    refer = 'https://yys.cbg.163.com/cgi/mweb/equip/'
    refer = refer + str(params['serverid']) + '/' + str(params['ordersn'])
    headers = {
        'User-Agent': user_agent,
        'Refer': refer,
        'origin': 'https://yys.cbg.163.com',
    }

    r = requests.get(url='https://yys.cbg.163.com/cgi/api/get_equip_detail',
                     headers=headers, params=params)
    cont = r.json()
    equip_desc = cont['equip']['equip_desc']
    equip_desc = equip_desc.encode().decode('unicode_escape')
    try:
        equip_desc_json = json.loads(equip_desc)
    except json.decoder.JSONDecodeError:
        print('json转化失败')
        return {}, random.random() * 2 + 2
    cont['equip']['equip_desc'] = None
    info = {}
    info['other_info'] = cont
    info['equip_desc'] = equip_desc_json
    return info, random.random() * 2 + 4


def saveData(info):
    # 将藏宝阁数据保存
    if not info:
        print('数据为空')
        return
    print('将藏宝阁数据保存')
    key = info['other_info']['equip']['game_ordersn']
    with open('Data/RoleDataList/' + key + '.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(info, indent=2, ensure_ascii=False))
        file.close()
