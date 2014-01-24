# -*- coding: utf-8 -*-

from utils import Cache
from monulb import MonULB
from facebook import FacebookNotifier
from config import ULB_USER, ULB_PASSWORD, GMAIL_USER, GMAIL_PASSWORD, FB_GROUPID 

if __name__ == "__main__":
    with Cache('available_notes.json') as cache:
        diff = {}
        for course in MonULB(ULB_USER, ULB_PASSWORD).notes():
            if course.note is not None and course.mnemonic not in cache:
                diff[course.mnemonic] = course.name

        if len(diff) > 0:
            changed = [k+' - '+diff[k] for k in diff]
            message = "Les notes des cours suivants sont sorties: \n" 
            message += "\n".join(changed) + "\nhttps://mon-ulb.ulb.ac.be/"
            fb = FacebookNotifier(GMAIL_USER, GMAIL_PASSWORD)
            fb.post_to_group(FB_GROUPID, message)

        cache.update(diff)
