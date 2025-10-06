import os
import re
from time import time
import sys

lifeline = re.compile(r"(\d) received")
report = ("No response", "Partial Response", "Alive")
start=time()

post_report=[0, 0, 0]
for host in range(1,49):
#   ip = "129.11.146."+str(host)
   ip = "90.194.19." + str(host)
   pingaling = os.popen("ping -q -c2 " + ip, "r")
   print ("Testing ", ip, sys.stdout.flush(), end=" -> ")
   
   while 1:
      line = pingaling.readline()
      if not line: break
      igot = re.findall(lifeline, line)
      
      if igot:
         res = report[int(igot[0])]
         print (res)
         
         if res == report[0]:
            post_report[0]+=1
         elif res == report[1]:
            post_report[1]+=1
         elif res == report[2]:
            post_report[2]+=1
         
stop=time()
elapsed = stop - start

print (f"Time elapsed {elapsed} - done.")
print(f"{report[0]}({post_report[0]} {report[1]}({post_report[1]} {report[2]}({post_report[2]})")