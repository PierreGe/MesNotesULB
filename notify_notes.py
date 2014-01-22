# -*- coding: utf-8 -*-

import json
from config import TO_ADDR, ULB_USER, ULB_PASSWORD
from mesnotes import get_notes
from send_mail import mail

CACHEFILE = 'available_notes.json'

class Cache:
    def __init__(self, filename=CACHEFILE, initial={}):
        self.filename = filename
        self.initial = initial

    def __enter__(self):
        self.cache = self.initial
        try:
            self.cache = json.loads(open(self.filename).read())
        except:
            pass
        return self.cache

    def __exit__(self, exc_type, exc_value, backtrace):
        if exc_type is None:
            try:
                open(self.filename, 'w').write(json.dumps(self.cache))
            except:
                return False
            return True

if __name__ == "__main__":
    with Cache() as cache:
        diff = {}
        for mnemonic, name, ects, note in get_notes(ULB_USER, ULB_PASSWORD):
            if note is not None and mnemonic not in cache:
                diff[mnemonic] = name

        if len(diff) > 0:
            changed = [k+' - '+diff[k] for k in diff]
            message = "Les notes des cours suivants sont sorties: \n" 
            message += "\n".join(changed) + "\nhttps://mon-ulb.ulb.ac.be/"
            mail(TO_ADDR, "", message)

        cache.update(diff)
