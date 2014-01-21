# -*- coding: utf-8 -*-

import subprocess
import re
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse, urlunparse
from unidecode import unidecode

COOKIES = ".cookies"
HEADERS = ".headers"
CURL = ["curl", "-sk1", "-b", COOKIES, "-c", COOKIES, "-D", HEADERS]

class LoginError(Exception):
    pass

def headers():
    res = {}
    with open(HEADERS) as f:
        for line in f:
            if line[:5] == "HTTP/":
                res['STATUS'] = line.split(' ')[1]
            else:
                l = line.split(':')
                if len(l) > 1:
                    res[l[0].strip()] = (':'.join(l[1:])).strip()
    return res

def init():
    for f in [COOKIES, HEADERS]:
        subprocess.check_output(['rm', '-f', f])

def get(url, maxfollows=10):
    res = subprocess.check_output(CURL + [url])
    follows = 0
    while headers().get('STATUS') == '302' and follows < maxfollows:
        res = subprocess.check_output(CURL + [headers()['Location']])
        follows += 1
    return res

def post(url, data={}, maxfollows=10):
    query = "&".join("%s=%s"%(key, data[key]) for key in data)
    res = subprocess.check_output(CURL + ["-X", "POST", "-d", query, url])
    if headers().get('STATUS') == '302':
        res = get(headers()['Location'], maxfollows)
    return res

def login(netid, password):
    init()
    page = get("https://mon-ulb.ulb.ac.be/cp/home/displaylogin")

    match = re.search(r'document.cplogin.uuid.value="([^"]+)"', page)
    if not match:
        raise LoginError()
    
    page = post("https://mon-ulb.ulb.ac.be/cp/home/login", {
        'uuid': match.group(1),
        'user': netid,
        'pass': password
    })

    match = re.search(r'window.top.location=.*"([^"]+)"', page)
    if not match:
        raise LoginError()
    get("https://mon-ulb.ulb.ac.be"+match.group(1))

def get_notes(netid, password):
    login(netid, password)
    page = get("http://mon-ulb.ulb.ac.be/cp/ip/login?sys=sctssb&url=http%3A%2F%2Fbanssbfr.ulb.ac.be%2FPROD_frFR%2Fbzdispin.p_disprog")
    soup = BeautifulSoup(page)
    atBegin = False
    for line in soup('table')[-1]('tr'):
        cells = map(lambda x: unidecode(x.text), line('td'))
        if not atBegin:
            if cells[0] == 'NRE':
                atBegin = True
            continue
        if len(cells) == 6:
            (mnemonic, name, ects) = cells[1:4]
            notes = int(cells[-1]) if cells[-1] else None
            yield(mnemonic, name, int(ects), notes)

def print_stats(netid, password):
    total_notes, total_ects = 0, 0
    for mnemonic, name, ects, note in get_notes(netid, password):
        if note is not None:
            print '\033[33m%s\033[0m: %s "%s" (%d ECTS)'%(mnemonic, str(note), name, ects)
            total_notes += note*ects
            total_ects += ects
        else:
            print "\033[33m%s\033[0m: \033[35mPas encore de note\033[0m %s"%(mnemonic, name)
    if total_ects > 0:
        print "\033[1mMoyenne pondérée: %d\033[0m (basée uniquement sur les notes connues)"%(total_notes/total_ects)

if __name__ == "__main__":
    from sys import argv

    if len(argv) < 2:
        print "Usage: %s NETID [PASSWORD]"%(argv[0])
    else:
        password = argv[2] if len(argv) >=3 else raw_input("Password: ")
        print "Connexion en cours..."
        try:
            print_stats(argv[1], password)
        except LoginError:
            print "\033[31mErreur de connexion\033[0m"
