# Twitter-Data-Mining
This code is an attempt at data mining twitter. It successfully implements the tweepy twitter api for python to gather tweets based on the top 10 trends within the US and then analyzes certain features of the tweets. The data set used here was approximately 23,000 tweets.

To collect tweets from the twitter api twitter_stream.py is run and the output is piped into tweets.txt (not contained here because it was too large to upload ~85 MB): python twitter_stream.py > tweets.txt
This will continue to run until it is manually stopped with (ctr+c) as to allow for me to run it for as long as I wish

structured.py is then run which takes in the raw data from tweets.txt, structures it, pipes it into another file called tweets.csv as to avoid a memory overload, and then opens the csv it just created to analyze the now structured data. 

So far there are only three specific attributes that I've analyzed. 
-I've created a histogram of sources used to tweet (i.e iphone, andorid,...)
-I've compared two features of the data by plotting the amount of followers a user has vs the number of tweets they've tweeted
-I've created a map of the united states and plotted the location where each tweet is generated

For now, this is the extent of the project. Until I create a text analysis machine learning program of my own (because I'm too cheap to buy one) this is as much information as I care to gain from this data set. When I do create a text analysis package I intend be able to tell the polarity of the text (positive or negative) whether it was a subjective sentence or objective and other various details about the text itself to be able to gain further insight into each tweet. 
