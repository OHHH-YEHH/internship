from __future__ import print_function
from sys import path
path.append('..\\modules')

import KeyStoreDB as DB

class TestClass(object):

    db = DB.load('..\\main.db', auto_dump=False)

    def test_load(self):
        x = DB.load('x.db', auto_dump=False)
        assert x is not None
    
    def test_set1(self):
        self.db["foo"] = "bar"
        assert "bar" == self.db.db["foo"]

if __name__ == "__main__":
    tests = TestClass()
    test_methods = [method for method in dir(tests) if callable(getattr(tests, method)) if method.startswith('test_')]
    for method in test_methods:
            getattr(tests, method)()  # run method
            print(".", end="")