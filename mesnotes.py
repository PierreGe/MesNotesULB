# -*- coding: utf-8 -*-

import getpass

from monulb import MonULB
try:
    from config import ULB_USER, ULB_PASSWORD
except:
    ULB_USER = ''
    ULB_PASSWORD = ''

if __name__ == "__main__":
    from sys import argv

    if len(argv) < 2 and not ULB_USER:
        print "Usage: %s NETID [PASSWORD]"%(argv[0])
    else:
        if len(argv) >= 2:
            ULB_USER, ULB_PASSWORD = argv[1], ''
        total_notes, total_ects = 0, 0
        if not ULB_PASSWORD:
            ULB_PASSWORD = argv[2] if len(argv) >= 3 else getpass.getpass("Password:")
        print "Connexion..."
        try:
            
            for course in MonULB(ULB_USER, ULB_PASSWORD).notes():
                if course.note is not None:
                    color = 2 if course.note >= 12 else 1
                    print '\033[33m%s\033[0m: \033[3%dm%.2f\033[0m "%s" (%d ECTS)'%(
                        course.mnemonic, color, course.note, course.name, course.ects
                    )
                    total_notes += course.note*course.ects
                    total_ects += course.ects
                else:
                    print "\033[33m%s\033[0m: \033[35mPas encore de note\033[0m %s"%(
                        course.mnemonic, course.name
                    )
            if total_ects > 0:
                avg = total_notes/total_ects
                color = 2 if avg >= 12 else 1
                print "\033[1mMoyenne pondérée: \033[3%dm%.2f\033[0m (basée uniquement sur les notes connues)"%(color, avg)

        except MonULB.LoginError:
            print "\033[31mErreur de connexion\033[0m"
