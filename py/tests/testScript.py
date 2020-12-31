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
        x = self.db["key"]
        assert x == "value"

    def test_get(self):
        self.db.create('key1', 'value1')
        x = self.db.get('key1')
        assert x == 'value1'

    def test_set1(self):
        self.db["foo"] = "bar"
        assert "bar" == self.db.db["foo"]

    def test_set(self):
        self.db.create('foo1', 'bar1')
        x = self.db.get('foo1')
        assert x == 'bar1'


if __name__ == "__main__":
    tests = TestClass()
    test_methods = [method for method in dir(tests) if callable(getattr(tests, method)) if method.startswith('test_')]
    for method in test_methods:
            getattr(tests, method)()  # run method
            print(".", end="")