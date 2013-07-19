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

if __name__ == "__main__":
        
    print "Basic "+enc_str
    conn = httplib.HTTPSConnection("api.twitter.com")
    #Acquiring the access token
    param = urllib.urlencode({'grant_type':'client_credentials'})
    headers = {"Authorization":"Basic "+enc_str,"Content-type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    conn.request("POST","/oauth2/token/",param,headers)
    response=conn.getresponse()
    #print "Status: "+str(response.status) 
    #print "Reason: "+str(response.reason)
    payload=response.read()
    #print payload
    ##Simple string manipulation to get the access token
    access_token=payload[payload.find("n\":\"")+4:payload.find("token_type")-3]
    
    #print "Acces_token is: "+access_token
    
    get_headers={"Authorization":"Bearer "+access_token}
    
    ##Acquiring the user_timeline
    
    uinput = str(raw_input("Enter twitter handle: "))
    #print uinput
    
    ##Checking whether the info with the screen_name already in database
    client = MongoClient('localhost', 27017)
    db = client.test_database
    screen_name = db.posts.find_one({"screen_name":str(uinput)})
    #pdb.set_trace()
    
    #if in database print from database
    if screen_name:
        print "---HIT! Printing from database---\n"
        print "Screen Name: "+screen_name['screen_name']
        print screen_name['name'] + "\n"
        print screen_name['location']+ "\n"
        print screen_name['description'] + "\n"
       
    #Else print and insert into data base
    else:
        conn.request("GET","/1.1/statuses/user_timeline.json?screen_name=%s&count=10"%(uinput),"",get_headers)
        get_resp=conn.getresponse()
        #print str(get_resp.reason)
        #print str(get_resp.status)
        statuses=get_resp.read()
        data=json.loads(str(statuses))
        print "---Taking Info for the first time, Will go to database---\n"
        print "Screen Name: "+data[0]['user']['screen_name']
        print data[0]['text']+ "\n\n"
        #user_detail = data[0]['user']
        #print pp.pprint(user_detail)
        db.posts.insert(data[0]['user'])
       
    #print "--------------------------------------------------Information---------------------------------------------"
    #import pdb; pdb.set_trace()
    
    #print "\n------------------------------------------------Data to read---------------------------------------------"
    #print data
    #pretty = pp.pprint(data[0])
    
    #f=open("data1.json","w")
    #f.write(str(data[0]))
    
    #print data[0]['user']['screen_name']
    #print pretty
