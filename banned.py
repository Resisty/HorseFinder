#!/usr/bin/python
# =======================================
#
#  File Name : banned.py
#
#  Purpose :
#
#  Creation Date : 14-01-2015
#
#  Last Modified : Sun 08 Feb 2015 04:54:52 PM CST
#
#  Created By : Brian Auron
#
# ========================================

annoying = ['my[\s-]*little[\s-]*pony',
            'ebay',
            'gekoo',
            'high[\s-]*horse',
            'dark[\s-]*horse']
annoying = ['[\'"]*{0}[\'"]*'.format(i) for i in annoying]

hateful = ['nigger',
           'nigga',
           'spic',
           'wet[\s-]*back',
           'gook',
           'kike',
           'sand[\s-]*nigger',
           'dyke',
           'rape',
           'faggot']
hateful = ['[\'"]*{0}[\'"]*'.format(i) for i in hateful]

dirty = ['penis',
         'cock',
         'hung[\s-]*like[\s-]*a[\s-]*horse',
         'hung[\s-]*like[\s-]*horse',
         'riding[\s-]*like[\s-]*a[\s-]*horse',
         'hung[\s-]*horse',
         'dick',
         'fucking[\s-]*a[\s-]*horse',
         'sex',
         'gentlem[ea]n(\'?s)?[\s-]*club']
dirty = ['[\'"]*{0}[\'"]*'.format(i) for i in dirty]
