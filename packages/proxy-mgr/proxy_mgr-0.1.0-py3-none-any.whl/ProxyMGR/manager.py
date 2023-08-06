import random
import threading
import re
import requests

class Proxy(object):
    def __init__(self, proxy_string=None, default_type="http://"):
        """
        Proxy object

        :param proxy_string: Proxy
        :param default_type: Default network
        """

        if proxy_string:
            self.__parse_proxy_string(proxy_string, default_type)
        else:
            self.proxy_string = None

    def __str__(self) -> str:
        return self.proxy_string

    def __parse_proxy_string(self, proxy_string, default_type) -> None:
        """
        Proxy parsing

        :param proxy_string: Proxy
        :param default_type: Default network
        :return:
        """

        self.type = default_type
        if '://' in proxy_string:
            self.type = re.search(r"[A-Za-z0-9]+://", proxy_string).group(0)

        if "@" in proxy_string:
            proxy_string = proxy_string.strip('\n').strip(self.type).split('@')
            split_proxy = proxy_string[1].split(':')
            split_authenticated = proxy_string[0].split(':')

            self.ip = split_proxy[0]
            self.port = split_proxy[1]

            self.username = split_authenticated[0]
            self.password = split_authenticated[1]

            self.proxy_string_not_type = f'{self.username}:{self.password}@{self.ip}:{self.port}'
        else:
            split_string = proxy_string.strip('\n').strip(self.type).split(':')
            self.ip = split_string[0]
            self.port = split_string[1]
            self.proxy_string_not_type = f'{self.ip}:{self.port}'

            self.authenticated = len(split_string) == 4
            if self.authenticated:
                self.username = split_string[2]
                self.password = split_string[3]

                self.proxy_string_not_type = f'{self.username}:{self.password}@{self.proxy_string_not_type}'

        self.proxy_string = f'{self.type}{self.proxy_string_not_type}'

    def get_dict(self) -> dict:
        """
        Receiving dict proxy in the form of
        {
            'http': '',
            'https': ''
        }

        :return: dict
        """

        return {
            'http': self.proxy_string,
            'https': self.proxy_string
        } if self.proxy_string else {}

    def get_info(self) -> dict:
        """
        Getting proxy information from the site https://ipwho.is/

        :return: dict
        """
        try:
            with requests.get('https://ipwho.is/', proxies=self.get_dict()) as response:
                return response.json()
        except requests.exceptions.ProxyError:
            return None
        except requests.exceptions.ConnectionError:
            return None



class ProxyMGR(object):
    def __init__(self, proxy_file_path: str=None, proxy_list: list=None, default_type: str="http://"):
        """
        Proxy Manager

        :param proxy_file_path: Path proxy file
        :param proxy_list: List proxy
        :param default_type: Default network
        """

        if proxy_file_path:
            self.proxies: list = self.load_proxies_from_file(proxy_file_path, default_type) if proxy_file_path else [Proxy()]
        elif proxy_list:
            self.proxies: list = self.load_proxies_from_list(proxy_list, default_type) if proxy_list else [Proxy()]
        else:
            raise ValueError("Specify proxy_file_path or proxy_list")

        self.__lock = threading.Lock()
        self.__current_proxy: int = 0
        self.last_proxy: str = None
        self.default_type: str = default_type


    @staticmethod
    def load_proxies_from_file(proxy_file_path, default_type) -> list[Proxy]:
        proxies = []
        temp = []
        with open(proxy_file_path) as proxy_file:
            for proxy_string in proxy_file.readlines():
                if ":" in proxy_string and proxy_string not in temp:
                    proxies.append(Proxy(proxy_string, default_type))
                    temp.append(proxy_string)
        return proxies

    @staticmethod
    def load_proxies_from_list(proxy_list, default_type) -> list[Proxy]:
        proxies = []
        for proxy_string in proxy_list:
            if ":" in proxy_string:
                proxies.append(Proxy(proxy_string, default_type))
        return proxies

    def random_proxy(self) -> Proxy:
        return random.choice(self.proxies)

    def next_proxy(self, loop: bool=True) -> Proxy:
        if self.__current_proxy >= len(self.proxies):
            if loop:
                self.__current_proxy = 0
            else: return Proxy()

        with self.__lock:
            proxy = self.proxies[self.__current_proxy]
            self.__current_proxy += 1
            return proxy
