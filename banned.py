#!/usr/bin/python
# =======================================
#
#  File Name : banned.py
#
#  Purpose :
#
#  Creation Date : 14-01-2015
#
#  Last Modified : Mon 09 Feb 2015 12:56:51 AM CST
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
            'charl(ie|ey)[\s-]*horse',
            'high[\s-]*horse',
            'dark[\s-]*horse']
annoying = ['[\s{0}]*{1}([\s{2}]+|$)'.format(reg_punc, i, reg_punc) for i in annoying]

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
hateful = ['[\s{0}]*{1}([\s{2}]+|$)'.format(reg_punc, i, reg_punc) for i in hateful]

dirty = ['penis',
         'cock',
         'hung',
         'riding[\s-]*like[\s-]*a[\s-]*horse',
         'hung[\s-]*horse',
         'dick',
         'fucking[\s-]*a[\s-]*horse',
         'sex',
         'gentlem[ea]n(\'?s)?[\s-]*club']
dirty = ['[\s{0}]*{1}([\s{2}]+|$)'.format(reg_punc, i, reg_punc) for i in dirty]
