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


def igggames(url):
  res = requests.get(url)
  soup = BeautifulSoup(res.text, "html.parser")
  soup = soup.find("div", class_="uk-margin-medium-top").findAll("a")

  bluelist = []
  for ele in soup:
    bluelist.append(ele.get('href'))
  bluelist = bluelist[6:-1]

  links = ""
  for ele in bluelist:
    if "bluemediafiles" in ele:
      links = links + bypassBluemediafiles(ele) + "\n"
    elif "pcgamestorrents.com" in ele:
      res = requests.get(ele)
      soup = BeautifulSoup(res.text, "html.parser")
      turl = soup.find(
        "p", class_="uk-card uk-card-body uk-card-default uk-card-hover").find(
          "a").get("href")
      links = links + bypassBluemediafiles(turl, True) + "\n"
    else:
      links = links + ele + "\n"

  return links[:-1]


###############################################################
# htpmovies cinevood sharespark atishmkv


def htpmovies(link):
  client = cloudscraper.create_scraper(allow_brotli=False)
  r = client.get(link, allow_redirects=True).text
  j = r.split('("')[-1]
  url = j.split('")')[0]
  param = url.split("/")[-1]
  DOMAIN = "https://go.theforyou.in"
  final_url = f"{DOMAIN}/{param}"
  resp = client.get(final_url)
  soup = BeautifulSoup(resp.content, "html.parser")
  try:
    inputs = soup.find(id="go-link").find_all(name="input")
  except:
    return "Incorrect Link"
  data = {input.get('name'): input.get('value') for input in inputs}
  h = {"x-requested-with": "XMLHttpRequest"}
  time.sleep(10)
  r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
  try:
    return r.json()['url']
  except:
    return "Something went Wrong !!"


