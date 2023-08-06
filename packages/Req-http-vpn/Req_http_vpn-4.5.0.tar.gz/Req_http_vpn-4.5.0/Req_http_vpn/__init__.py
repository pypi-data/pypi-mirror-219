#  ____                       _      _    _
# |  _ \   ___   __ _        | |__  | |_ | |_  _ __         __   __ _ __   _ __  
# | |_) | / _ \ / _` |       | '_ \ | __|| __|| '_ \        \ \ / /| '_ \ | '_ \ 
# |  _ < |  __/| (_| |       | | | || |_ | |_ | |_) |        \ V / | |_) || | | |
# |_| \_\ \___| \__, | _____ |_| |_| \__| \__|| .__/  _____   \_/  | .__/ |_| |_|
#                  |_||_____|                 |_|    |_____|       |_|

"""
Req_http_vpn Library
~~~~~~~~~~~~~~~~~~~~~

Req_http_vpn Library is an HTTP library, written in Python, for human beings.
Basic GET usage:

>>>   from Req_http_vpn import *
>>>   from os import environ
>>>   environ['print_access_request_library_Req_http_vpn'] = '0'
>>>   this = Requests_filter('https://instagram.com')
>>>   this = this.filter_req_GET()
>>>   print(this.get('status_code'))
   
:Library used in the code: Requests
:Copyright: (c) 2023 Amin Rngbr.
:license: MIT
"""

import sys

sys.dont_write_bytecode = True

from .Req_class import Requests_filter, Req_Vpn_print, __version__

this : dict = {}