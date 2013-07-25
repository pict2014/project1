#!/usr/bin/env python

import urllib
import httplib
import base64
import json
import pprint as pp
from pymongo import MongoClient
from bson.objectid import ObjectId as objid
import pdb



CONSUMER_KEY='tI0bUJuctVgzA82wGYLiQ'
CONSUMER_SECRET='59GVWA6j7RJt1Ntw2cFi57FS91jzRFIk6lbNzH8Cs8'

#OAUTH_TOKEN='165807027-Y9GeHly2EiJ5LBzcI3eAGvNp9M44kpO5tK9yfu2n'
#OAUTH_TOKEN_SECRET='qTopfcbhvo1qo3RvWvqzxDg2IHeJETyz8x5SPn8n0zk'

enc_str= base64.b64encode(CONSUMER_KEY+":"+CONSUMER_SECRET)

conn = httplib.HTTPSConnection("api.twitter.com")

#Acquiring the access token
param = urllib.urlencode({'grant_type':'client_credentials'})
headers = {"Authorization":"Basic "+enc_str,"Content-type": "application/x-www-form-urlencoded;charset=UTF-8"
}
conn.request("POST","/oauth2/token/",param,headers)
response=conn.getresponse()
payload = response.read()
access_token=payload[payload.find("n\":\"")+4:payload.find("token_type")-3]
get_headers={"Authorization":"Bearer "+access_token}

##Getting WorldWide Trends 
conn.request("GET","/1.1/trends/place.json?id=1","",get_headers)  
get_resp = conn.getresponse()
sample = get_resp.read()

##converting the received string in JSON form 
data = json.loads(str(sample))
#print pp.pprint(data[0])
names = data[0]['trends']

print "-----------------------------Trends-----------------------------------"
for x in names:

    #printing each trending topic/person etc
    print "\n-----------Tweets for :" + x['name'] + "--------------"
    conn.request("GET","/1.1/search/tweets.json?q="+str(x['query']),"",get_headers)
    tweets_resp = conn.getresponse()
    tweets = tweets_resp.read()
    tweets_json = json.loads(str(tweets))

    #print pp.pprint(tweets_json)
    for s in tweets_json['statuses']:
        #printing names of users and tweets for each trending topic 
        print s['user']['name']
        print s['text']+"\n"
    
print "\n"
    
