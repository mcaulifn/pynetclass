#/usr/bin/env python

from __future__ import print_function

class MyClass(object):
    def __init__(self, var1, var2, var3):
        self.var1 = var1
        self.var2 = var2
        self.var3 = var3

    def hello(self):
        print("Hello world")
        print("%s, %s, and %s were the variables passed in." %(str(self.var1), str(self.var2), str(self.var3)))
        return

    def not_hello(self):
        print("Goodbye") 
        print("%s, %s, and %s were the variables passed in." %(str(self.var1), str(self.var2), str(self.var3)))
        return

class MyChildClass(MyClass):
    def __init__(self):
        print("__init__ from child class")

    def hello(self):
        print("This is different.")
        print("Still saying 'hi', though.")
        print("%s, %s, and %s were the variables passed in." %(str(self.var1), str(self.var2), str(self.var3)))
        return

def func1():
    print("This is func1 from world.py.")

def main():
    print("This is main from world.py.")

if __name__ == "__main__":
    main()

