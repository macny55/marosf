# -*- coding: utf-8 -*-
import cgi

from google.appengine.ext import db

class Newest_tweet(db.Model):
  usr_id = db.StringProperty()
  newest_tweet_id = db.IntegerProperty()
  statuses = db.IntegerProperty()
  flag_1 = db.StringProperty()
  flag_2 = db.StringProperty()
  
class Book_tweet(db.Model):
  usr_id = db.StringProperty()
  tweet_id = db.IntegerProperty()
  contents = db.StringProperty(multiline=True)
  memo = db.StringProperty(multiline=True)
  asin = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  tag = db.StringProperty()
  
class Book_img(db.Model):
  asin = db.StringProperty()
  book_img_url = db.StringProperty()
  book_title = db.StringProperty(multiline=True)

class Books(db.Model):
  usr_id = db.StringProperty()
  asin = db.StringProperty()
  created_at = db.DateTimeProperty(auto_now_add=True)
  flag = db.IntegerProperty()

