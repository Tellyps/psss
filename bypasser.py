import re
from re import match as rematch, findall, sub as resub
import requests
from requests import get as rget
import base64
from urllib.parse import unquote, urlparse, parse_qs
import time
import cloudscraper
from bs4 import BeautifulSoup, NavigableString, Tag
from lxml import etree
import hashlib
import json
from dotenv import load_dotenv

load_dotenv()
from asyncio import sleep as asleep
import PyBypass
import os

##########################################################
# ENVs

GDTot_Crypt = os.environ.get(
  "CRYPT", "b0lDek5LSCt6ZjVRR2EwZnY4T1EvVndqeDRtbCtTWmMwcGNuKy8wYWpDaz0%3D")
Laravel_Session = os.environ.get("Laravel_Session", "")
XSRF_TOKEN = os.environ.get("XSRF_TOKEN", "")
DCRYPT = os.environ.get("DRIVEFIRE_CRYPT", "")
KCRYPT = os.environ.get(
  "KOLOP_CRYPT",
  "aWFicnVaNWh4TThRbzFqdkE2U2FKNmJOTWhvWkZmbWswaUFadTB5NXJ3RT0%3D")
HCRYPT = os.environ.get(
  "HUBDRIVE_CRYPT",
  "Q29hdlpLUEZTSEJLUjVZRkZQSExLODFuWGVudUlNK0ZPZlZmS1hENWxZVT0%3D")
KATCRYPT = os.environ.get("KATDRIVE_CRYPT", "")

############################################################
# Lists

ddllist = ["shareus.io"]


  
###################################################
# script links


def getfinal(domain, url, sess):

  #sess = requests.session()
  res = sess.get(url)
  soup = BeautifulSoup(res.text, "html.parser")
  soup = soup.find("form").findAll("input")
  datalist = []
  for ele in soup:
    datalist.append(ele.get("value"))

  data = {
    '_method': datalist[0],
    '_csrfToken': datalist[1],
    'ad_form_data': datalist[2],
    '_Token[fields]': datalist[3],
    '_Token[unlocked]': datalist[4],
  }

  sess.headers = {
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': domain,
    'Connection': 'keep-alive',
    'Referer': url,
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
  }

  # print("waiting 10 secs")
  time.sleep(10)  # important
  response = sess.post(domain + '/links/go', data=data).json()
  furl = response["url"]
  return furl


def getfirst(url):

  sess = requests.session()
  res = sess.get(url)

  soup = BeautifulSoup(res.text, "html.parser")
  soup = soup.find("form")
  action = soup.get("action")
  soup = soup.findAll("input")
  datalist = []
  for ele in soup:
    datalist.append(ele.get("value"))
  sess.headers = {
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Origin': action,
    'Connection': 'keep-alive',
    'Referer': action,
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
  }

  data = {'newwpsafelink': datalist[1], "g-recaptcha-response": RecaptchaV3()}
  response = sess.post(action, data=data)
  soup = BeautifulSoup(response.text, "html.parser")
  soup = soup.findAll("div", class_="wpsafe-bottom text-center")
  for ele in soup:
    rurl = ele.find("a").get("onclick")[13:-12]

  res = sess.get(rurl)
  furl = res.url
  # print(furl)
  return getfinal(f'https://{furl.split("/")[-2]}/', furl, sess)




######################################################
# shareus


def shareus(url):
  token = url.split("=")[-1]
  bypassed_url = "https://us-central1-my-apps-server.cloudfunctions.net/r?shortid=" + token
  response = requests.get(bypassed_url).text
  return response


# helpers


# check if present in list
def ispresent(inlist, url):
  for ele in inlist:
    if ele in url:
      return True
  return False


# shortners
def shortners(url):

  # igg games
  if "https://igg-games.com/" in url:
    print("entered igg:", url)
    return igggames(url)

  # shareus
  elif "https://shareus.io/" in url:
    print("entered shareus:", url)
    return shareus(url)

  # else
  else:
    temp = PyBypass.bypass(url)
    if temp != None: return temp
    else: return "😒 Not in Supported Links"


################################################################################################################################
