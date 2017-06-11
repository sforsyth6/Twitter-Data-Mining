import tweepy
import json
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from collections import Counter

#This function cleans the data and makes it easier to use
def cleaning(singleTweet):
	tweet = singleTweet
			
	#Source issues: Format the source output
	source = None
	tweetSplit = tweet['source'].split('="nofollow">')[1]
	if 'Twitter for ' in tweetSplit:
		source =  str(tweet['source'].split('="nofollow">')[1].split('Twitter for ')[1].split('</a>')[0])
	elif 'Twitter Web' in  tweetSplit:
		source = 'Web'
	else:
		source = str(tweetSplit.split('</a>')[0])
	
	#Place issues: Check if there is a place parameter and then break it up into city and state
	if tweet['place'] != None:
		if ',' in tweet['place']['full_name']:
			try:
				city,state = tweet['place']['full_name'].split(', ')
			except: 
				city,state = tweet['place']['full_name'], None 
		else: 
			city = tweet['place']['full_name']
			state = None
	else:
		city = None
		state = None
	
	#text issues: remove all links and emojis from the text
	textTemp = tweet['text']
	if 'http' in textTemp:
		q = 0
		split = textTemp.split()
		while q < len(split):
			if split[q].startswith('https'):
				del split[q]
			else:
				q += 1
		textTemp = ' '.join(split)
	text = ''.join([x for x in textTemp if ord(x) < 128])
	
	return source,city,state,text

#Put the semi-structured data into a data frame
def dataFrame(singleTweet,source,city,state,text):
	tweets = pd.DataFrame()
	tweets['source'] = [source]
	tweets['city'] = [city]
	tweets['state'] = [state]
	tweets['text'] = [text]
	
	tweets_data = [singleTweet]
	tweets['month'] = map(lambda tweet: tweet['created_at'].split()[1] if tweet['place'] != None else None, tweets_data)
	tweets['day'] = map(lambda tweet: tweet['created_at'].split()[2] if tweet['place'] != None else None, tweets_data)
	tweets['time'] = map(lambda tweet: tweet['created_at'].split()[3] if tweet['place'] != None else None, tweets_data)
	tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
	tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)
	tweets['timestamp_ms'] = map(lambda tweet: tweet['timestamp_ms'], tweets_data)
	tweets['user'] = map(lambda tweet: tweet['user']['screen_name'], tweets_data)
	tweets['followers'] = map(lambda tweet: tweet['user']['followers_count'], tweets_data)
	tweets['statuses_count'] = map(lambda tweet: tweet['user']['statuses_count'], tweets_data)
	tweets['coord'] = map(lambda tweet: tweet['place']['bounding_box']['coordinates'][0][0] if tweet['place'] != None else None, tweets_data)

	#Create a new csv file and append each instance of structured data to it (This is to avoid destroying your memory when dealing with large tweet volume)
	if os.path.isfile(fileName) != True:
		tweets.to_csv(fileName)
	else:
		tweets.to_csv(fileName, mode = 'a', header=False)
	
	return None

#Open the csv file that was created in the above function
def openFile():
	files =  pd.read_csv(fileName)
	files = files.drop('Unnamed: 0', axis = 1)
	
	return files

#Load in the raw semi-structured data from tweets.txt (this was generated from twitter_stream.py)
def importTweets():
	try: 
		os.system('rm %s' %fileName)
	except: 
		pass

	dataFile = open('tweets.txt', 'r')
	for line in dataFile:
			try:
				singleEntry= json.loads(line)
			except: 
				continue
			source,city,state,text = cleaning(singleEntry)
			dataFrame(singleEntry,source,city,state,text)
	return None

#Basemap stuff to make a map of the US
def draw_map_background(m, ax):
    ax.set_axis_bgcolor('#729FCF')
    m.fillcontinents(color='green', ax=ax, zorder=0)
    m.drawcounties(ax=ax)
    m.drawstates(ax=ax)
    m.drawcountries(ax=ax)
    m.drawcoastlines(ax=ax)

fileName = 'tweets.csv'
importTweets()
		
#-------------------------------------------analyze the tweets-----------------------------------------------
tweets = openFile()

#plot a histogram of the sources used in the tweets
source = tweets['source']
count = Counter(source)
df = pd.DataFrame.from_dict(count, orient='index')
df.plot(kind='bar')

#See if there is any coorelation between follower count and status count
tweets.plot(kind='scatter', x='followers', y='statuses_count')

#plot location of tweet on a US map
KM = 1000
clat = 39.3
clon = -94.7333
wid = 5500 * KM
hgt = 3500 * KM
m = Basemap(width=wid, height=hgt, rsphere=(6378137.00,6356752.3142),
            resolution='i', area_thresh=2500., projection='lcc',
            lat_1=38.5, lat_2=38.5, lat_0=clat, lon_0=clon)
fig = plt.figure()
ax = fig.add_subplot(111)
draw_map_background(m, ax)
lon = []
lat = []

for coord in tweets['coord']:
	if type(coord) is str:
		newCoord = coord.strip('[').strip(']').split(', ')
		lon.append(float(newCoord[0]))
		lat.append(float(newCoord[1]))

x,y = m(lon, lat)
m.plot(x, y, 'bo', markersize=5)
plt.show()

