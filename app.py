import tweepy
from flask import Flask, render_template, request, flash, redirect, url_for

import logging
import os,sys



app = Flask(__name__)


@app.route('/') # for the home page
def index():
    return render_template('index.html', title="This is FlushTwitter")

#i can't do an async call because flask is synchronous.
#design choice-- when you delete, it will reload the page with the old tweet blacked out and status message shown instead


@app.route('/delete')
def delete():
    duplicateDelete = False
    tweetid = request.args.get('tid')
    print tweetid
    try:
        status = api.destroy_status(tweetid) #name is the id of the tweet
       # print status
        
    except tweepy.TweepError, e: 
        message = "error: "+str(e)
        logging.basicConfig(filename='myapp.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        logging.debug("*******************************\n")
        duplicateDelete = True
   
    if (duplicateDelete):
        flash('That tweet does not exist.')
    else: 
        flash('Deleted tweet.')
    #start redirect
    return redirect(url_for("hello"))
    



@app.route('/next')
def hello():

    user = request.args.get('handle')

    tweets= {};
    try:
        my_tweets=api.user_timeline(id=user, count=100)
 
 
    
  
  
        for tweet in my_tweets:
            if "RT" not in tweet.text:
                tweets[tweet.id ]= tweet.text
        
    except tweepy.TweepError, e:
        message = "error: "+str(e)
        logging.basicConfig(filename='myapp.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        logging.debug("*******************************\n")

    return render_template('default.html', name=user, seq=tweets)
    
    

@app.route('/map/<hashtag>')
def map(hashtag=None):
    tweets = api.search(q="warriors", rpp="100")
    count = 0
    for t in tweets:
        print str(t._json.get('location'))
  
        # if (t.geo_enabled == True):


        #     print str(t.place.bounding_box.coordinates) +"\n"
        # else:
        #     flash("No locations found.")

    return render_template('map.html', name=hashtag)




if __name__ == "__main__":
    app.debug = True
#    app.config['SESSION_TYPE'] = 'filesystem'

    config={}

    execfile("twitter.conf", config)
    app.config['SECRET_KEY'] = config["secret_key"]
    auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
    auth.set_access_token(config["access_token"], config["access_token_secret"])
    api= tweepy.API(auth)
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
