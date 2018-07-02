# Base version:
# 11.11.025
# 11.11.025
# OAWIN_00032:11.14.014
# Hotfix version:
# HFWIN_14096:11.14.158
# HFWIN_14107:11.14.172



from subprocess import Popen, PIPE

path = "C:/users/ysiew/desktop/abc2.bat"
batfile = Popen(path, stdout=PIPE)

data = []
while True:
  oneline = batfile.stdout.readline()
  if oneline != '':
    data.append(oneline.rstrip())
  else:
    break

abc = str(''.join(data))
print repr(abc)
defg = "Base version:11.11.02511.11.025OAWIN_00032:11.14.014Hotfix version:HFWIN_14096:11.14.158HFWIN_14107:11.14.172"
print repr(defg)
if defg == abc:
    print "same"
else:
    print "diff"


