#!/usr/bin/python
# =======================================
#
#  File Name : banned.py
#
#  Purpose :
#
#  Creation Date : 14-01-2015
#
#  Last Modified : Mon 02 Mar 2015 02:44:18 PM CST
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
           'faggot']
hateful = ['([^\w]+|^){0}([^\w]+|$)'.format(i) for i in hateful]

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
         'cleavage',
         'choke',
         'drown',
         'dick(|s)',
         'virgin(|s|ity|ities)',
         'hentai',
         'ecchi',
         'fucking[\s-]*a[\s-]*horse',
         'sex(x)*(y)*',
         'bestiality',
         'gentlem[ea]n(\'?s)?[\s-]*club']
dirty = ['([^\w]+|^){0}([^\w]+|$)'.format(i) for i in dirty]
