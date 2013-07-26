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
for d in data:
    print d
