# #! /usr/bin/env python
# # coding=utf-8
# # import SM9gentest2
import sys

# reload(sys)
# import shutil
# # sys.setdefaultencoding("utf-8")
# import csc.csclxmls
# import path
# import string
# import os, time,glob
#
# # cfg = csc.csclxmls.node.cfgfile()
#
# # if cfg('/root/item[@key="Pid check"]').text:
# #     if not cfg.pidfilecheck():
# #         print cfg('/root/item[@key="Exit Error"]').text
# #         sys.exit(1)
# # try:
#
# # code starts here --------------------------------------------------------------------------------
# # path-ing settings.xml
# # pth = path.path('settings.xml')
# # cc = csc.csclxmls.node(pth)
# # SM9gentest2.sm9_firefox_start()
# # # login
# # SM9gentest2.sm9_login()
# # # choose nav
# # SM9gentest2.sm9_navpanel(4)
# # SM9gentest2.sm9_opensearch(2)
# # a = SM9gentest2.sm9_buttons()
# # a.cancel()
# # pth = path.path('rulebase.xml')
# # cc = csc.csclxmls.node(pth)
# #
# # a = cc('//accept/item[@Assignee="SENTAN"]').text
# # print a
# # sys.exit()
# # print a
# # for x in cc('//accept/item').text:
# # #     print x['Assignee']
# # pth = path.path('Rule_Email.xml')
# # cc = csc.csclxmls.node(pth)
# # abc = cc('//item[@key="Body"]').text
# #
# # abc = string.replace(abc,"{" , "<")
# # abc = string.replace(abc,"}" , ">")
# #
# # print abc % "ashdahsdasd"
# # task = 'Disk E'
# # pth = path.path('Rule_Email.xml')
# # cc = csc.csclxmls.node(pth)
# # y = "C.SAP.MY.APAC.LA1"
# # k = cc('//item[@key="%s"]/..' %y)
# # kk = "Secure Hosting - Munich  MSL migration server (internal) - virtual farms missing in CAMP"
# # if k is not None:
# #     move_ag = True
# #     cond_task = k.conditions.item.text
# #     for x in cond_task:
# #         if x.lower() in kk.lower():
# #             print "WI: " + x + " exist, remain in queue"
# #             move_ag = False
# #             break
# #
# #
# # else:
# #     print 'nonetype'
#
# # fn= string.split(os.path.basename(sys.argv[0]),".")
# # filename = fn[0]
# # print filename
#
# # for x in k:
# #     print 111, cc('//item[@key = "task"]').text
# #     if y == x['key']:
# #         print k
#
# #     print traceback.format_exc()
# # finally:
# #     if cfg('/root/item[@key="Pid check"]').text:
# #         if cfg.pidfilecheck():
# #             print cfg('/root/item[@key="Exit"]').text
# #             cfg.pidfile.unlink()
# # #             sys.exit()
# # # oldest = ""
# # dir = r"C:\credss"
# #
# # while 1:
# #     newest = min(glob.iglob(dir + '/*.xml'), key=os.path.getmtime)
# #
# #     print os.path.basename(newest)
# #     os.utime(newest, (time.time(),time.time()))
# #     time.sleep(.4)
# #     a , b = os.path.basename(newest).split(".")
# #     print a
# # a = os.listdir(path.path('csc'))
# #
# # print len(a)
#
# # decorator---------------------------------------------
# def my_cache(some_function):
#     if not hasattr(some_function,"cache"):
#         some_function.cache = {}
#     def bili(*args,**kwds):
#         kwd=tuple([(x,y) for x,y in kwds.iteritems()])
#         print "------------ asd asd asd asd -----------------"
#         print args,kwds
#         value = some_function.cache.get((args, kwd), None)
#         if value is None:
#             some_function.cache[(args, kwd)]=value=some_function(*args,**kwds)
#         print "------------ asd asd asd asd -----------------"
#         return value
#     return bili
#
# def my_spy(some_function):
#
#     def bili(*args,**kwds):
#
#         print "------------ BEEP BEEP! BEEP BEEP! -----------------"
#         print time.asctime()
#         print 'calling function',some_function.__name__
#         print "parameter",args, kwds
#         arg0 = args[0]
#         arg1 = args[1]+5
#         result = some_function(arg0,arg1,arg1 ,arg1  )
#         result = result * result
#         print time.asctime()
#         print "result: " , result
#         print "------------ BEEP BEEP! BEEP BEEP! -----------------"
#         return result
#     return bili
#
# class tmdct():
#     def __init__(self,g=10):
#         self.g=g
#     def __call__(self, func):
#         def wrapper(*args,**kwds):
#             result=func(*args,**kwds)+self.g
#             return result
#         return wrapper
# dcrt=tmdct(15)
# #@my_cache
# #@my_spy
# @dcrt
# def j(a,b,c,d):
#     print "NI MEN HAO!!!!!!"
#     time.sleep(5)
#     value = a + b + c + d
#     return value
#
# #just_some_function = my_decorator(j)
#
# #just_some_function()
# print 'start'
# print j(1,2,3,4)
# print 'Cont.'
# print j(1,2,3,5)
# print 'Cont.'
# print j(1,2,3,4)
# print 'end'

# my_list = []
# list_2=[]
# crimefile = open(r"C:\CNLLOG\test.txt", 'r')
# crime2 = open(r"C:\CNLLOG\test2.txt", 'r')
# a = crimefile.read()
# b = crime2.read()
# my_list = a.split("\n")
#
# list_2 = b.split("\n")
#
# set1 = set(my_list)
# set2 = set(list_2)
# set3 = set1.union(set2)
# #print("Original List : ",my_list)
#
# my_new_list = list(set2-set1)
# my_new_list2 = list(set1-set2)
#
# #print set3
# print("List of unique numbers : ",my_new_list)
# print ("list of unique 2 : ", my_new_list2)

# import socket
# print socket.gethostbyname("www.google.com")

# from urlparse import urlparse
# #
# # print urlparse("https://www.google.com")
# import time
# tm = time.time()
# print 'thomas%s=' % (tm + 3) + ('%s' % (tm + 1))*10000

# from flask import Flask
# app = Flask(__name__)
#
# @app.route("/")
# def hello():
#     return "mushi mushi , ni hao , mama hen hao , baba yeh hen hao"
#
#
# # app.run(host="0.0.0.0", port=33)
# tick = [1,2,3]
# ttt = [3,3,3]
# abc = [1,4,5]
# print len(abc)
# import csv
# fl = open("illecsv.csv",'wb+')
# mycsv = csv.writer(fl)
# mycsv.writerow(["INM NO","BEFORE","AFTER"])
# for x in range(3):
#     tmp=[]
#     for y in [tick,ttt,abc]:
#         tmp.append(y[x])
#     mycsv.writerow(tmp)
# fl.close()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
# import time
# while 1:
#     driver = webdriver.Firefox()
#     driver.get("https://app.sli.do/event/fasyxtgb/ask")
#     time.sleep(5)
#
#     driver.find_element_by_class_name("score__btn score__btn--plus btn-plain")[0].click()
#     driver.quit()

import os

print os.getcwd()
import csc.csclxmls
import path

createpath = path.path("asd.xml")
cr8 = csc.csclxmls.node(createpath)
cr8inm = "asngfhfgh"
cr8('//item[@key="INCIDENTID"]').text = cr8inm
cr8('//item[@key="ticketcreated"]').text = "TRUE"
createpath.write_bytes(cr8.xml)
