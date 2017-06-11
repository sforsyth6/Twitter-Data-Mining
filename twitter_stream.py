import tweepy
import json
from tweepy.streaming import StreamListener

#Twitter authorization
auth = tweepy.OAuthHandler(consumer_key='uTDerR4hkdMNy2JOp4IMnNJBc',
                        consumer_secret='61SaSdgC7dUIo3DJk4DNzwrNCH33DHhLVwK3NvCV5SZQLFpvI2')

auth.set_access_token('1305197144-ygdGMzLDN6F2YirHU7rICx47QE1Ovok3P8lm6IE',
                'NzGoADqIPaAfozgzJe1VAmnRQVrCxejNUrPBvVpUXwUQv')

api = tweepy.API(auth)

class StdOutListener(StreamListener):

    def on_data(self, data):
	data = json.loads(data)
	if 'lang' in data.keys():
		if data['lang'] == 'en':
			if 'RT' not in data['text']:
				print json.dumps(data)
        return None

    def on_error(self, status):
        print status
	return None

#Find the trends
trend = api.trends_place(23424977)
trends = []
for i in range(10):
	trends.append(trend[0]['trends'][i]['name'])

#Download tweets within the USA that pertain to the word in track
l = StdOutListener()
stream = tweepy.Stream(auth, l)
stream.filter(track = trends)

