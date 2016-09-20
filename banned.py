#!/usr/bin/python
# =======================================
#
#  File Name : banned.py
#
#  Purpose :
#
#  Creation Date : 14-01-2015
#
#  Last Modified : Tue 20 Sep 2016 12:45:22 PM CDT
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
            'etsy',
            'horse[\s-]*radish',
            'bron(ie|y|ey)(|s)',
            'charl(ie|ey)[\s-]*horse',
            'high[\s-]*horse',
            'rooks[\s-]*store',
            'dark[\s-]*horse']
annoying = ['([^\w]+|^){0}([^\w]+|$)'.format(i) for i in annoying]

hateful = ['nigger',
           'nigga',
           'spic',
           'wet[\s-]*back',
           'gook',
           'kike',
           'sand[\s-]*nigger',
           'dyke',
           'rape',
           'trump',
           'faggot']
hateful = ['([^\w]+|^){0}([^\w]+|$)'.format(i) for i in hateful]

dirty = ['penis(|es)',
         'cock',
         'climax(|es)',
         'vagina',
         'hung',
         'rid(es|e|ing)',
         'rode(|s)',
         'ridden',
         'jack(|s)[\s-]*off',
         'hung',
         'cleavage',
         'choke',
         'drown',
         'dick(|s)',
         'virgin(|s|ity|ities)',
         'hentai',
         'ecchi',
         'fuck(|s|er|ers|ing)',
         'fucking[\s-]*a[\s-]*horse',
         'sex(x)*(y)*',
         'bestiality',
         'porn',
         'gentlem[ea]n(\'?s)?[\s-]*club']
