import _thread
import time

def func1():
    while 1:
        print("hello 1...")
        time.sleep(1)

def func2():
    while 1:
        print("hello 2...")
        time.sleep(1)

_thread.start_new_thread(func1,())
_thread.start_new_thread(func2,())


while 1:
  pass
