import requests
import json
import random
import time
import math
import os

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
proxies = {
    "https": "https://212.87.220.2:3128",
}
# 所有的角色简要信息列表
allRolesList = []


def GetAllUserData():
    if not os.path.isdir('Data') or not os.path.isdir('Data/RoleList'):
        # 当前不存在保存所有角色的文件夹
        print('当前不存在报错所有角色的文件夹,开始爬取数据')
        if not os.path.isdir('Data'):
            os.mkdir('Data')
        else:
            os.mkdir('Data/RoleList')
        while True:
            if GetOnePageData():
                time.sleep(random.random() + 0.5)
            else:
                break
        print('数据爬取结束')
    # 存在这个目录，直接读取文件中的信息
    files = os.listdir('Data/RoleList')
    for fileName in files:
        f = open('Data/RoleList/' + fileName, encoding='utf-8')
        fileContent = f.read()
        fileJson = json.loads(fileContent)
        res = fileJson['result']
        allRolesList.extend(res)
        f.close()
    return allRolesList


def GetOnePageData():
    # 获取一页数据
    global curPage, params, headers
    with open('user-agent.json', 'r', encoding='utf-8') as file:
        cont = file.read()
        file.close()
        cont = json.loads(cont)
        cont = cont['browsers']
        browser = random.choice(list(cont.keys()))
        user_agent = random.choice(cont[browser])
        print('随机选择的user-agent为：', user_agent)
    headers['User-Agent'] = user_agent
    params['page'] = curPage
    params['_'] = timeInt + curPage
    r = requests.get(url='https://recommd.yys.cbg.163.com/cgi-bin/recommend.py',
                     headers=headers, params=params, proxies=proxies)
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
    print(responseJson)
    if responseJson['paging']['is_last_page']:
        print('已经是最后一页了')
        return False
    curPage = curPage + 1
    print('爬取一页数据成功')
    return True
