Req_Vpn_print = '0'

from typing import overload
from requests import post, head
import os, sys
from ColorTER import *

__version__ = ['4.0.0']

class Requests_filter:
    """
    ## Requests_filter Class
    The Req_http_vpn library is a simple library for sending **http** requests to websites that are **filtered and blocked** by governments.
    ### How to create an object from this class:
    ```python
    from Req_http_vpn import *
    Req = Requests_filter('https://google.com')
    ```
    And this class has **three functions** >>>
    ```python
    filter_req_GET() #To send http request with GET method
    filter_req_PorT() #To send http request with PorT method
    filter_req_HEAD() #To send an http request to get website headers
    ```
    `The author and developer of this light and simple library:` َ**Amin Rngbr**
    **and over (:**
    
    **GitHub address**: [aminrngbr1122](https://github.com/aminrngbr1122)
    """
    
    def __init__(self, Url: str):
        self.url = Url
        global Req_Vpn_print
        if 'print_access_request_library_Req_http_vpn' not in os.environ:
            os.environ['print_access_request_library_Req_http_vpn'] = Req_Vpn_print
        if os.environ['print_access_request_library_Req_http_vpn'] == '0':
            Print.printY(f'You are using Req_http_vpn library :')
            Print.printM(f'\t version: {__version__[0]} (:')
            Print.printB(f'You are sending a request to this IP: \"{self.url}\"')
        
    # =======================================================================================
    
    @overload
    def filter_req_GET(
        self,
        Content_type: str = 'text/html',
        Headers: str = '',
        Timeout: float = 500.5,
        *,
        Referer: str = 'https://google.com',
        UserAgent: str = 'Google Chrome',
        Stream: bool = False
    ) -> list or dict:
        ...
       
    @overload 
    def filter_req_send_file(
        self,
        files = {},
        Headers: str = '',
        Timeout: float = 500.5,
        Referer: str = 'https://google.com',
        UserAgent: str = 'Google Chrome',
    ) -> list or dict:
        ...
    
    @overload
    def filter_req_POST(
        self,
        Data: str = 'login=...&pass=...',
        Content_type: str = 'text/html',
        Headers: str = '',
        Timeout: float = 500.5,
        *,
        Referer: str = 'https://google.com',
        UserAgent: str = 'Google Chrome',
        Stream: bool = False
    ) -> list or dict:
        ...
    
    @overload
    def filter_req_HEAD(
        self,
        Data: str = 'login=...&pass=...',
        Content_type: str = 'text/html',
        Timeout: float = 500.5,
        Headers: str = '',
        *,
        Referer: str = 'https://google.com',
        UserAgent: str = 'Google Chrome',
    ) -> list or dict:
        ...

    # =======================================================================================
    
    def filter_req_GET(
        self,
        Content_type: str = 'text/html',
        Headers: str = '',
        Timeout: float = 500.5,
        Referer: str = 'https://google.com',
        UserAgent: str = 'Google Chrome',
        Stream: bool = False
    ) -> list or dict:
        try:
            datas = {
                'UrlBox': f'{self.url}',
                'ContentTypeBox': f'{Content_type}',
                'ContentDataBox': '',
                'HeadersBox': f'{Headers}',
                'RefererBox': f'{Referer}',
                'AgentList': f'{UserAgent}',
                'VersionsList': 'HTTP/1.1',
                'MethodList': 'GET',
            }
            data = post('https://www.httpdebugger.com/Tools/ViewHttpHeaders.aspx', data=datas, timeout=Timeout, stream=Stream)
            # assert data.status_code != 500, "Server error !"
            # return dict(
            #     headers= data.headers,
            #     content= data.content.decode('utf-8'),
            #     status_code= data.status_code
            # )
            self._h = data.headers
            self._c = data.content.decode('utf-8')
            self._s = data.status_code
        except Exception as e:
            return [e]
    
    def filter_req_POST(
        self,
        Data: str = 'login=...&pass=...',
        Content_type: str = 'text/html',
        Headers: str = '',
        Timeout: float = 500.5,
        Referer: str = 'https://google.com',
        UserAgent: str = 'Google Chrome',
        Stream: bool = False
    ) -> list or dict:
        try:
            datas = {
                'UrlBox': f'{self.url}',
                'ContentTypeBox': f'{Content_type}',
                'ContentDataBox': f'{Data}',
                'HeadersBox': f'{Headers}',
                'RefererBox': f'{Referer}',
                'AgentList': f'{UserAgent}',
                'VersionsList': 'HTTP/1.1',
                'MethodList': 'POST',
            }
            data = post('https://www.httpdebugger.com/Tools/ViewHttpHeaders.aspx', data=datas, timeout=Timeout, stream=Stream)
            # assert data.status_code != 500, "Server error !"
            # return dict(
            #     headers= data.headers,
            #     content= data.content.decode('utf-8'),
            #     status_code= data.status_code
            # )
            self._h = data.headers
            self._c = data.content.decode('utf-8')
            self._s = data.status_code
        except Exception as e:
            return [e]
        
    def filter_req_send_file(
        self,
        files = {},
        Headers: str = 'enctype: multipart/form-data',
        Timeout: float = 500.5,
        Referer: str = 'https://google.com',
        UserAgent: str = 'Google Chrome',
    ) -> list or dict:
        try:
            datas = {
                'UrlBox': f'{self.url}',
                'ContentTypeBox': f'application/json',
                'ContentDataBox': f'{str(files)}',
                'HeadersBox': f'{Headers}',
                'RefererBox': f'{Referer}',
                'AgentList': f'{UserAgent}',
                'VersionsList': 'HTTP/1.1',
                'MethodList': 'POST',
            }
            data = post('https://www.httpdebugger.com/Tools/ViewHttpHeaders.aspx', data=datas, timeout=Timeout)
            # assert data.status_code != 500, "Server error !"
            # return dict(
            #     headers= data.headers,
            #     content= data.content.decode('utf-8'),
            #     status_code= data.status_code
            # )
            self._h = data.headers
            self._c = data.content.decode('utf-8')
            self._s = data.status_code
        except Exception as e:
            return [e]
    
    def filter_req_HEAD(
        self,
        Data: str = 'login=...&pass=...',
        Content_type: str = 'text/html',
        Timeout: float = 500.5,
        Headers: str = '',
        Referer: str = 'https://google.com',
        UserAgent: str = 'Google Chrome',
    ) -> list or dict:
        try:
            datas = {
                'UrlBox': f'{self.url}',
                'ContentTypeBox': f'{Content_type}',
                'ContentDataBox': f'{Data}',
                'HeadersBox': f'{Headers}',
                'RefererBox': f'{Referer}',
                'AgentList': f'{UserAgent}',
                'VersionsList': 'HTTP/1.1',
                'MethodList': 'HEAD',
            }
            data = head('https://www.httpdebugger.com/Tools/ViewHttpHeaders.aspx', timeout=Timeout, data=datas)
            # assert data.status_code != 500, "Server error !"
            # return dict(
            #     headers= data.headers,
            #     content= data.content.decode('utf-8'),
            #     status_code= data.status_code
            # )
            self._h = data.headers
            self._c = data.content.decode('utf-8')
            self._s = data.status_code
        except Exception as e:
            return [e]
        
    @property
    def content(self) -> str:
        return self._c
        
    @property
    def headers(self) -> str:
        return self._h
    
    @property
    def status_code(self) -> str:
        return self._s
    
    @property
    def list_data(self) -> str:
        return [self._s, self._c, self._h]
    
    @property
    def object_data(self) -> str:
        yield self._s
        yield self._c
        yield self._h
    
    def dateTime() -> str:
        return 0.0
    
# =======================================================================================