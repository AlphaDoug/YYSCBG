import json
import requests


def getCbgData(server_id, order_sn):
    # 根据服务器ID和角色唯一ID获取指定的角色的藏宝阁数据
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'Refer': 'https://yys.cbg.163.com/cgi/mweb/equip/11/202008232001616-11-VTGMKTV8K4VDS?view_loc=all_list%7Ctag_key%3A%7B%22sort_key%22%3A%20%22recommd%22,%20%22tag%22%3A%20%22auto-gen%22,%20%22sort_order%22%3A%20%22%22%7D&tag=auto-gen'
    }
    params = {
        'serverid': server_id,
        'ordersn': order_sn,
        'view_loc': 'reco_home|tag_key:{"sort_key": "recommd", "tag": "auto-gen", "sort_order": ""}'
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
        return {}
    cont['equip']['equip_desc'] = None
    info = {}
    info['other_info'] = cont
    info['equip_desc'] = equip_desc_json
    return info


def saveData(info):
    # 将藏宝阁数据保存
    print('将藏宝阁数据保存')
    if not info:
        return
    key = info['other_info']['equip']['game_ordersn']
    with open('Data/RoleDataList/' + key + '.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(info, indent=2, ensure_ascii=False))
        file.close()
