import re, json

# TODO http原始请求

http_str = '''POST https://edith.xiaohongshu.com/api/sns/web/v1/homefeed HTTP/2
host: edith.xiaohongshu.com
content-length: 229
sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"
x-t: 1686633270292
dnt: 1
x-b3-traceid: 6aeb0cc59fdb31e0
sec-ch-ua-mobile: ?0
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43
content-type: application/json;charset=UTF-8
accept: application/json, text/plain, */*
x-s-common: 2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0P1PUhAHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHUN0D1+jHVHdWMH0ijP/W9GALM8eDIPemk4ebd2Bb34fFMJ9DIyBlV+gpT+0mSJ/+x2gLUy0qMPeZIPerh+0GlwsHVHdW9H0il+0W9+0PAP0qIP0DUNsQh+UHCHSY8pMRS2LkCGp4D4pLAndpQyfRk/SzbyLleadkYp9zMpDYV4Mk/a/8QJf4hanS7ypSGcd4/pMbk/9St+BbH/gz0zFMF8eQnyLSk49S0Pfl1GflyJB+1/dmjP0zk/9SQ2rSk49S0zFGMGDqEybkea/8QJpbEnpzpPpSx/gkOprLlnDzdPbSLafl+pBYV/MzaJrRrzfkyzbk3/fkzPDhU//b+pBVA/LzaypSLc/m8JLET/L4wJrEonfSw2DMC/fkBySkr/fl+pBqU/Sz++rErng4wpBlk/p4Q2SkT//b+prFAnnk+PFRgL/z+zBqI/FzbPFEo//pyprEknfMayrMgnfY8pr8Vnnk34MkrGAm8pFpC/p4QPLEo//++JLE3/L4zPFEozfY+2D8k/SzayDECafkyzF8x/Dzd+pSxJBT8pBYxnSznJrEryBMwzF8TnnkVybDUnfk+PS8i/nkyJpkLcfS+ySDUnpzyyLEo/fk+PDEk/Sz3+LRraflwPSpC/pzd2rEopfMwPDpEnfkb+bSgzfk8pMDI/L4Q2DErpgY+zbLU//QzPDRLp/zwzFLF/LzByDMCnfT+zM8Vnnkb2rMLzfkwzMLUnS4ByrECp/bOzrbE/LziJrExp/pypBzV/nMbPFMTzg482DbC/MzByFExngYyySQTnS4z+rETng4wzBqI/fk++LECGAbyzF8V/M4b+LELz/QyzFLU//Q+PrRr8Bl+Jp8TnnkBypSgLgk8prrM/M4b2DMg/fkOzr8x/M4yJpSLL/p+zrET/gkm+LEL8BMOzMrM/Dz32pkLag4+pbrl/Mzb4MDUa/+yJp8V/fMb2rR/a0DjNsQhwsHCHDDAwoQH8B4AyfRI8FS98g+Dpd4daLP3JFSb/BMsn0pSPM87nrldzSzQ2bPAGdb7zgQB8nph8emSy9E0cgk+zSS1qgzianYt8p+s/LzN4gzaa/+NqMS6qS4HLozoqfQnPbZEp98QyaRSp9P98pSl4oSzcgmca/P78nTTL0bz/sVManD9q9z1J7+xJMcM2gbFnobl4MSUcdb6agW3tF4ryaRApdz3agWIq7YM47HFqgzkanTU4FSkN7+3G9PAaL+P8DDA/9LI4gzVP0mrnd+P+nprLFkSyS87PrSk8nphpd4PtMmFJ7Ql4BYcJLTSy9Mg+rSht9SQyoQa2S878FTc4bSQPMbcJFlN8/8l4BYQ2sRA+S8FJFSk/nRQynYAJDH98p+DGA8U8d8AydpFa7Qy89pfG7HE898N8pS0Lo+Q2BRSLMmF2DSbJ9pf4gc7qflnyrE6/BEQ2epAP7bFLfE0+9pn8Dq3anT04FSkaocFPBQ+ag8iqgz/wB4QynSfqb87cLSeab8tJA+SL7mS8nTc4b8Q2e+SPBkHOaHVHdWEH0iE+AHh+eL7PeGVHdWlPsHCPAQR
x-s: XYW_eyJzaWduU3ZuIjoiNTEiLCJzaWduVHlwZSI6IngxIiwiYXBwSWQiOiJ4aHMtcGMtd2ViIiwic2lnblZlcnNpb24iOiIxIiwicGF5bG9hZCI6ImQyYTU1YjMzOTE1ZDg0YTJlMThlOTRlODFjZDZkNjQ2N2M1MTk3MDRiYTA0YmNmMGNlNGZiNzMzNjFjZDNlMTg2NTM4NDYwNTliMWIzZmM1MTM3YjM3OWQ4MDg0ODE3NGM5ZTNiZmRhMWZhYTFlYjkwZDc0YWEzMWI1NGM3MmNkMGQ3NGFhMzFiNTRjNzJjZGFjNDg5YjlkYThjZTVlNDhmNGFmYjlhY2ZjM2VhMjZmZTBiMjY2YTZiNGNjM2NiNTk5ODJlN2UzMTgxNGVmN2EyZjE4YWFjYWY0MGIzNDUxMDU2M2Q2OTU4NGE4MDFjMzZkMGVlYjExMTFjNGU2ZWFhNzU1ODAyMDhlNjU5ZTdlMmE3MmEwYzAzOTFkNjYxZjRmZWQ4NmYwNDg0NjM5Nzc1ZGFlOWE5NTE2ZGE2M2M0ODdlMmVmYjFiYWQzYTA5OWEzMWNjODFjOWZmYTQ5MDNmMzA5NTdmOGQ5NDkyZTIwMTQ1OTEwY2I3ZmVlNmExOSJ9
sec-ch-ua-platform: "Windows"
origin: https://www.xiaohongshu.com
sec-fetch-site: same-site
sec-fetch-mode: cors
sec-fetch-dest: empty
referer: https://www.xiaohongshu.com/
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
cookie: xhsTrackerId=103a8c81-ea5d-4cc6-b0b9-98609637d8e0; xhsTrackerId.sig=Kx1jTJUZW-xYWfH6kgIuzUtppaD260nKguNCgWai6tM; xsecappid=xhs-pc-web; a1=186c55d9000it1gxakvm5oi0hll5um60em3jyu2j750000186618; webId=51f2ad3237ce8c6e0a72d35263bda93d; web_session=030037a33ac4bd53bb1d85d671234a63b4a3ef; gid=yYKS22fj2JdiyYKS22fj867J8839ykC0Th62qVWl38x11V28276K8v888yYKKyY8KfYD4SJ0; gid.sign=4fWZt9FNf/o6MGxroTITTgPWhNA=; webBuild=2.9.6; websectiga=10f9a40ba454a07755a08f27ef8194c53637eba4551cf9751c009d9afb564467; sec_poison_id=28f8ead5-cc3e-49b9-9481-bbbe296d7f70

{"cursor_score":"","num":47,"refresh_type":1,"note_index":0,"unread_begin_note_id":"647853570000000027010ada","unread_end_note_id":"64686fcc0000000027000021","unread_note_count":31,"category":"homefeed_recommend","search_key":""}
'''

