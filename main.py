#! /usr/bin/python
# -*- coding: utf-8 -*-

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import deferred
import webapp2 as webapp
import tweepy
from tweepy import OAuthHandler
import os, datetime
import logging
import urllib
import urllib2
import re
import json
import data
import tweet_analyze
import set_book_tweet
from setting import *
import cookie

def is_dev():
    return os.environ["SERVER_SOFTWARE"].find("Development") != -1

SESSION_EXPIRE = 200
CALLBACK_URL = 'http://localhost:8090/login_callback' if is_dev() else 'http://project-marosf.appspot.com/login_callback'
CALLBACK = 'http://localhost:8090' if is_dev() else 'http://project-marosf.appspot.com'

# AmazonAppStoreに置いてもらうための設定
class amazon_confirm(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'view/web-app-manifest.json')
        self.response.out.write(template.render(path,{}))

# Twitter API 関連-----------------------------------------------------------------------------------------------------
class RequestToken(db.Model):
    token_key    = db.StringProperty(required=True)
    token_secret = db.StringProperty(required=True)

class OAuthLogin(webapp.RequestHandler):
    def get(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)
        logging.info(auth)
        auth_url = auth.get_authorization_url()
        request_token = RequestToken(token_key=auth.request_token.key, token_secret=auth.request_token.secret)
        request_token.put()
        self.redirect(auth_url)

class OAuthLoginCallBack(webapp.RequestHandler):
    def get(self):
        request_token_key = self.request.get("oauth_token")
        request_verifier  = self.request.get('oauth_verifier')
        auth = tweepy.OAuthHandler(CONSUMER_KEY,  CONSUMER_SECRET)
        request_token = RequestToken.gql("WHERE token_key=:1",  request_token_key).get()

        if request_token is None:
            self.redirect('/')
        else:
            auth.set_request_token(request_token.token_key,  request_token.token_secret)
            access_token = auth.get_access_token(request_verifier)
            cookie.set_cookie(self, str(access_token), SESSION_EXPIRE)
            self.redirect('/')

class OAuthLogout(webapp.RequestHandler):
    def get(self):
        cookie.del_cookie(self)
        self.redirect('/')

def token_api(access_token):
    elems = access_token.split(u'&')
    token = dict([tuple(e.split(u'=')) for e in elems])
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(token[u'oauth_token'], token[u'oauth_token_secret'])
    api = tweepy.API(auth_handler=auth)
    return auth, api
# /Twitter API 関連----------------------------------------------------------------------------------------------------

# 関数-----------------------------------------------------------------------------------------------------------------
# ログインユーザのIDを取得
def get_usr_name(access_token):
    tmp ,api = token_api(access_token)
    if api:
        time_line = api.user_timeline(count=5)
    else:
        return -1
    if time_line:
        #time_line[0]は最新のツイート
        usr_name = time_line[0].author.screen_name
        return usr_name
    else:
        return 0

# ログインユーザのツイート数を取得
def get_statuses(access_token):
    tmp ,api = token_api(access_token)
    if api:
        time_line = api.user_timeline(count=5)
    else:
        return -98
    if time_line:
        #time_line[0]は最新のツイート
        usr_name = time_line[0].author.screen_name
        statuses = time_line[0].author.statuses_count
        q = data.Newest_tweet.get_by_key_name(usr_name)
        if q:
            return statuses - q.statuses
        else:
            return statuses
    else:
        return -99

# ユーザが保存している全てのタグ名を取得
def get_tags(usr_name):
    unique_tags = []
    tags = []
    q_tag = db.GqlQuery("SELECT * FROM Book_tweet WHERE usr_id=:1" ,usr_name)
    for unique_tag in q_tag:
        unique_tags.append(unique_tag.tag)
    for obj in unique_tags:
        if obj not in tags:
            tags.append(obj)
    return tags
# /関数----------------------------------------------------------------------------------------------------------------

# イベントハンドラ-----------------------------------------------------------------------------------------------------
# ログイン後のトップページ 未取得のツイートがあれば自動的に取得し保存する なければBookPageを表示する
class MainPage(webapp.RequestHandler):
    def get(self):
        token = cookie.load_cookie(self)
        if token != 'deleted' and token != '':
            usr_name = cookie.load_cookie_usr_name(self)
            if usr_name == None:
                usr_name = get_usr_name(token)
            progress = get_statuses(token)
            if usr_name == -1 or progress == -98:
                self.redirect('/logout')
            if progress == 0:
                redirect_url = '/books?usr_id=' + usr_name
                self.redirect(redirect_url)
            elif progress == -99:
                path = os.path.join(os.path.dirname(__file__), 'view/index.html')
                self.response.out.write(template.render(path, {
                    'url' : 'login',
                    'url_linktext' : 'Login',
                }))
            else:
                progress = progress * 50
                # バックグラウンドでデータを取得し保存する（画面ではプログレスバーを表示する）
                deferred.defer(set_book_tweet.set_usr_book_tweet,token)
                path = os.path.join(os.path.dirname(__file__), 'view/progress_bar.html')
                self.response.out.write(template.render(path, {
                            'CALLBACK' : CALLBACK,
                            'progress' : progress,
                            'url' : 'logout',
                            'url_linktext' : 'Logout',
                            'usr_id' : usr_name,
                            }))
        else:
            path = os.path.join(os.path.dirname(__file__), 'view/index.html')
            self.response.out.write(template.render(path, {
                        'url' : 'login',
                        'url_linktext' : 'Login',
                        }))

