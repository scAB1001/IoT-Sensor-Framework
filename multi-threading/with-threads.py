import os
import re
from time import time
import sys
from threading import Thread
class testit(Thread):
   def __init__ (self,ip):
      Thread.__init__(self)
      self.ip = ip
      self.status = -1
   def run(self):
      pingaling = os.popen("ping -q -c2 "+self.ip,"r")
      while 1:
        line = pingaling.readline()
        if not line: break
        igot = re.findall(testit.lifeline,line)
        if igot:
           self.status = int(igot[0])
testit.lifeline = re.compile(r"(\d) received")
report = ("No response","Partial Response","Alive")
#print time.ctime()
start=time()
pinglist = []
for host in range(1,49):
#   ip = "129.11.144."+str(host)
   ip = "90.194.19."+str(host)
   current = testit(ip)
   pinglist.append(current)
   current.start()
for pingle in pinglist:
   pingle.join()
   print ("Status from ",pingle.ip,"is",report[pingle.status])
stop=time()
elapsed = stop -start
print ("Time elapsed", elapsed)
print ("done.")
