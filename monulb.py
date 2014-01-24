import re
from HTMLParser import HTMLParser

from utils import CURLSession

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
        self._note = None if value is None else int(value)

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

class MonULB(CURLSession):
    class LoginError(Exception):
        pass

    def __init__(self, netid, password):
        super(MonULB, self).__init__('-k1')
        self.login(netid, password)

    def __repr__(self):
        return "<MonULB %s>"%(self.netid)

    def login(self, netid, password):
        page = self.get('https://mon-ulb.ulb.ac.be/cp/home/displaylogin')
        match = re.search(r'document.cplogin.uuid.value="([^"]+)"', page.body)
        if not match:
            raise self.LoginError("Connection UUID not found")

        page = self.post("https://mon-ulb.ulb.ac.be/cp/home/login", {
            'uuid': match.group(1),
            'user': netid,
            'pass': password
        })

        match = re.search(r'window.top.location=.*"([^"]+)"', page.body)
        if not match:
            raise self.LoginError("Wrong username/password pair")
        self.netid = netid
    
    def notes(self):
        page = self.get('http://mon-ulb.ulb.ac.be/cp/ip/login?sys=sctssb&url=http%3A%2F%2Fbanssbfr.ulb.ac.be%2FPROD_frFR%2Fbzdispin.p_disprog')
        if page.ok:
            parser = NotesParser()
            parser.feed(page.body)
            return parser.courses

