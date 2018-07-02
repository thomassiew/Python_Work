#!/usr/bin/python

import threading
import time

class myThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name

   def run(self):
      print "Starting " + self.name
      # Get lock to synchronize threads
      #threadLock.acquire()
      print_time(self.name)
      # Free lock to release next thread
      #threadLock.release()

def print_time(threadName):

      print "%s" % (threadName)


#threadLock = threading.Lock()
threads = []
a= 10000
while a:
    for x in range(5):
        thread1 = myThread(x, "Thread-" + str(x) + "data left: " + str(a))
        thread1.start()
        threads.append(thread1)
        a -=1