def scrappers(link):

  try:
    link = rematch(
      r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*",
      link)[0]
  except TypeError:
    return 'Not a Valid Link.'
  links = []

  if "sharespark" in link:
    gd_txt = ""
    res = rget("?action=printpage;".join(link.split('?')))
    soup = BeautifulSoup(res.text, 'html.parser')
    for br in soup.findAll('br'):
      next_s = br.nextSibling
      if not (next_s and isinstance(next_s, NavigableString)):
        continue
      next2_s = next_s.nextSibling
      if next2_s and isinstance(next2_s, Tag) and next2_s.name == 'br':
        text = str(next_s).strip()
        if text:
          result = resub(r'(?m)^\(https://i.*', '', next_s)
          star = resub(r'(?m)^\*.*', ' ', result)
          extra = resub(r'(?m)^\(https://e.*', ' ', star)
          gd_txt += ', '.join(
            findall(r'(?m)^.*https://new1.gdtot.cfd/file/[0-9][^.]*',
                    next_s)) + "\n\n"
    return gd_txt

  elif "htpmovies" in link and "/exit.php" in link:
    return htpmovies(link)

  elif "htpmovies" in link:
    prsd = ""
    links = []
    res = rget(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    x = soup.select('a[href^="/exit.php?url="]')
    y = soup.select('h5')
    z = unquote(
      link.split('/')[-2]).split('-')[0] if link.endswith('/') else unquote(
        link.split('/')[-1]).split('-')[0]

    for a in x:
      links.append(a['href'])
      prsd = f"Total Links Found : {len(links)}\n\n"

    msdcnt = -1
    for b in y:
      if str(b.string).lower().startswith(z.lower()):
        msdcnt += 1
        url = f"https://htpmovies.lol" + links[msdcnt]
        prsd += f"{msdcnt+1}. <b>{b.string}</b>\n{htpmovies(url)}\n\n"
        asleep(5)
    return prsd

  elif "cinevood" in link:
    prsd = ""
    links = []
    res = rget(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    x = soup.select('a[href^="https://kolop.icu/file"]')
    for a in x:
      links.append(a['href'])
    for o in links:
      res = rget(o)
      soup = BeautifulSoup(res.content, "html.parser")
      title = soup.title.string
      reftxt = resub(r'Kolop \| ', '', title)
      prsd += f'{reftxt}\n{o}\n\n'
    return prsd

  elif "atishmkv" in link:
    prsd = ""
    links = []
    res = rget(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    x = soup.select('a[href^="https://gdflix.top/file"]')
    for a in x:
      links.append(a['href'])
    for o in links:
      prsd += o + '\n\n'
    return prsd

  elif "teluguflix" in link:
    gd_txt = ""
    r = rget(link)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.select('a[href*="gdtot"]')
    gd_txt = f"Total Links Found : {len(links)}\n\n"
    for no, link in enumerate(links, start=1):
      gdlk = link['href']
      t = rget(gdlk)
      soupt = BeautifulSoup(t.text, "html.parser")
      title = soupt.select('meta[property^="og:description"]')
      gd_txt += f"{no}. <code>{(title[0]['content']).replace('Download ' , '')}</code>\n{gdlk}\n\n"
      asleep(1.5)
    return gd_txt

  elif "taemovies" in link:
    gd_txt, no = "", 0
    r = rget(link)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.select('a[href*="shortingly"]')
    gd_txt = f"Total Links Found : {len(links)}\n\n"
    for a in links:
      glink = rocklinks(a["href"])
      t = rget(glink)
      soupt = BeautifulSoup(t.text, "html.parser")
      title = soupt.select('meta[property^="og:description"]')
      no += 1
      gd_txt += f"{no}. {(title[0]['content']).replace('Download ' , '')}\n{glink}\n\n"
    return gd_txt

  elif "toonworld4all" in link:
    gd_txt, no = "", 0
    r = rget(link)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.select('a[href*="redirect/main.php?"]')
    for a in links:
      down = rget(a['href'], stream=True, allow_redirects=False)
      link = down.headers["location"]
      glink = rocklinks(link)
      if glink and "gdtot" in glink:
        t = rget(glink)
        soupt = BeautifulSoup(t.text, "html.parser")
        title = soupt.select('meta[property^="og:description"]')
        no += 1
        gd_txt += f"{no}. {(title[0]['content']).replace('Download ' , '')}\n{glink}\n\n"
    return gd_txt

  elif "animeremux" in link:
    gd_txt, no = "", 0
    r = rget(link)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.select('a[href*="urlshortx.com"]')
    gd_txt = f"Total Links Found : {len(links)}\n\n"
    for a in links:
      link = a["href"]
      x = link.split("url=")[-1]
      t = rget(x)
      soupt = BeautifulSoup(t.text, "html.parser")
      title = soupt.title
      no += 1
      gd_txt += f"{no}. {title.text}\n{x}\n\n"
      asleep(1.5)
    return gd_txt

  else:
    res = rget(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    mystx = soup.select(r'a[href^="magnet:?xt=urn:btih:"]')
    for hy in mystx:
      links.append(hy['href'])
    return links


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


####################################################################################################
# ez4short


def ez4(url):
  client = cloudscraper.create_scraper(allow_brotli=False)
  DOMAIN = "https://ez4short.com"
  ref = "https://techmody.io/"
  h = {"referer": ref}
  resp = client.get(url, headers=h)
  soup = BeautifulSoup(resp.content, "html.parser")
  inputs = soup.find_all("input")
  data = {input.get('name'): input.get('value') for input in inputs}
  h = {"x-requested-with": "XMLHttpRequest"}
  time.sleep(8)
  r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
  try:
    return r.json()['url']
  except:
    return "Something went wrong :("


####################################################
# filercrypt


def getlinks(dlc, client):
  headers = {
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': 'application/json, text/javascript, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'http://dcrypt.it',
    'Connection': 'keep-alive',
    'Referer': 'http://dcrypt.it/',
  }

  data = {
    'content': dlc,
  }

  response = client.post('http://dcrypt.it/decrypt/paste',
                         headers=headers,
                         data=data).json()["success"]["links"]
  links = ""
  for link in response:
    links = links + link + "\n"
  return links[:-1]


def filecrypt(url):

  client = cloudscraper.create_scraper(allow_brotli=False)
  headers = {
    "authority":
    "filecrypt.co",
    "accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language":
    "en-US,en;q=0.9",
    "cache-control":
    "max-age=0",
    "content-type":
    "application/x-www-form-urlencoded",
    "dnt":
    "1",
    "origin":
    "https://filecrypt.co",
    "referer":
    url,
    "sec-ch-ua":
    '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    "sec-ch-ua-mobile":
    "?0",
    "sec-ch-ua-platform":
    "Windows",
    "sec-fetch-dest":
    "document",
    "sec-fetch-mode":
    "navigate",
    "sec-fetch-site":
    "same-origin",
    "sec-fetch-user":
    "?1",
    "upgrade-insecure-requests":
    "1",
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
  }

  resp = client.get(url, headers=headers)
  soup = BeautifulSoup(resp.content, "html.parser")

  buttons = soup.find_all("button")
  for ele in buttons:
    line = ele.get("onclick")
    if line != None and "DownloadDLC" in line:
      dlclink = "https://filecrypt.co/DLC/" + line.split(
        "DownloadDLC('")[1].split("'")[0] + ".html"
      break

  resp = client.get(dlclink, headers=headers)
  return getlinks(resp.text, client)


######################################################
# shareus


def shareus(url):
  token = url.split("=")[-1]
  bypassed_url = "https://us-central1-my-apps-server.cloudfunctions.net/r?shortid=" + token
  response = requests.get(bypassed_url).text
  return response


# api from https://github.com/bypass-vip/bypass.vip
def others(url):
  try:
    payload = {"url": url}
    url_bypass = requests.post("https://api.bypass.vip/", data=payload).json()
    bypassed = url_bypass["destination"]
    return bypassed
  except:
    return "Could not Bypass your URL :("


##################################################################################################################
# AppDrive or DriveApp etc. Look-Alike Link and as well as the Account Details (Required for Login Required Links only)


def unified(url):

  try:

    Email = "OPTIONAL"
    Password = "OPTIONAL"

    account = {"email": Email, "passwd": Password}
    client = cloudscraper.create_scraper(allow_brotli=False)
    client.headers.update({
      "user-agent":
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    })
    data = {"email": account["email"], "password": account["passwd"]}
    client.post(f"https://{urlparse(url).netloc}/login", data=data)
    res = client.get(url)
    key = re.findall('"key",\s+"(.*?)"', res.text)[0]
    ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")
    info = re.findall(">(.*?)<\/li>", res.text)
    info_parsed = {}
    for item in info:
      kv = [s.strip() for s in item.split(":", maxsplit=1)]
      info_parsed[kv[0].lower()] = kv[1]
    info_parsed = info_parsed
    info_parsed["error"] = False
    info_parsed["link_type"] = "login"
    headers = {
      "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
    }
    data = {"type": 1, "key": key, "action": "original"}
    if len(ddl_btn):
      info_parsed["link_type"] = "direct"
      data["action"] = "direct"
    while data["type"] <= 3:
      boundary = f'{"-"*6}_'
      data_string = ""
      for item in data:
        data_string += f"{boundary}\r\n"
        data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
      data_string += f"{boundary}--\r\n"
      gen_payload = data_string
      try:
        response = client.post(url, data=gen_payload, headers=headers).json()
        break
      except BaseException:
        data["type"] += 1
    if "url" in response:
      info_parsed["gdrive_link"] = response["url"]
    elif "error" in response and response["error"]:
      info_parsed["error"] = True
      info_parsed["error_message"] = response["message"]
    else:
      info_parsed["error"] = True
      info_parsed["error_message"] = "Something went wrong :("
    if info_parsed["error"]:
      return info_parsed
    if urlparse(url).netloc == "driveapp.in" and not info_parsed["error"]:
      res = client.get(info_parsed["gdrive_link"])
      drive_link = etree.HTML(
        res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
      info_parsed["gdrive_link"] = drive_link
    info_parsed["src_url"] = url
    if urlparse(url).netloc == "drivehub.in" and not info_parsed["error"]:
      res = client.get(info_parsed["gdrive_link"])
      drive_link = etree.HTML(
        res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
      info_parsed["gdrive_link"] = drive_link
    if urlparse(url).netloc == "gdflix.top" and not info_parsed["error"]:
      res = client.get(info_parsed["gdrive_link"])
      drive_link = etree.HTML(
        res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
      info_parsed["gdrive_link"] = drive_link

    if urlparse(url).netloc == "drivesharer.in" and not info_parsed["error"]:
      res = client.get(info_parsed["gdrive_link"])
      drive_link = etree.HTML(
        res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
      info_parsed["gdrive_link"] = drive_link
    if urlparse(url).netloc == "drivebit.in" and not info_parsed["error"]:
      res = client.get(info_parsed["gdrive_link"])
      drive_link = etree.HTML(
        res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
      info_parsed["gdrive_link"] = drive_link
    if urlparse(url).netloc == "drivelinks.in" and not info_parsed["error"]:
      res = client.get(info_parsed["gdrive_link"])
      drive_link = etree.HTML(
        res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
      info_parsed["gdrive_link"] = drive_link
    if urlparse(url).netloc == "driveace.in" and not info_parsed["error"]:
      res = client.get(info_parsed["gdrive_link"])
      drive_link = etree.HTML(
        res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
      info_parsed["gdrive_link"] = drive_link
    if urlparse(url).netloc == "drivepro.in" and not info_parsed["error"]:
      res = client.get(info_parsed["gdrive_link"])
      drive_link = etree.HTML(
        res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
      info_parsed["gdrive_link"] = drive_link
    if info_parsed["error"]:
      return "Faced an Unknown Error!"
    return info_parsed["gdrive_link"]
  except BaseException:
    return "Unable to Extract GDrive Link"


#####################################################################################################
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