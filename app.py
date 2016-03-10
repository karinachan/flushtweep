import tweepy
from flask import Flask
from flask import render_template
import logging
import os,sys



app = Flask(__name__)


@app.route('/') # for the home page
def index():
    return render_template('index.html', title="This is FlushTwitter")

@app.route('/<name>')
def hello(name):
    tweets= {};
    try:
        my_tweets=api.user_timeline(id=name, count=100)
 
 
    
  
  
        for tweet in my_tweets:
            if "RT" not in tweet.text:
                tweets[tweet.id ]= tweet.text
        
    except tweepy.TweepError, e:
        message = "error: "+str(e)
        logging.basicConfig(filename='myapp.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        logging.debug("*******************************\n")
    return render_template('default.html', name=name, seq=tweets)
    
    

@app.route('/map/<hashtag>')
def map(hashtag=None):
    tweets = api.search(q="warriors", rpp="400")
    for t in tweets:
        if (t.place!=None):
            print str(t.place.bounding_box.coordinates) +"\n"

    return render_template('map.html', name=hashtag)




if __name__ == "__main__":
    app.debug = True
    config={}
    execfile("twitter.conf", config)
    auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
    auth.set_access_token(config["access_token"], config["access_token_secret"])
    api= tweepy.API(auth)
 
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
