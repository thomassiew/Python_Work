import re
import sys
import os
import distutils.spawn
import subprocess


os.system("opcagt -stop")
os.system("opcagt -start")

g = subprocess.Popen("opcagt -status", shell=True, stdout=subprocess.PIPE).stdout
d = g.read()
g.close()

if "Stopped" in d:
    print "CODE:FAIL"
    print "Stopped found"
    print "ACTION: Dispatch Ticket to L2"
    print ""
    sys.exit(1)

path = r"C:\server\tools\uptime"
f = subprocess.Popen(path, shell=True, stdout=subprocess.PIPE).stdout
b = f.read()
f.close()
# b = str(os.system(path))
m = re.search(r":\s(\d+?)\s.+?\s(\d+?)\s", b, re.DOTALL)

hours = int(m.group(2))
days = int(m.group(1))

if hours > 0 or days > 0:
    print "CODE:PASS"
    print "Uptime more than 1 hour"
    print "ACTION: Ticket Closure"
    sys.exit(0)
else:
    print "CODE:FAIL"
    print "Uptime less than 1 hour"
    print "ACTION: Dispatch Ticket to L2"
    print "%s" % b
    sys.exit(1)