# 保存されている本の全ての表紙画像を取得し表示する
class BookPage(webapp.RequestHandler):
    def get(self):
        token = cookie.load_cookie(self)
        if token != 'deleted' and token != '':
            path = os.path.join(os.path.dirname(__file__), 'view/index.html')
            usr_name = self.request.get('usr_id')
            books_info = []
            tags = []
            tags = get_tags(usr_name)
            q = db.GqlQuery("SELECT * FROM Books WHERE usr_id = :1" , usr_name)
            books = q.get()
            if books:
                #リストのbook_urlsに本の画像URLを保存
                for book_img in q:
                    q_book_img = db.GqlQuery("SELECT * FROM Book_img WHERE __key__ = key('Book_img', :1)" , book_img.asin)
                    book_url = q_book_img[0].book_img_url
                    book_title = q_book_img[0].book_title
                    book_info = {"book_url" : book_url, "asin":book_img.asin , "book_title":book_title}
                    books_info.append(book_info)
            url = u'logout'
            url_linktext = 'Logout'
            self.response.out.write(template.render(path, {'url': url,
                                                           'url_linktext': url_linktext,
                                                           'login': url == u'logout',
                                                           'books_info' : books_info,
                                                           'tags' : tags,
                                                           'CALLBACK' : CALLBACK,
                                                           'usr_id' : usr_name,
                                                           }))
        else:
            path = os.path.join(os.path.dirname(__file__), 'view/top.html')
            self.response.out.write(template.render(path,{}))

# ログイン前のトップページ
class TopPage(webapp.RequestHandler):
    def get(self):
        token = cookie.load_cookie(self)
        if token != 'deleted' and token != '':
            usr_name = get_usr_name(token)
            if usr_name == 0:
                path = os.path.join(os.path.dirname(__file__), 'view/index.html')
                self.response.out.write(template.render(path, {
                    'url' : 'login',
                    'url_linktext' : 'Login',
                }))
            else:
                cookie.set_cookie_usr_name(self, str(usr_name), SESSION_EXPIRE)
                self.redirect('/confirm')
                
        else:
            path = os.path.join(os.path.dirname(__file__), 'view/top.html')
            self.response.out.write(template.render(path,{}))

# ログインするかしないかの確認画面を表示
class Confirm(webapp.RequestHandler):
    def get(self):
        usr_name = cookie.load_cookie_usr_name(self)
        path = os.path.join(os.path.dirname(__file__), 'view/confirm.html')
        self.response.out.write(template.render(path,{'usr_name' : usr_name,}))

# 本個別の詳細データの表示
class BookInformation(webapp.RequestHandler):
    def get(self):
        url = u'logout'
        url_linktext = 'Logout'
        path = os.path.join(os.path.dirname(__file__), 'view/book.html')
        contents = []
        tags = []
        qualify_flag = 1
        content_count = 0
        tweet_count = 0
        qualify_usr_name = cookie.load_cookie_usr_name(self)
        usr_name = self.request.get('usr_id')
        if usr_name != qualify_usr_name:
            qualify_flag = 0
        tags = get_tags(usr_name)
        http_tag = unicode(self.request.get('tag'))
        if http_tag:
            q_book_tweet = db.GqlQuery("SELECT * FROM Book_tweet WHERE tag = :1 AND usr_id=:2" ,http_tag, usr_name)
            if q_book_tweet:
                for tweet in q_book_tweet:
                    content = {"contents":tweet.contents , "memo":tweet.memo , "tag":http_tag , "tweet_id":tweet.tweet_id , "content_count":content_count}
                    contents.append(content)
                    content_count += 1
            self.response.out.write(template.render(path, {'url':url,
                                                           'url_linktext':url_linktext,
                                                           'contents':contents,
                                                           'login': url == u'logout',
                                                           'tags' : tags,
                                                           'CALLBACK' : CALLBACK,
                                                           'usr_id' : usr_name,
                                                           'qualify' : qualify_flag,
                                                           'ind_tag' : http_tag,
                                                           'content_count' : content_count
                                                           }))
        else:
            nyoronyoro = "〜"
            post_date_count = 0
            first_post_date = datetime.datetime.now()
            last_post_date = datetime.datetime.now()
            asin = str(self.request.get('asin'))
            q_book_img = db.GqlQuery("SELECT * FROM Book_img WHERE __key__ = key('Book_img' , :1)" , asin)
            q_book_tweet = db.GqlQuery("SELECT * FROM Book_tweet WHERE asin = :1 AND usr_id=:2" , asin , usr_name)
            if q_book_tweet:
                book_img = q_book_img[0].book_img_url
                book_title = q_book_img[0].book_title
                for tweet in q_book_tweet:
                    tweet_count += 1
                    if post_date_count == 0:
                        first_post_date = tweet.date
                    post_date_count += 1
                    content = {"contents":tweet.contents , "memo":tweet.memo , "tag":tweet.tag, "content_count":content_count , "tweet_id":tweet.tweet_id}
                    contents.append(content)
                    last_post_date = tweet.date
                    content_count += 1
                if tweet_count == 0:
                    q_delete_book = db.GqlQuery("SELECT * FROM Books WHERE __key__ = key('Books' , :1)" , asin + usr_name)
                    db.delete(q_delete_book)
                    self.redirect('/main')
                else:
                    first_post_date = first_post_date.strftime('%Y/%m/%d')
                    last_post_date = last_post_date.strftime('%Y/%m/%d')
            self.response.out.write(template.render(path, {'url':url,
                                                           'url_linktext':url_linktext,
                                                           'book_title':book_title,
                                                           'book_img':book_img,
                                                           'contents':contents,
                                                           'login': url == u'logout',
                                                           'asin':asin,
                                                           'tags' : tags,
                                                           'CALLBACK' : CALLBACK,
                                                           'usr_id' : usr_name,
                                                           'first_post_date' : first_post_date,
                                                           'last_post_date' : last_post_date,
                                                           'nyoronyoro' : nyoronyoro, 
                                                           'qualify' : qualify_flag,
                                                           'content_count' : content_count
                                                           }))
                                                           
