import tweepy
import json
from tweepy.streaming import StreamListener

#Twitter authorization
auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class StdOutListener(StreamListener):

    def on_data(self, data):
	data = json.loads(data)
	#Specify english only tweets
	if 'lang' in data.keys():
		if data['lang'] == 'en':
			#No retweets
			if 'RT' not in data['text']:
				print json.dumps(data)
        return None

    def on_error(self, status):
        print status
	return None

#Find the trends within the US
trend = api.trends_place(23424977)
trends = []
for i in range(10):
	trends.append(trend[0]['trends'][i]['name'])

#Download tweets within the USA that pertain to the word in track
l = StdOutListener()
stream = tweepy.Stream(auth, l)
stream.filter(track = trends)

