import _thread
import time

def func1():
    while 1:
        print("hello 1...")
        time.sleep_ms(10)

def func2():
    while 1:
        print("hello 2...")
        time.sleep_ms(10)


_thread.start_new_thread(func1,())
_thread.start_new_thread(func2,())



while 1:
  print("hello 3...")
  time.sleep_ms(10)