# コンテンツデータの削除時
class DeleteContent(webapp.RequestHandler):
    def get(self):
        http_tag = unicode(self.request.get('tag'))
        usr_id = self.request.get('usr_id')
        asin = self.request.get('asin')
        tweet_id = self.request.get('param')
        delete_record = db.GqlQuery("SELECT * FROM Book_tweet WHERE __key__ = key('Book_tweet', :1)" , str(tweet_id))
        db.delete(delete_record)
        if http_tag:
            tag = urllib2.quote(http_tag.encode("utf-8"))
            self.redirect('/book?usr_id=' + usr_id + '&tag=' + tag)
        else:
            self.redirect('/book?usr_id=' + usr_id + '&asin=' + asin)

# ログインしているユーザの全データの削除
class DeleteAll(webapp.RequestHandler):
    def get(self):
        usr_name = self.request.get('usr_id')
        qualify_usr_name = cookie.load_cookie_usr_name(self)
        if usr_name == qualify_usr_name:
            o = db.GqlQuery("SELECT * FROM Book_tweet WHERE usr_id=:1" , usr_name)
            p = db.GqlQuery("SELECT * FROM Newest_tweet WHERE usr_id=:1" , usr_name)
            q = db.GqlQuery("SELECT * FROM Books WHERE usr_id=:1" , usr_name)
            db.delete(o)
            db.delete(p)
            db.delete(q)
            self.redirect('/main')
        else:
            path = os.path.join(os.path.dirname(__file__), 'view/top.html')
            self.response.out.write(template.render(path,{}))

# タグ、投稿した文章、メモの編集
class ContentUpdate(webapp.RequestHandler):
    def get(self):
        self.redirect('/')

    def post(self):
        http_tag = unicode(self.request.get('tag'))
        usr_id = self.request.get('usr_id')
        asin = self.request.get('asin')
        tweet_id = self.request.get('param')
        tag = unicode(self.request.get('post_tag'))
        contents = self.request.get('contents')
        memo = self.request.get('memo')
        if tag:
            update_tag = data.Book_tweet.get_by_key_name(tweet_id)
            update_tag.tag = tag
            update_tag.put()
            tag = urllib2.quote(tag.encode("utf-8"))
        elif contents:
            update_contents = data.Book_tweet.get_by_key_name(tweet_id)
            update_contents.contents = contents
            update_contents.put()
        elif memo:
            update_memo = data.Book_tweet.get_by_key_name(tweet_id)
            update_memo.memo = memo
            update_memo.put()
        if tag:
            self.redirect('/book?usr_id=' + usr_id + '&tag=' + tag)
        elif http_tag:
            self.redirect('/book?usr_id=' + usr_id + '&tag=' + http_tag)
        else:
            self.redirect('/book?usr_id=' + usr_id + '&asin=' + asin)
# /イベントハンドラ----------------------------------------------------------------------------------------------------

def main():
    app = webapp.WSGIApplication([
                        ('/',TopPage),
                        ('/confirm',Confirm),
                        ('/delete_content',DeleteContent),
                        ('/delete_all',DeleteAll),
                        ('/main', MainPage),
                        ('/books' , BookPage),
                        ('/login', OAuthLogin),
                        ('/login_callback', OAuthLoginCallBack),
                        ('/logout', OAuthLogout),
                        ('/book' , BookInformation),
                        ('/update' , ContentUpdate),
                        ('/amazon' , amazon_confirm)    
                        ],debug=True)

if __name__ == "__main__":
    main()

