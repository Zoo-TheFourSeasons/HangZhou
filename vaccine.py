import time

import requests


def login(app_id, token):
    session = requests.Session()
    session.headers = {
        'Host': 'dgwxs.jwx.com.cn',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://dgwxs.jwx.com.cn',
        'appId': app_id,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
        'Content-Type': 'application/json;charset=UTF-8',
        'token': token,
        'Referer': 'https://dgwxs.jwx.com.cn/mobile/?appId=%s' % app_id,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
        'Cookie': 'lg-token=%s' % token
    }

    try:
        rsp = session.post(
            'https://dgwxs.jwx.com.cn/mobile/outpatient/nearby',
            json={'pageNum': 1, 'numPerPage': 20, 'areaId': '441900', 'outpName': '', 'outpMapLongitude': '',
                  'outpMapLatitude': ''},
            verify=False
        )
    except Exception as e:
        print('连接失败', e)
        return

    response = rsp.json()
    if 'data' not in response:
        print('连接失败', response)

    if 'list' not in response['data']:
        print('连接失败', response)

    items = response['data']['list']

    address = ('大朗', '大岭', '南城', '东城', '莞城', '寮步', '茶山', '东坑', '高埗', '石碣')
    for item in items:
        if item['status'] != '1':
            break
        if item['outpName'][:2] not in address:
            continue
        print(item)


if __name__ == '__main__':
    count = 0
    while True:
        count += 1
        print(count)
        login('wx49202e41041d340e', '-t-zZUUyEUb4W5rODwoZoi3RQ-7_IsKxk3_c8B2GNoXwabFvtBOmpj_Ww')
        time.sleep(10)
