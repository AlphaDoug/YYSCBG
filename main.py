import re

import requests

import CrawlYYSCBG_Roles.main
import CrawlYYSCBG_RoleDataList.main
import xlwt
import time
import random


def SaveDataAsExcel():
    # 将读取藏宝阁中的数据，进行一定会处理后保存在表格中
    allRoles = CrawlYYSCBG_Roles.main.GetAllUserData()
    allRolesInfo = []
    for role in allRoles:
        oneRoleInfo = {}
        oneRoleInfo['level'] = role['equip_level']
        oneRoleInfo['area_name'] = role['area_name']
        oneRoleInfo['server_name'] = role['server_name']
        oneRoleInfo['price'] = role['price'] * 0.01
        oneRoleInfo['ssr_num'] = int(role['other_info']['basic_attrs'][0].split(' ')[1])
        oneRoleInfo['six_star_num'] = int(role['other_info']['basic_attrs'][1].split(' ')[1])
        oneRoleInfo['sign_in_day'] = re.sub('\D', '', role['other_info']['basic_attrs'][2])
        oneRoleInfo['collect_num'] = role['collect_num']
        oneRoleInfo['format_equip_name'] = role['format_equip_name']
        if role['platform_type'] == 1:
            oneRoleInfo['platform_type'] = 'IOS'
        else:
            oneRoleInfo['platform_type'] = '安卓'
        allRolesInfo.append(oneRoleInfo)
    wb = xlwt.Workbook()
    ws = wb.add_sheet('所有上架角色数据')
    row = 0
    ws.write(row, 0, '名字')
    ws.write(row, 1, '等级')
    ws.write(row, 2, '区域名称')
    ws.write(row, 3, '服务器')
    ws.write(row, 4, '平台')
    ws.write(row, 5, '价格')
    ws.write(row, 6, 'SSR数量')
    ws.write(row, 7, '六星数量')
    ws.write(row, 8, '签到天数')
    ws.write(row, 9, '收藏数量')
    row = row + 1

    for one_row in allRolesInfo:
        ws.write(row, 0, one_row['format_equip_name'])
        ws.write(row, 1, one_row['level'])
        ws.write(row, 2, one_row['area_name'])
        ws.write(row, 3, one_row['server_name'])
        ws.write(row, 4, one_row['platform_type'])
        ws.write(row, 5, one_row['price'])
        ws.write(row, 6, one_row['ssr_num'])
        ws.write(row, 7, one_row['six_star_num'])
        ws.write(row, 8, one_row['sign_in_day'])
        ws.write(row, 9, one_row['collect_num'])
        row = row + 1
    wb.save('Data/AllRoles.xls')


def SaveAllRolesData():
    # 根据订单号获取所有的角色的详细数据并保存
    allRoles = CrawlYYSCBG_Roles.main.GetAllUserData()
    all_order_sn = []
    for role in allRoles:
        one_data = {'order_sn': role['game_ordersn'], 'server_id': role['serverid']}
        all_order_sn.append(one_data)
    s_time = 0
    for data in all_order_sn:
        time.sleep(s_time)
        role_data, s_time = CrawlYYSCBG_RoleDataList.main.getCbgData(data['server_id'], data['order_sn'])
        CrawlYYSCBG_RoleDataList.main.saveData(role_data)


SaveAllRolesData()

proxypool_url = 'http://127.0.0.1:5555/random'
target_url = 'http://httpbin.org/get'

def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxypool_url).text.strip()

def crawl(url, proxy):
    """
    use proxy to crawl page
    :param url: page url
    :param proxy: proxy, such as 8.8.8.8:8888
    :return: html
    """
    proxies = {'http': 'http://' + proxy}
    return requests.get(url, proxies=proxies).text


def main():
    """
    main method, entry point
    :return: none
    """
    proxy = get_random_proxy()
    print('get random proxy', proxy)
    html = crawl(target_url, proxy)
    print(html)

if __name__ == '__main__':
    main()