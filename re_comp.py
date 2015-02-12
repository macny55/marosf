# -*- coding: utf-8 -*-

import re

RE_HTTP = re.compile('(http?://[A-Za-z0-9\.\-\/]*)\s?',re.DOTALL)
RE_CONTENTS = re.compile('"content":"(.*?)"',re.DOTALL)
RE_MEMO = re.compile('"note":"(.*?)"',re.DOTALL)
RE_TAG_1 = re.compile('([#＃].*)[\s　]',re.DOTALL)
RE_TAG_2 = re.compile('([#＃].*)$',re.DOTALL)
RE_ASIN = re.compile('"asin":"(.*?)"',re.DOTALL)
