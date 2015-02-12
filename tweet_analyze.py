# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import re
import urllib2
import data
import logging
import htmlentitydefs

RE_CONTENTS = re.compile('"content":"(.*?)"',re.DOTALL)
RE_MEMO = re.compile('"note":"(.*?)"',re.DOTALL)
RE_TAG_1 = re.compile('([#＃].*)[\s　]',re.DOTALL)
RE_TAG_2 = re.compile('([#＃].*)$',re.DOTALL)
#RE_ASIN = re.compile('"asin":"(.*?)"',re.DOTALL)
RE_ASIN = re.compile('"asin":"(.*?)"',re.DOTALL)

# 実体参照 & 文字参照を通常の文字に戻す
def htmlentity2unicode(text):
    # 正規表現のコンパイル
    reference_regex = re.compile(u'&(#x?[0-9a-f]+|[a-z]+);', re.IGNORECASE)
    num16_regex = re.compile(u'#x\d+', re.IGNORECASE)
    num10_regex = re.compile(u'#\d+', re.IGNORECASE)
    
    result = u''
    i = 0
    while True:
        # 実体参照 or 文字参照を見つける
        match = reference_regex.search(text, i)
        if match is None:
            result += text[i:]
            break
        
        result += text[i:match.start()]
        i = match.end()
        name = match.group(1)
        
        # 実体参照
        if name in htmlentitydefs.name2codepoint.keys():
            result += unichr(htmlentitydefs.name2codepoint[name])
        # 文字参照
        elif num16_regex.match(name):
            # 16進数
            result += unichr(int(u'0'+name[1:], 16))
        elif num10_regex.match(name):
            # 10進数
            result += unichr(int(name[1:]))

    return result

#URL解析にかかる時間 1URLにつき8秒

#html = urllib2.urlopen("https://kindle.amazon.co.jp/post/aB4F9vHyR22R7yhc6ArXsg")


def set_book_tweet(html,tweet):
    contents = ""
    memo = ""
    asin = ""
    book_title = ""
    img_url = ""
    tag = ""

    #soup = BeautifulSoup(urllib2.urlopen(html).read(),fromEncoding='utf-8')
    soup = BeautifulSoup(html,fromEncoding='utf-8')
    script = soup.findAll('script')
    asin_code = soup.find("span", {"class":"title"}).find("a").get("href")

#共有文  contents
    #RE_CONTENTS = re.compile('"content":"(.*?)"',re.DOTALL)
    for cont in re.findall(RE_CONTENTS,script[1].text):
        contents = htmlentity2unicode(cont)
#ツイート内容  memo
    #RE_MEMO = re.compile('"note":"(.*?)"',re.DOTALL)
    for mem in re.findall(RE_MEMO,script[1].text):
        memo = htmlentity2unicode(mem)

    if contents == "" and memo == "":
        contents = tweet
        
#タグ tag
    #RE_TAG_1 = re.compile('([#＃].*)[\s　]',re.DOTALL)
    #RE_TAG_2 = re.compile('([#＃].*)$',re.DOTALL)
    tag_flag_1 = re.findall(RE_TAG_1,memo)
    tag_flag_2 = re.findall(RE_TAG_2,memo)
    if not tag_flag_1 == []:
        for ta in tag_flag_1:
            tag = ta
            memo = re.sub(tag,"",memo)
            memo = re.sub('^¥s',"",memo)
            memo = re.sub('^　',"",memo)
            tag = re.sub('[#＃\s　]*',"",tag)
    elif not tag_flag_2 == []:
        for ta in tag_flag_2:
            tag = ta
            memo = re.sub(tag,"",memo)
            memo = re.sub('^¥s',"",memo)
            memo = re.sub('^　',"",memo)
            tag = re.sub('[#＃\s　]*',"",tag)


#ASINコード  asin
    #RE_ASIN = re.compile('"asin":"(.*?)"',re.DOTALL)
#    for asi in re.findall(RE_ASIN,script[1].text):
#        asin = asi
    asin_codes = re.split( r'/', asin_code )
    for i in asin_codes:
        asin = i

#商品ページ　http://www.amazon.co.jp/dp/ ASIN /ref=r_soa_po_i

#画像URL  img_url
    img = soup.find(attrs={'class':'bookCover'})
    img_url = img['src']
    img_url = re.sub(r',.*?\.','.',img_url)
    
#本のタイトル  title
    book_title = htmlentity2unicode(soup.find('span' , {'class':'title'}).text)

    if asin:
        return contents , memo , asin , book_title , img_url , tag
    else:
        return -1 , -1 , -1 , -1 , -1 , -1


