#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This modules parse and upload data to mongodb
"""
from re import sub
import ijson
import pymongo
import pprint

"""
Your task is to wrangle the data and transform the shape of the data
into the model as shown below. The output should be a list of dictionaries
that look like this:

{
    "_id": "57f69a76ef1746266976cad2",
    "picture": "http://placehold.it/32x32",
    "name": {
        "last": "Raymond",
        "first": "Pope"
    },
    "gender": "male",
    "age": 34,
    "email": "poperaymond@amtas.com",
    "phone": "+1 (811) 526-3095",
    "address": {
        "city": " Bendon",
        "state": " Nebraska",
        "street": "526 Ainslie Street",
        "zip": " 2221"
    },
    "balance": 2650.9,
    "company": "AMTAS",
    "isActive": true
}

"""

def upload_file_data(fileName):

    db=get_db('intuit')
    with open(fileName, "r") as file:
        for item in ijson.items(file, "item"):
            # 1. lets first split name in first name and last name
            name=item['name'].split(' ')
            item['name']={'first':name[0],'last':name[1]}

            # 2. Convet dollar string to decimal
            item['balance'] = float(sub(r'[^\d\-.]', '', item['balance']))

            # 3. Split address into Street, City, State and Zipcode
            address=item['address'].split(',')
            item['address']={'street':address[0],'city':address[1],'state':address[2],'zip':int(address[3])}

            #4. Insert item to MongoDB
            db.data.save(item)
            pprint.pprint(item)
            print '-------------------------------------'

  
def get_db(db_name):
    from pymongo import MongoClient
    try:
        return MongoClient('mongodb://localhost:27017')[db_name]
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to server: %s" % e


if __name__ == "__main__":
    upload_file_data("./data.txt")

    