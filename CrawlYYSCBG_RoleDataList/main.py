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
    refer = 'https://yys.cbg.163.com/cgi/mweb/equip/'
    refer = refer + str(params['serverid']) + '/' + str(params['ordersn'])
    headers = {
        'User-Agent': user_agent,
        'Refer': refer,
        'origin': 'https://yys.cbg.163.com',
        'cookie': 'mail_psc_fingerprint=7c3bc12ef1f65f007da2e589b4c95f8a; _ntes_nnid=7dc285612b827f353295ce81309cbf6f,1589114474748; _ntes_nuid=7dc285612b827f353295ce81309cbf6f; fingerprint=xzthondgyopwlwbw; _9755xjdesxxd_=32; YD00000722197596%3AWM_NI=%2FO2iEmPrc1DJJwq%2BWIkhHiSMws2ODCAOohPpSQxTxMqFtOUZqsoKP4jhUSHOKZZjBWKwnsrkBB3bYZE5rotp2yC1jBvmOEWjDDW2P6y0gFGGk8wy%2BmF1%2BwSSaLtXVmGaR2Q%3D; YD00000722197596%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed2f845a8adad99c47e97b88ba3c45b869f9abbae478fa7a88ee5638aaffbbbd42af0fea7c3b92aed91fe8ac86794aeadd2c7428aa9bfccd643a9b8888ad247b5adfeb0c7498391a189d37c918fb8b5fb47b39abcb0d852b3ada1acd340aab89bb4cb458986968bc15d89a9a294f161829efd83dc5287ebbe90f77cf2a78dd2e94ab6b381a6d662889c99d3d33ebbf0a9a7c64da9e8b99aaa6786efe598d259a394bcb9d56785bf9ed3d437e2a3; YD00000722197596%3AWM_TID=hoL0PbBfPnBEUBAVREM6dNzwmayc%2F4ZU; gdxidpyhxdE=ve3Q%2BQpt%5CnxXCwD7Ve6PhK%2B46c9qqCl24R7W5HAdJv7ASx3l8l6ewHuAGKL5OSv2WPnZJYDEJ17JQndsC6mmIJmYcXqwHKqQe%2BZqOpGdjq0gZw9aQOZiHZ%2BU8pek1HwvyeX5BnraC%2BuKMISsn%5CuiLg%5ChiEYZDbxjOp7Grb3V97Nto8rm%3A1600626703522; _external_mark=direct; is_log_active_stat=1; back_url=https%3A%2F%2Fyys.cbg.163.com%2Fcgi%2Fmweb%2Fequip%2F7%2F202006251601616-7-W5ZMVPOXCYSSN9; NTES_YD_SESS=kRdXuopzX7KoaqfZ3Pzf8pHxGajdx62PafypdgvGg1Z8RcNfRVhy3u6xu8ShG7qMn.VTnpR5QfHoPF3Om_3w5ojTXETfBMW9mXtkV9NtsCiKg92AbkCYDB1PLZRw37EeLRxQFzmPRBzGWzY82a_21AbNYk30rxtIj7gdpI9FEUgU8OcjattnMks3gui7v3edQ_4IVbwhNcxcCqvk5uU_xGlY1ks1x2NZw; NTES_YD_PASSPORT=usmMEDtkSZWef6RNMQ7dWNvyv0hPfOXo.uBKy1eRAY8rsHBnse9N0vfAvD39m2rRioeVi.shynCw9WwiQ2oAgKjIz8GiGpL883KpwpGkaewNoK35QBc6NQGzsiA9obmxf12__VCbaXnQcJSxMq6uleQCpeewyyswYLlAcbGwiaPoIGbJaMI3Eeer0MQ47r3SBoZRmNugToLTq6FPvZcGdHyqi; S_INFO=1600707940|0|3&80##|13469982083; P_INFO=13469982083|1600707940|1|cbg|00&99|null&null&null#shh&null#10#0|&0|null|13469982083; sid=etyT4Y8hEvsGFBpEI27i88kciMrj5YHdo4g9HKQX; urs_share_login_token=yd.3520384577244f56a@163.com$75070e2783b63031132119074918e2f7; login_id=ad288ca6-fc2c-11ea-894f-6066d946b4ca'
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
    return info, random.random() * 2 + 2


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
