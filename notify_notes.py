# -*- coding: utf-8 -*-

import json
from config import TO_ADDR, ULB_USER, ULB_PASSWORD
from mesnotes import get_notes
from send_mail import mail

CACHEFILE = 'available_notes.json'

cache = []
try:
	with open(CACHEFILE) as inFile:
		cache = json.loads(inFile.read())
except:
	pass

diff = []
for mnemonic, name, ects, note in get_notes(ULB_USER, ULB_PASSWORD):
	if note is not None and mnemonic not in cache:
		diff.append(mnemonic)

if len(diff) > 0:
	message = "Les notes des cours suivants sont sorties: \n" + "\n".join(diff) + "\nhttps://mon-ulb.ulb.ac.be/"
	mail(TO_ADDR, "", message)

cache += diff
with open(CACHEFILE, 'w') as outFile:
	outFile.write(json.dumps(list(cache)))

