# coding: UTF-8
 
import tweepy
import webbrowser
import sys 

CONSUMER_KEY  = "G4xybi16VBMP7Pscd5WiJw"
CONSUMER_SECRET = "EDRNKVOMXKSBXWX4jSZMGgVhdUMVMMtyQjxqNzMsKc"
ACCESS_KEY = "573195224-yGJreRsIWMcTZIWvHwD9OEnQhl08UcirVYfPVacN"
ACCESS_SECRET = "wvTFPIExnPB4iDrQTb6ARllXXaaxPvMyWdrEQiowA"


mypost = sys.stdin.readline().strip()
if 0==len(mypost):
    exit()
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
api.update_status(mypost)#OAuth認証で使うハンドルを宣言
auth=tweepy.OAuthHandler( consumer_token, consumer_secret)
#ユーザにアプリケーションを認証させるためのURL取得
pin_url=auth.get_authorization_url()

#webbrowser.openによって既定のブラウザでpin_urlを開く
webbrowser.open(pin_url)
#Twitterによって発行されたpinキーを入力させる
verifier=raw_input('PIN: ').strip()

#pinキーを使ってAccessTokenをTwitterに発行してもらう
auth.get_access_token(verifier)

#取得したAccessToken,AccessSecretをわかりやすいように格納しておく
access_token=auth.access_token.key
access_secret=auth.access_token.secret
#print access_token
#print access_secret

#ためしにユーザー名を取得
username=auth.get_username()
#ユーザー名を出力
print 'username:'+username
