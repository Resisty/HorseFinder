#!/usr/bin/python
# =======================================
#
#  File Name : banned.py
#
#  Purpose :
#
#  Creation Date : 14-01-2015
#
#  Last Modified : Mon 23 Feb 2015 10:50:31 AM CST
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
            'horse[\s-]*radish',
            'bron(ie|y|ey)(|s)',
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
         'climax(|es)',
         'vagina',
         'hung',
         'rid(es|e|ing)',
         'rode(|s)',
         'ridden',
         'jack(|s)[\s-]*off',
         'hung',
         'dick(|s)',
         'virgin(|s|ity|ities)',
         'hentai',
         'ecchi',
         'fucking[\s-]*a[\s-]*horse',
         'sex(x)*(y)*',
         'bestiality',
         'gentlem[ea]n(\'?s)?[\s-]*club']
dirty = ['[^\w]+{0}([^\w]+|$)'.format(i) for i in dirty]
