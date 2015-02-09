#!/usr/bin/python
# =======================================
#
#  File Name : banned.py
#
#  Purpose :
#
#  Creation Date : 14-01-2015
#
#  Last Modified : Mon 09 Feb 2015 12:16:00 AM CST
#
#  Created By : Brian Auron
#
# ========================================
from string import punctuation
import re

reg_punc = re.escape(punctuation)

annoying = ['my[\s-]*little[\s-]*pony',
            'ebay',
            'gekoo',
            'high[\s-]*horse',
            'dark[\s-]*horse']
annoying = ['[\s{0}]*{1}[\s{2}]+'.format(reg_punc, i, reg_punc) for i in annoying]

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
hateful = ['[\s{0}]*{1}[\s{2}]+'.format(reg_punc, i, reg_punc) for i in hateful]

dirty = ['penis',
         'cock',
         'hung[\s-]*like[\s-]*a[\s-]*horse',
         'hung[\s-]*like[\s-]*horse',
         'riding[\s-]*like[\s-]*a[\s-]*horse',
         'hung[\s-]*horse',
         '(horse(\s)*)*dick',
         'fucking[\s-]*a[\s-]*horse',
         'sex',
         'gentlem[ea]n(\'?s)?[\s-]*club']
dirty = ['[\s{0}]*{1}[\s{2}]+'.format(reg_punc, i, reg_punc) for i in dirty]
