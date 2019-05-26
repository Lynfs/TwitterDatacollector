from tweepy import API 
from tweepy import Cursor
from tweepy import OAuthHandler
import twitter_credentials
import numpy as np
import pandas as pd

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class Datatweet():
    def df_convert(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['post-id'] = np.array([tweet.id for tweet in tweets])
        df['post-len'] = np.array([len(tweet.text) for tweet in tweets])
        df['post-date'] = np.array([tweet.created_at for tweet in tweets])
        df['post-source'] = np.array([tweet.source for tweet in tweets])
        df['post-likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets-count'] = np.array([tweet.retweet_count for tweet in tweets])
        return df

if __name__ == '__main__':
    ids = list()
    twitter_client, tweet_data = TwitterClient(), Datatweet()
    api = twitter_client.get_twitter_client_api()
    counter = 0
    while(True):
        for user in Cursor(api.followers).items():
            ids.append(user.screen_name)
            counter+=1
            #counter = number of followers to get tweets
            if counter == 5:
                break
        break
    for value in ids:
        tweets = api.user_timeline(screen_name="%s" %value, count=10)#count = how many tweets to get peer user
        df = tweet_data.df_convert(tweets)
        print(f'\nUSER_ACCOUNT ========> {value}\n {df}')
