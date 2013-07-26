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




conn = httplib.HTTPSConnection("api.twitter.com")

conn.request("POST","/oauth2/token/",param,headers)
response=conn.getresponse()

payload = response.read()

access_token = payload[payload.find("n\":\"")+4:payload.find("token_type")-3]
get_headers = {"Authorization":"Bearer "+access_token}



newclient = MongoClient('localhost', 27017)
db = newclient.trends
db.users.remove()

for name in names:

    url = "/1.1/search/tweets.json?q=" + str(name['query'])
    conn.request("GET",url,"",get_headers)
    get_resp = conn.getresponse()
    sample = get_resp.read()
    data = json.loads(str(sample))

    #CHECKING IF LOCATION = NONE
    for val in data['statuses']:
        tz = str(val['user']['time_zone']).encode('utf-8')
        if(tz == 'None'):
            tz = str(val['user']['location']).encode('utf-8')
    
        if(tz == 'None'):
            tz = str(val['place']).encode('utf-8')    
    
        if(tz != 'None'):    
            db.users.insert({"topic" : str(name['name']).encode('utf-8'),"time_zone" : tz})
    

    #SORTING THE LIST WRT TIME ZONE        
    newlist = sorted(db.users.find({"topic":str(name['name']).encode('utf-8')}), key=lambda k: k['time_zone'])

    tz = ''
    trend = ''
    for x in newlist:
        if(tz != x['time_zone']):
            tz = x['time_zone']
            if(trend != x['topic']):
                trend = x['topic']
                print "--------"*5
                print "No of people talking about "+ x['topic']+" from various countries are"
                print "--------"*5
            print tz + ":",
            print db.users.find({"topic" :x['topic'],"time_zone":tz}).count()




