#!/usr/bin/python
# =======================================
#
#  File Name : banned.py
#
#  Purpose :
#
#  Creation Date : 14-01-2015
#
#  Last Modified : Fri 13 Feb 2015 08:10:43 PM CST
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
annoying = ['[^\w]+{0}([^\w]+|$)'.format(i) for i in annoying]

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
hateful = ['[^\w]+{0}([^\w]+|$)'.format(i) for i in hateful]

dirty = ['penis',
         'cock',
         'hung',
         'riding[\s-]*like[\s-]*a[\s-]*horse',
         'hung',
         'dick',
         'virgin(|s|ity|ities)',
         'hentai',
         'ecchi',
         'fucking[\s-]*a[\s-]*horse',
         'sex(x)*(y)*',
         'bestiality',
         'gentlem[ea]n(\'?s)?[\s-]*club']
dirty = ['[^\w]+{0}([^\w]+|$)'.format(reg_punc, i, reg_punc) for i in dirty]
