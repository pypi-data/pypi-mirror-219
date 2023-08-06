import shutil
from selectorlib import Extractor
import requests
import os
import io


def per20(st):
    t = st.split(" ")
    r_st = ""
    for r in t:
        r_st = r_st + "/" + r
    print(r_st)

    return r_st


def fit(t):
    i = 0
    while i < len(t):
        if (t[i]["link"].find("/tree/") + 1) and (t[i]["name"] is not None):
            t[i]['type'] = 'folder'
        elif t[i]["link"].find("/blob/") + 1:
            r1 = t[i]["link"].find("/blob/")
            s = t[i]["link"][0:r1] + t[i]["link"][r1 + 5:]
            t[i]["link"] = s
            t[i]['type'] = 'file'
        else:
            t[i]['type'] = 'move_up'
        i = i + 1


def rel(t, master):
    for r in t:
        if r['type'] == "folder":
            data = scrape("https://github.com" + r["link"])
            t = data["branches"]
            fit(t)
            rel(t, master)
            master.append(t)


def scrape(url):
    e = Extractor.from_yaml_string('''branches:
        css: 'div.Box-row:nth-of-type(n+2)'
        xpath: null
        multiple: true
        type: Link
        children:
            name:
                css: 'div.flex-auto.col-md-2 span.css-truncate'
                xpath: null
                type: Text
            link:
                css: a.js-navigation-open
                xpath: null
                type: Link
    ''')
    headers = {
        'authority': 'www.github.com/',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    # Download the page using requests
    print("Reading page: %s" % url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to flipkart data please contact" in r.text:
            print("Page %s was blocked by flipkart. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by flipkart as the status code was %d" % (url, r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)


def run(url):
    def diz(u):
        nex = u.find(urt) + len(urt)
        return u[nex:]

    # url = per20(per_url)
    print("hellonknjfb")
    # url = "https:/"+url
    urt = url
    while True:
        ur = urt.find("/") + 1
        if ur:
            urt = urt[ur:]
        else:
            break

    print(urt)

    data = scrape(url)
    t = data["branches"]
    fit(t)

    master = [t]
    rel(t, master)

    # try:
    #   os.mkdir(path)
    # except:
    #   print("hello control passed from except")
    # os.mkdir(os.path.join(path,urt))
    # urt1=path+"/"+urt
    urt1 = urt
    dir_name = urt
    os.mkdir(dir_name)
    for r in master:
        for r1 in r:
            if r1["type"] == "folder":
                os.mkdir(urt1 + diz(r1["link"]))

    for r in master:
        for r1 in r:
            if r1["type"] == "file":
                try:
                    print("downloading file: %s" % r1["name"])
                    myfile = requests.get("https://raw.githubusercontent.com" + r1["link"])
                    open(urt1 + diz(r1["link"]), 'wb').write(myfile.content)
                except:
                    print("there is some problem with that file")
                    continue

    shutil.make_archive(dir_name, 'zip', dir_name)

    return dir_name
