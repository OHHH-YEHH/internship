#!/usr/bin/env python3
from sys import path
path.append('..\\modules')

import KeyStoreDB as DB

# DB initialization
db = DB.load() # -> creates KeyValDatabase.db in current working directory.
# db = DB.load('..\\main.db', auto_dump=True) # -> db file can be initialized using an optional file path. 


# create operation
db.create('key', 'value')
# db.create('key','value') # -> KeyError: 'Key already present in database'

db.create("Abhinav Anand",{"Headache":[{
                        "name":"asprin",
                        "dose":"Morning",
                        "strength":"500 mg"
                    },
                    {
                        "name":"Crocin",
                        "dose":"Afternoon",
                        "strength":"500 mg"
                    },
                    {
                        "name":"D-Cold",
                        "dose":"Night",
                        "strength":"500 mg"
                    }
                    ]})

db.dump()

# read operation
print(db.get('Abhinav Anand')) # -> returns valid JSON object

# delete operation
db.rem('Abhinav Anand')
# db.rem('Abhinav Anand') # -> KeyError: 'Key is not present in database'