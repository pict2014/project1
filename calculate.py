#!/usr/bin/env python

import json
import pprint as pp
from pymongo import MongoClient
from bson.objectid import ObjectId as objid
import pdb

##have to take out datafrom database and print contry wise contributions to trends

client = MongoClient('localhost', 27017)
db = client.test_database
data = db.tests.find()
current_trend=[]
country=[]
i=0
trend_list=db.tests.distinct('trend')

"""for d in data:
    if d['trend'] not in trend_list:
        trend_list.append(d['trend'])
"""
print trend_list
        
    
