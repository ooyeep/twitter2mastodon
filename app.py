from flask import Flask, request, jsonify, redirect, session, render_template
from flask_redis import FlaskRedis
import tweepy
import os
import re


# Twitter API信息
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
callback_url = os.environ.get('CALLBACK_URL')


app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY', os.urandom(16))

# 初始化Redis
app.config['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
redis_client = FlaskRedis(app)
redis_client.init_app(app)

# Twitter Oauth认证
def get_twitter_auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
    return auth

# 授权登录
@app.route('/login')
def login():
    auth = get_twitter_auth()
    auth_url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(auth_url)

# 回调函数，获取access token
@app.route('/callback')
def callback():
    request_token = session['request_token']
    del session['request_token']
    auth = get_twitter_auth()
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)
    session['access_token'] = auth.access_token
    session['access_token_secret'] = auth.access_token_secret
    return redirect('/')

# 注销登录
@app.route('/logout')
def logout():
    session.pop('access_token', None)
    session.pop('access_token_secret', None)
    return redirect('/')

# 主页
@app.route('/')
def index():
    if 'access_token' not in session:
        return render_template('index.html')
    else:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(session['access_token'], session['access_token_secret'])
        api = tweepy.API(auth)
        user = api.verify_credentials()

        return render_template('home.html', user=user)

@app.route('/submit', methods=['POST'])
def submit():
    if 'access_token' not in session:
        return redirect('/')
    else:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(session['access_token'], session['access_token_secret'])
        api = tweepy.API(auth)
        user = api.verify_credentials()

        twitter_username = user.screen_name
        mastodon_domain = request.form['mastodon_domain']
        mastodon_username = request.form['mastodon_username']

        # 检查提交的字段是否只包含字母和-_.三种符号
        if not re.match(r'^[a-zA-Z0-9\-_.]+$', mastodon_domain) or not re.match(r'^[a-zA-Z0-9\-_.]+$', mastodon_username):
            return '提交失败：域名和用户名只能包含字母、数字、-、_ 和 .'

        redis_client.set(twitter_username, f'{mastodon_domain},{mastodon_username}')

        return redirect('/')

# 公共API接口
@app.route('/api', methods=['GET'])
def api():
    username = request.args.get('username')
    if redis_client.exists(username):
        value = redis_client.get(username).decode('utf-8').split(',')
        return jsonify({'status': 'success', 'mastodon_domain': value[0], 'mastodon_username': value[1]})
    else:
        return jsonify({'status': 'User Not Found'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)
