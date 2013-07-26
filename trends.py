#!/usr/bin/env python
import urllib
import httplib
import base64
import json
import pprint as pp
from pymongo import MongoClient
from bson.objectid import ObjectId as objid




CONSUMER_KEY='tI0bUJuctVgzA82wGYLiQ'
CONSUMER_SECRET='59GVWA6j7RJt1Ntw2cFi57FS91jzRFIk6lbNzH8Cs8'


enc_str= base64.b64encode(CONSUMER_KEY+":"+CONSUMER_SECRET)




conn = httplib.HTTPSConnection("api.twitter.com")
#Acquiring the access token
param = urllib.urlencode({'grant_type':'client_credentials'})
headers = {"Authorization":"Basic "+enc_str,"Content-type": "application/x-www-form-urlencoded;charset=UTF-8"}
conn.request("POST","/oauth2/token/",param,headers)
response=conn.getresponse()

payload = response.read()
access_token=payload[payload.find("n\":\"")+4:payload.find("token_type")-3]
get_headers={"Authorization":"Bearer "+access_token}
conn.request("GET","/1.1/trends/place.json?id=1","",get_headers)
get_resp = conn.getresponse()
sample = get_resp.read()




data = json.loads(str(sample))
#print pp.pprint(data[0]['trends'])
names = data[0]['trends']


print "Currrent trending topics with tweets:"

for val in names:

    print "-"*50
    print "\nTopic Name: " + val['name']
    print "-"*50

    # generating url for search
    url = "/1.1/search/tweets.json?q=" + str(val['query'])+"&count=4"
    print url
    conn.request("GET",url,"",get_headers)
    get_resp = conn.getresponse()
    sample = get_resp.read()
    data = json.loads(str(sample))

    cnt = 1
    for status in data['statuses']:
        print str(cnt) + ") " + status['user']['name'].encode('utf-8') +":",
        print status['text'].encode('utf-8')
        cnt = cnt+1
