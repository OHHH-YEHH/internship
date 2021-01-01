from __future__ import print_function
from sys import path
path.append('..\\modules')

import KeyStoreDB as DB

class TestClass(object):

    db = DB.load('..\\main.db', auto_dump=False)

    def test_load(self):
        x = DB.load('x.db', auto_dump=False)
        assert x is not None
    
    def test_get1(self):
        self.db["key"] = "value"
        x = self.db["key"][0]
        assert x == "value"

    def test_get(self):
        self.db.create('key1', 'value1',10)
        x = self.db.get('key1')[0]
        assert x == 'value1'

    def test_set1(self):
        self.db["foo"] = "bar"
        assert "bar" == self.db.db["foo"][0]

    def test_set(self):
        self.db.create('foo1', 'bar1')
        x = self.db.get('foo1')[0]
        assert x == 'bar1'

    def test_exists(self):
        self.db.create('key2', 'value')
        x = self.db.exists('key2')
        assert x is True
        self.db.rem('key2')

if __name__ == "__main__":
    tests = TestClass()
    test_methods = [method for method in dir(tests) if callable(getattr(tests, method)) if method.startswith('test_')]
    for method in test_methods:
            getattr(tests, method)()  # run method
            print(".", end="")