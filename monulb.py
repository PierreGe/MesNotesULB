import re
from HTMLParser import HTMLParser

import requests

class Course(object):
    def __init__(self, name=None, mnemonic=None, ects=None, note=None):
        self.name, self.mnemonic = name, mnemonic
        self.ects, self.note = ects, note

    @property
    def ects(self):
        return self._ects
    @ects.setter
    def ects(self, value):
        self._ects = None if value is None else int(value)
    
    @property
    def note(self):
        return self._note
    @note.setter
    def note(self, value):
        if isinstance(value, str) or isinstance(value, unicode):
            value = value.replace(',', '.') #Replace european decimal mark
        self._note = None if value is None else float(value)

    def __str__(self):
        return ' '.join([str(self.mnemonic), str(self.ects), str(self.note), str(self.name)])
    
    def __repr__(self):
        return "<course %s>"%(self.mnemonic)

class NotesParser(HTMLParser):
    COLUMNS = {1: 'mnemonic', 2: 'name', 3: 'ects', 5: 'note'}

    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self.hasFoundHeaderLine = False
        self.inNotes = False
        self.courses = []

    def reinit_course(self):
        self.current_course = {
            'mnemonic': None,
            'name': None,
            'ects': None,
            'note': None
        }
        self.col_count = 0
        self.last_text = ''

    def handle_endtag(self, tag):
        if tag.lower() == 'tr':
            if self.hasFoundHeaderLine and not self.inNotes:
                self.inNotes = True
                self.reinit_course()
            elif self.inNotes:
                if self.current_course['mnemonic'] and self.current_course['name']:
                    self.courses.append(Course(**self.current_course))
                self.reinit_course()
        elif self.inNotes and tag.lower() == 'td':
            if self.col_count in self.COLUMNS and self.last_text:
                self.current_course[self.COLUMNS[self.col_count]] = self.last_text
            elif "Total ECTS de l'an" in self.last_text:
                self.inNotes = False
            self.last_text = ''
            self.col_count += 1

    def handle_data(self, text):
        t = text.strip()
        if t:
            if t == 'NRE':
                self.hasFoundHeaderLine = True
            elif self.inNotes:
                self.last_text = t

class MonULB():
    class LoginError(Exception):
        pass

    def __init__(self, netid, password):
        self._loginItems = {
            "user": netid,
            "pass": password,
            "uuid": None # identifiant dynamique 
        }
        self._headers = {
            "Host":"mon-ulb.ulb.ac.be",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) Gecko/20100101 Firefox/29.0",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"en-US,en;q=0.5",
            "Accept-Encoding":"gzip, deflate",
            "Connection":"keep-alive",
            "Referer":"http://mon-ulb.ulb.ac.be/cp/home/loginf"
        }
        self._session = requests.session()
        self._session.headers.update(self._headers)

    def login(self):
        page = self._session.get("https://mon-ulb.ulb.ac.be/cp/home/displaylogin")
        match = re.search(r'document.cplogin.uuid.value="([^"]+)"', page.text)
        if not match:
            raise self.LoginError("Connection UUID not found")
        self._loginItems["uuid"] = match.group(1)
        page = self._session.post("https://mon-ulb.ulb.ac.be/cp/home/login", data=self._loginItems)
        match = re.search(r'window.top.location=.*"([^"]+)"', page.text)
        if not match:
            raise self.LoginError("Wrong username/password pair")
    
    def notes(self):
        self.login()
        page = self._session.get("http://mon-ulb.ulb.ac.be/cp/ip/login?sys=sctssb&url=http%3A%2F%2Fbanssbfr.ulb.ac.be%2FPROD_frFR%2Fbzdispin.p_disprog")
        if page.status_code == 200:
            parser = NotesParser()
            parser.feed(page.text)
            return parser.courses

    def __repr__(self):
        return "<MonULB %s>"%(self.netid)
