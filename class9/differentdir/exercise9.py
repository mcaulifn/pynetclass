#/usr/bin/env python


import mytest


def main():
    mytest.func1()
    mytest.func2()
    mytest.func3()

    tempclass = mytest.MyClass(1, 'some string', 4)
    tempclass.hello()
    tempclass.not_hello()


if __name__ == "__main__":
   main()
