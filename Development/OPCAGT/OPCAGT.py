# from subprocess import Popen, PIPE
# import uptime
#
# server = round(uptime.uptime() / 60 /60, 2)
path = "C:/users/ysiew/desktop/abc.bat"
# batfile = Popen(path, stdout=PIPE)
# stdout , stderr = batfile.communicate()
#
# stop = "Stopped"
# if stop in stdout:
#     print "Stopped is found,quitting"
#
# else:
#     print "No stop , resuming"
#     if server > 1:
#         print "Server > 1 hr"
#
# # data = []
# # while True:
# #   oneline = batfile.stdout.read()
# #   if oneline != '':
# #     data.append(oneline.rstrip())
# #   else:
# #     break
# #
# # print data

import os
b = str(os.system(path))
if "Stopped" in b:
    print "yes"
else:
    print "no"