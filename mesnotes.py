# -*- coding: utf-8 -*-

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
            ULB_PASSWORD = argv[2] if len(argv) >= 3 else raw_input("Password: ")
        print "Connexion..."
        try:
            
            for course in MonULB(ULB_USER, ULB_PASSWORD).notes():
                if course.note is not None:
                    print '\033[33m%s\033[0m: %s "%s" (%d ECTS)'%(
                        course.mnemonic, str(course.note), course.name, course.ects
                    )
                    total_notes += course.note*course.ects
                    total_ects += course.ects
                else:
                    print "\033[33m%s\033[0m: \033[35mPas encore de note\033[0m %s"%(
                        course.mnemonic, course.name
                    )
            if total_ects > 0:
                print "\033[1mMoyenne pondérée: %d\033[0m (basée uniquement sur les notes connues)"%(total_notes/total_ects)

        except MonULB.LoginError:
            print "\033[31mErreur de connexion\033[0m"
