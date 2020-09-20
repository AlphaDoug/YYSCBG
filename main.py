import re
import CrawlYYSCBG_Roles.main
import xlwt

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
