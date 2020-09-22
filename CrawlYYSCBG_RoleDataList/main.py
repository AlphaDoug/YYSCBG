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
        "https": "https://212.87.220.2:3128",
    }
    refer = 'https://yys.cbg.163.com/cgi/mweb/equip/'
    refer = refer + str(params['serverid']) + '/' + str(params['ordersn'])
    headers = {
        'cookie':'_ntes_nnid=36db6fc834efbc176edcf5d503cb0f79,1578482710716; _ntes_nuid=36db6fc834efbc176edcf5d503cb0f79; UM_distinctid=1737f891a2f9b4-01aef21e2eab0b-6373664-1fa400-1737f891a30bbc; fingerprint=3ktiarciltqmedf0; is_log_active_stat=1; _external_mark=www.baidu.com; __snaker__captcha=xuhUFnt8w4PYDzYR; gdxidpyhxdE=s%2BR8CBa030aDB9WkPASBzOzk89YTa0zQjvPm8a%2B8d49ZZdkY0yWcTHgfc0GbOx0cRaB3WdqXo6qAz96pnw04PTo%2FxYYxaiDma35SDeLQDpl8J%5C7ajDb%5CsJ8bacM9alqogc48VBrH0QAxufaoj4uNmY7zxtzzu8KZrwT7Coy1sMqXZ2jR%3A1600760644025; _9755xjdesxxd_=32; YD00000722197596%3AWM_NI=X6LbMhV58OE%2FhV5FO5gG7ziaqY%2BcnS3pDr1WD9XY2c6ZfFQJKZQVF7A1Bfm09jwcJa980KP2JZq%2FwNBvpdbKb%2F95Dv5wRuChtd4lim5oKhdC%2F4SRJl%2Bb%2BXzTeES1MzioNjY%3D; YD00000722197596%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed7f47497bcfbccc579a9a88ab6c14a929a9fabf4438fb1a98fb240a5b59caff22af0fea7c3b92a9cea8483d06496ebf8b0c825ac8afba7ce3fa599f99bec6bb387e584ed59f1b08c93b45d88e798bab169f686aaa7d44289869fb7c53d83ef8e87f03cfbb6b984c96bfbe800acd33a8a86bfd0f64682aac085e141a2f1f7d6c77ef7a99e96c264b8bcfc8dec67f7b18589e749edec9db3c968e9bee5b9f960a79b9dd2d072abb1828bdc37e2a3; YD00000722197596%3AWM_TID=3GqEZDnwONREEFERFVNuJMpgzithkDIo; back_url=https%3A%2F%2Fyys.cbg.163.com%2Fcgi%2Fmweb%2Fequip%2F30%2F202008232201616-30-KZRQ6YPTNJ4MD%3Fview_loc%3Dequip_list%257Ctag_key%253A%257B%2522sort_key%2522%253A%2520%2522recommd%2522%2C%2520%2522tag%2522%253A%2520%2522auto-gen%2522%2C%2520%2522sort_order%2522%253A%2520%2522%2522%257D%26tag%3Dauto-gen; NTES_SESS=5QwbGe4Bb.uzE4TGVE_nIjSNZgVj5JcnOBXFB.Q7D0.0bX4tbOxW2SOQiwDAX8gjsp4mx50ho8d7i719bnN8WZoZKFB7AymAAYlyt0B3HctIQapDiz4ZH3Cc6dDTAdMr_DlI7Nq2zvjl5eMUAeQI2JBhimIC6l7hYwnnU_KTuVCXP6k7Nq1sbqWIJ4RhlJ_YQdd2K6CfBy7s7IryNcDAzah60CV.Wp28D; NTES_PASSPORT=T683sP_UTF6VIOtc7jZDaG9JcvKt3ZyQS705tD5FJ1OZO1zGOBYERDBqacj71dbiepR2BGZl3uX3kFgXXIYkKua2_zQjJQPE4v1DPxvbuwTK1GVvMW_s76_d.D80j9sJRpJ8Bzbh.my8GpAiLJadg_WBJSJmXh5Zxefdqrd5wrataFOx5FjSF0W6yBf6zWTeK; S_INFO=1600760227|0|3&80##|m13469982083; P_INFO=m13469982083@163.com|1600760227|1|cbg|00&99|shh&1599837440&ntesgod_app#shh&null#10#0#0|134083&1|godlike_app&ntesgod_app&cbg|13469982083@163.com; sid=Gzhlo_wo1zdlX56v8R2xFprpSgkYkH4HToCEm4kA; urs_share_login_token=m13469982083@163.com$4f599b5ca4970617393221d00a411901; login_id=6aa95fab-fca6-11ea-ad86-7e0fdeddccf1',
        'User-Agent': user_agent,
        'Refer': refer,
        'origin': 'https://yys.cbg.163.com',
    }

    r = requests.get(url='https://yys.cbg.163.com/cgi/api/get_equip_detail',
                     headers=headers, params=params, proxies=proxies)
    cont = r.json()
    equip_desc = cont['equip']['equip_desc']
    equip_desc = equip_desc.encode().decode('unicode_escape')
    try:
        equip_desc_json = json.loads(equip_desc)
    except json.decoder.JSONDecodeError:
        print('json转化失败,将失败的订单号写入文件,下次不再爬取')
        with open('ignore.txt', 'a', encoding='utf-8') as file:
            file.write(order_sn)
            file.write('\n')
            file.close()
        return {}, random.random() * 2 + 2
    cont['equip']['equip_desc'] = None
    info = {'other_info': cont, 'equip_desc': equip_desc_json}
    return info, random.random() * 5 + 5


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
