#! /usr/bin/env python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import time
import path
import csv
import csc.csclxmls
import traceback

cfg = csc.csclxmls.node.cfgfile()
# if cfg('/root/item[@key="Pid check"]').text:
# 	if not cfg.pidfilecheck():
# 		print cfg('/root/item[@key="Exit Error"]').text
# 		sys.exit(1)
# try:
#     pth = path.path('xml.xml')
#    # create xml file with <root/> before initiate below
#     cc = csc.csclxmls.node('<root/>')
#     # t = cc + 'abc'
#     # h = t + 'item'
#     # h['key'] = "1"
#     # h.text = "abcd"
#     # print cc.xml
#     print cc('//item[@key="1"]').text
#     cc.write(pth)
# except:
# 	print traceback.format_exc()
# finally:
# 	if cfg('/root/item[@key="Pid check"]').text:
# 		if cfg.pidfilecheck():
# 			print cfg('/root/item[@key="Exit"]').text
# 			cfg.pidfile.unlink()
# 			sys.exit()