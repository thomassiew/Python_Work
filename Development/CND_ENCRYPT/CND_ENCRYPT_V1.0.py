#! /usr/bin/env python
# coding=utf-8

import path
import os,sys,time
import csc.csclxmls
import getpass
from cryptography.fernet import Fernet

key = 'vXEXjeVp9WOAjFlRqXfJEMX3far-TuBmFquUvDoKgGw='
cipher_suite = Fernet(key)
# pid = str(os.getpid())
creddir = path.path('CREDS')
def main_console():
    while 1:
        os.system('cls')
        print "CND Credential Creation Version 1.0"
        print "1 : Credentials Creator"
        print "2 : Credentials Checker"
        print "3 : Exit"
        selection = raw_input("Please select :")
        if selection == "1":
            creds_cr8()
        elif selection == '2':
            creds_checker()
        elif selection == "3":
            sys.exit()
        else:
            print "Invalid Input"
            time.sleep(1)

def creds_cr8():
    a = 1
    print "You Chosen Credentials Creator"
    while a:
        print "Please key in your new credentials"
        username = raw_input("Username :")
        userpath = path.path('CREDS/' + username + '.xml')
        root = csc.csclxmls.node("<root/>")
        user = root + 'user'
        item1 = user + 'item'
        item1['key'] = "username"
        item2 = user + 'item'
        item2['key'] = "password"
        cipher_text_username = cipher_suite.encrypt(username)
        item1.text = cipher_text_username
        password = getpass.getpass('Password:')
        cipher_text_password = cipher_suite.encrypt(password)
        item2.text = cipher_text_password
        userpath.write_bytes(root.xml)
        print "credential: " + username + ".xml created"
        print "Would you like to create another one?"
        while True:
            answer = raw_input("Press 1 for yes | 2 to return to the main console | 3 to exit:")
            if answer == "1":
                break
            elif answer == "2":
                print "Returning to main console, Please hold"
                a = 0
                break
            elif answer == "3":
                sys.exit()
            else:
                print "Invalid Input"

def creds_checker():

    print "You Chosen Credentials Checker"
    d = 1

    while d:
        credddict = {}
        no = 1
        for a in os.listdir(creddir):
            splita = a.split('.')[0]
            credddict[str(no)] = str(splita)
            no += 1
        print "Please select your credentials"
        for a,b in credddict.items():
            print a , ": " , b
        selection = raw_input(">>>>")
        if selection in credddict:
            print credddict[selection]
            credslogin = csc.csclxmls.node(creddir + "/" + credddict[selection] + ".xml")
            decrypted_username = cipher_suite.decrypt(credslogin('//item[@key="username"]').text)
            decrypted_password = cipher_suite.decrypt(credslogin('//item[@key="password"]').text)
            print "username: ",decrypted_username
            print "password: ",decrypted_password
        else:
            print "Credentials don't exist or invalid input"


        while True:
            print "Would you like to continue??"
            answer = raw_input("Press 1 for yes | 2 to return to the main console | 3 to exit:")
            if answer == "1":
                os.system('cls')
                break
            elif answer == "2":
                print "Returning to main console, Please hold"
                d = 0
                break
            elif answer == "3":
                sys.exit()
            else:
                print "Invalid Input"

main_console()
#creds_checker()