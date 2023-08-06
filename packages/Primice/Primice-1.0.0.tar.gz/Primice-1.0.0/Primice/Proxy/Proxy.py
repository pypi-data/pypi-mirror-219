# coding=utf-8
import time,re,requests,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
代理获取模块

使用方法：
    1.实例化MyProxy类，传入参数，实例化后的对象即为代理对象
        参数说明如下：
            -- options: 选项
                -- mode: 代理模式
                    如果为空，则根据api_url和json_url自动选择，text_url优先
                -- max_retry_count: 最大重试次数
                -- text_url: 代理text地址,返回值需要是 ip:port格式字符串
                -- json_url: 代理json地址
    2.使用代理对象的proxies属性获取代理字典，
    3.使用代理对象的switch_proxy方法切换代理
    4.使用代理对象的__str__方法或str(实例)获取代理字典
    5.切换代理方法修改接口信息，不修改对象的内存地址，无需重复获取代理字典   
"""


class MyProxy:
    def __init__(self, options={}) -> None:
        """
        初始化实例配置
        :param text_url: 代理text地址,返回值需要是 ip:port格式字符串
        :param json_url: 代理json地址
        :param mode: 代理模式
            如果为空，则根据api_url和json_url自动选择，text_url优先
        """
        self.__options = {
            'mode': None,
            'max_retry_count': 5,
            'text_url': None,
            'json_url': None,
        }
        self.__options.update(options)

        self.__max_retry_count = self.__options['max_retry_count']
        self.__text_url = self.__options['text_url']
        self.__json_url = self.__options['json_url']
        self.__mode = self.__options['mode']

        if self.__options["mode"] == None:
            self.__judje_mode()
        else:
            self.__mode = self.__options['mode']

        self.__text_url = ''

        self.__proxies = {}
        if not self.switch_proxy():
            raise Exception('代理模块初始化失败')
        
        print("代理模块初始化完成")

    @property
    def proxies(self) -> dict:
        return self.__proxies
    def __str__(self) -> str|dict:
        return self.__proxies
    

    def __judje_mode(self) -> None:
        if self.__text_url != None:
            print('传入了text_url参数,使用text模式')
            self.__mode = 'text'
        elif self.__json_url != None:
            print('传入了json_url参数,使用json模式')
            self.__mode = 'json'
        else:
            self.__mode = 'text'

    # TODO 切换代理
    def switch_proxy(self) -> None:
        """
        切换代理
        :return: 请求成功返回True，失败返回False
        """
        for retry_count in range(self.__max_retry_count):
            if self.__mode == 'text':
                try:
                    ip_port = requests.get(self.__text_url).text
                    ip_port = re.match(
                        r'(\d{1,3}\.){3}\d{1,3}:\d{1,5}', ip_port).group()
                    self.__proxies['http'] = ip_port
                    self.__proxies['https'] = ip_port
                    print('代理获取成功', ip_port)
                    return True
                except AttributeError as e:
                    print(e)
                    print('代理获取失败,正在重试')
                    time.sleep(5)
                    self.switch_proxy()
            # TODO json模式
            elif self.__mode == 'json':
                pass
        return False