# TODO 生成requests代码

# 分割每一行参数
lines = http_str.split("\n")

# 获取请求方法和url
method_url = re.findall("(.*?) (.*?) HTTP/.*?", lines[0])[0]
# 取出method并转换为小写
request_method = method_url[0].lower()
# 取出url
request_url = method_url[1].split('?')[0]
body = {}
cookie_str = ''
def parse_params():
    params = {}
    for param in method_url[1].split('?')[1].split('&'):
        k, v = param.split('=')
        params[k] = v
    return params
def parse_headers():
    global cookie_str,body
    headers = {}
    if request_method == "get":
        for header in lines[1:]:
            if header.startswith("cookie"):
                print('haha')
                cookie_str = header.split(":",1)[1].strip()
                continue
            elif header.startswith('{"') and header.endswith('}') or header.startswith("{'") and header.endswith("}"):
                print(header)
                body = json.loads(header)
                continue
            elif header:
                key, value = header.split(":",1)
                headers[key] = value.strip()
    return headers
def parse_cookies(cookies_str):
    cookies = {}
    for cookie in cookies_str.split(";"):
        if cookie:
            key, value = cookie.split("=", 1)
            cookies[key] = value

    return cookies

if request_method == "get":
    params = parse_params()
headers = parse_headers()
cookies = parse_cookies(cookie_str)

spider_template_str = f'''

import requests

url = "{request_url}"
headers = {headers}
{f'params = {params}' if request_method == "get" else ''}
cookies = {cookies}
{f'body= {body}' if request_method=='post' else ''}
response = requests.{request_method}(url,headers=headers{',params=params' if request_method == 'get' else ''},cookies=cookies{',json=body' if body else ''})
data = response.json()
print(data)

'''

file_name = "Twitter爬虫.py"

with open(file_name, "w", encoding="utf-8") as f:
    f.write(spider_template_str)
