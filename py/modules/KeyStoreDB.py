#!/usr/bin/env python3
import sys
import os
import signal
import json
from threading import Thread
import math
import datetime

JSONVALUESIZE = 16*(2**10)
FILESIZE = 2**30

def load(location ="..\\KeyValDatabase.db", auto_dump=False, sig=True):
    '''Return a keyStoredb object. location is the path to the json file.'''
    return KeyStoreDB(location, auto_dump, sig)

class KeyStoreDB(object):
    key_string_error = TypeError('Key must be a string!')
    key_charSize_error = ValueError('Key size should be smaller than 32 chars')
    value_size_tooLarge_error = ValueError('value JSON Object should be smaller than 16KB ')
    duplicate_keyFound_error = KeyError('Key already present in database')
    key_notFound_error = KeyError('Key is not present in database')
    key_expired_error = RuntimeError('Associated key timeout ')
    file_exceed_error = RuntimeError('File size should not exceed 1GB')
    def __init__(self, location, auto_dump, sig):
        '''Creates a database object and loads the data from the location path. 
            If the file does not exist it will be created on the first update.
        '''
        self.load(location, auto_dump)
        self.dthread = None
        if sig:
            self.set_sigterm_handler()
    
    def set_sigterm_handler(self):
        '''Assigns sigterm_handler for graceful shutdown during dump()'''
        def sigterm_handler():
            if self.dthread is not None:
                self.dthread.join()
            sys.exit(0)
        signal.signal(signal.SIGTERM, sigterm_handler)

    def __setitem__(self, key, value):
        '''Syntax for setting value to key'''
        return self.create(key, value)

    def create(self, key, value,timeToLive=2592000):
        '''Set the str value of a key
            key stored for default 30 days'''
        if self.exists(key):
            if self.isExpired(key,timeToLive):
                self.rem(key)
                raise self.key_expired_error
            else:
                raise  self.duplicate_keyFound_error    
        else : 
            if isinstance(key, str):
                if len(key)<=32:
                    global JSONVALUESIZE
                    valueSize = len(json.dumps([value,(self.addSecs(datetime.datetime.now()
                                                            , timeToLive)).isoformat()]))  
                    if valueSize<JSONVALUESIZE:
                        if os.path.exists(self.loco) and \
                           (os.stat(self.loco).st_size + len(key) + valueSize )>FILESIZE :
                            raise self.file_exceed_error
                        else :
                            self.db[key] = [value,(self.addSecs(datetime.datetime.now()
                                                            , timeToLive)).isoformat()]
                            self._autodumpdb()
                            return True          
                    else :
                        raise self.value_size_tooLarge_error  
                else:
                    raise self.key_charSize_error
                
            else:
                raise self.key_string_error
    
    def exists(self, key):
        '''Return True if key exists in db, return False if not'''
        return key in self.db

    def isExpired(self,key,timeToLive):
        if datetime.datetime.now() > datetime.datetime.strptime(self.get(key)[1],'%Y-%m-%dT%H:%M:%S.%f'):
            return True

    def addSecs(self,tm, secs):
        return tm + datetime.timedelta(seconds=secs)

    def _autodumpdb(self):
        '''Write/save the json dump into the file if auto_dump is enabled'''
        if self.auto_dump:
            self.dump()
    
    def dump(self):
        '''Force dump memory db to file'''
        json.dump(self.db, open(self.loco, 'wt'))
        self.dthread = Thread(
            target=json.dump,
            args=(self.db, open(self.loco, 'wt')))
        self.dthread.start()
        self.dthread.join()
        return True
    
    def load(self, location, auto_dump):
        '''Loads, reloads or changes the path to the db file'''
        location = os.path.expanduser(location)
        self.loco = location
        self.auto_dump = auto_dump
        if os.path.exists(location):
            self._loaddb()
        else:
            self.db = {}
        return True

    def _loaddb(self):
        '''Load or reload the json info from the file'''
        try: 
            self.db = json.load(open(self.loco, 'rt'))
        except ValueError:
            if os.stat(self.loco).st_size == 0:  # Error raised because file is empty
                self.db = {}
            else:
                # File is not empty, avoid overwriting it 
                pass 
    
    def __getitem__(self, item):
        '''Syntax for get()'''
        return self.get(item)

    def get(self, key):
        '''Get the value of a key'''
        try:
            return self.db[key]
        except KeyError:
            raise self.key_notFound_error

    def getall(self):
        '''Return a list of all keys in db'''
        return self.db.keys()
    
    def __delitem__(self, key):
        '''Syntax for rem()'''
        self.rem(key)

    def rem(self, key):
        '''Delete a key'''
        if not key in self.db: 
            raise self.key_notFound_error
        del self.db[key]
        self._autodumpdb()    