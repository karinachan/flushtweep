import tweepy
from flask import Flask
from flask import render_template
app = Flask(__name__)


#public_tweets= api.home_timeline()
#print api.me()


@app.route('/') # for the home page
def index():
#    return hello()

    return render_template('index.html', title="This is FlushTwitter")

@app.route('/<name>')
def hello(name=None, tweets=None):
    auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
    auth.set_access_token(config["access_token"], config["access_token_secret"])
    api= tweepy.API(auth)
    my_tweets=api.user_timeline(count=200)
    tweets= {};
    #for tweet in public_tweets:
    for tweet in my_tweets:
        if "RT" not in tweet.text:
            tweets[tweet.id ]= tweet.text



    return render_template('default.html', name=name, seq=tweets)

if __name__ == "__main__":
    app.debug = True
    config={}
    execfile("twitter.conf", config)
    app.run()
