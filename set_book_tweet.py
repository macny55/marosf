# -*- coding: utf-8 -*-

import logging
import tweepy
from setting import *
import data
import tweet_analyze

from google.appengine.ext import db
from google.appengine.api import urlfetch
import re

RE_HTTP = re.compile('(http?://[A-Za-z0-9\.\-\/]*)\s?',re.DOTALL)

# DB[Book_tweet]に登録
def insert_Book_tweet(usr_name , tweet_id , contents , memo , asin , date , tag):
    if tag == "":
        tag = "No-Tag"
    if contents == "":
        contents = "No-Text"
    if memo == "":
        memo = "No-Memo"
    q = db.GqlQuery("SELECT * FROM Book_tweet WHERE usr_id=:1 AND asin=:2" , usr_name , asin)
    #count_numは、１冊ごとのつぶやきの数
    count_num = q.count()
    data.Book_tweet.get_or_insert(key_name=str(tweet_id),usr_id=usr_name,tweet_id=tweet_id,contents=contents,memo=memo,asin=asin,date=date,tag=tag)
    return 0

# DB[Books]に登録
def insert_Books(usr_name , asin):
    data.Books.get_or_insert(key_name=asin+usr_name,asin=asin,usr_id=usr_name)

# DB[Book_img]に登録
def insert_Book_img(asin , book_img_url , book_title):
    data.Book_img.get_or_insert(key_name=asin,asin=asin,book_img_url=book_img_url,book_title=book_title)
    
# DB[Newest_tweet]に登録
def insert_Newest_tweet(usr_name , newest_id , statuses)
    data.Newest_tweet.get_or_insert(key_name=usr_name,usr_id=usr_name,newest_tweet_id=newest_id,statuses=statuses)

# データを取得し保存する
def set_usr_book_tweet(access_token):
    tmp ,api = token_api(access_token)
    time_line = api.user_timeline(count=5)
    #time_line[0]は最新のツイート
    usr_name = time_line[0].author.screen_name
    statuses = time_line[0].author.statuses_count
    id = time_line[0].id
    q = data.Newest_tweet.get_by_key_name(usr_name)
    progress = 0
    tweet_urls = []
    rpcs = []
    books_info = []
    #２回目以降のデータ取得
    if q:
        # 保存されているツイートの数と現在のツイートの数を比較し現在のツイートの数の方が多ければ保存処理を行う
        if statuses > q.statuses:
            add_statuses = statuses - q.statuses
            for tweets in tweepy.Cursor(api.user_timeline,since_id=q.newest_tweet_id).items(add_statuses):
                tweet_url = get_url(tweets.text)
                if tweet_url != -1:
                    tweet_info = {"tweet_url" : tweet_url , "created_at" : tweets.created_at , "id" : tweets.id , "tweet" : tweets.text}
                    tweet_urls.append(tweet_info)
                else:
                    return 0
            for t_u in tweet_urls:
                rpc = urlfetch.create_rpc(deadline = 10)
                rpc.callback = create_callback(rpc,usr_name,t_u["created_at"],t_u["id"],t_u["tweet"],id,statuses)
                urlfetch.make_fetch_call(rpc,t_u["tweet_url"])
                rpcs.append(rpc)
            for rpc in rpcs:
                rpc.wait()
    #初めてデータを取得するとき
    else:
        for u in tweepy.Cursor(api.user_timeline).items(statuses):
            tweet_url = get_url(u.text)
            if tweet_url != -1:
                tweet_info = {"tweet_url" : tweet_url , "created_at" : u.created_at , "id" : u.id , "tweet" : u.text}
                tweet_urls.append(tweet_info)
            else:
                return 0
        for t_u in tweet_urls:
            rpc = urlfetch.create_rpc()
            rpc.callback = create_callback(rpc,usr_name,t_u["created_at"],t_u["id"],t_u["tweet"],id,statuses)
            urlfetch.make_fetch_call(rpc,t_u["tweet_url"])
            rpcs.append(rpc)
        for rpc in rpcs:
            rpc.wait()

# HTTPリクエストを並列化し実行
def create_callback(rpc,usr_name,created_at,id,tweet,newest_id,statuses):
    return lambda: handle_result(rpc,usr_name,created_at,id,tweet,newest_id,statuses)
    
# データを取得してきて各DBに保存する
def handle_result(rpc,usr_name,created_at,id,tweet,newest_id,statuses):
    try:
        result = rpc.get_result()
        contents , memo , asin ,book_title ,book_img_url , tag = tweet_analyze.get_book_tweet(result.content,tweet)
        if asin != -1:
            insert_Books(usr_name , asin)
            insert_Book_img(asin , book_img_url , book_title)
            insert_Book_tweet(usr_name,id,contents,memo,asin,created_at,tag)
            insert_Newest_tweet(usr_name,newest_id,statuses)
    except urlfetch.DownloadError:
        logging.info("URL fetch Error")

def get_url(tweet):
    tweet_url = re.findall(RE_HTTP,tweet)
    if tweet_url:
        return tweet_url[0]
    else:
        return -1

def token_api(access_token):
    elems = access_token.split(u'&')
    token = dict([tuple(e.split(u'=')) for e in elems])
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(token[u'oauth_token'], token[u'oauth_token_secret'])
    api = tweepy.API(auth_handler=auth)
    return auth, api



