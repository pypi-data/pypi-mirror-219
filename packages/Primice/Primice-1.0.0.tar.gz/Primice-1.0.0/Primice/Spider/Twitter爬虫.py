

import requests

url = "https://edith.xiaohongshu.com/api/sns/web/v1/homefeed"
headers = {}

cookies = {}
body= {}
response = requests.post(url,headers=headers,cookies=cookies)
data = response.json()
print(data)

