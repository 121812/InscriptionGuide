import requests
import sys
import os
import time

# 查询tick名称
tick = 'opbn'

url = "https://api.opbrc.com/addr/holdTicks"
headers = {
  'Content-Type': 'application/json'
}
database_enalbe = False
text_enalbe = False

# 数据库方式获取地址
def database():
    global address_all, database_enalbe
    import pymysql
    database_enalbe = True
    # 配置mysql数据库连接方式
    db = pymysql.connect(
            host='',
            user='',
            password='',
            database=''
    )
    # 配置查询语句
    query_sql = ''
    cursor = db.cursor()
    cursor.execute(query_sql)
    address_all = cursor.fetchall()

# 文件方式获取地址
def text():
    global address_all, text_enalbe
    text_enalbe = True
    script_path  = sys.argv[0]
    script_directory = os.path.dirname(os.path.abspath(script_path))  
    file_path = '%s\\acc.txt'%script_directory
    with open(file_path) as f:
        address_all = [line.rstrip('\n') for line in f.readlines()]

# 数据库查询方式
# database()

# 文本文件方式
text()


print(address_all)
total_balance = 0
n = 0
for address in address_all:
    # 项目方速率限制
    time.sleep(0.4)

    # 不同数据类型，不同解构
    if database_enalbe == True:
        address = address[0]
    elif text_enalbe == True:
        pass
    payload = "{\r\n    \"addr\": \"%s\"\r\n}"%address
    response = requests.request("POST", url, headers=headers, data = payload)
    try:
        records = response.json().get('data').get('records')
        for token in records:
            if token.get('tick') == '%s'%tick:
                balance = token.get('balance')
        print(balance)
    except:
        print(f'address:{address}', response.json())
        continue
    total_balance += balance
    n += 1
    print(f'address:{address} balance:{balance}')
    

print(f'可查账户为：{n}, 总余额为：{total_balance}')
