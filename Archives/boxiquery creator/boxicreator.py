import path
import csc.csclxmls

pth = path.path('query.xml')
xml = csc.csclxmls.node(pth)

data = xml('//item[@key="AG"]')

# agdata = "("
i = 1
query1 = ""
query2 = ""
query3 = ""
for ag in data:
    if i < 31:
        query1 = query1 + ' assignment="%s" ' % ag.text + "|"
    elif i > 30 and  i < 61:
        query2 = query2 + ' assignment="%s" ' % ag.text + "|"
    else:
        query3 = query3 + ' assignment="%s" ' % ag.text + "|"
    i += 1

query1 = query1.rstrip('|')
query2 = query2.rstrip('|')
query3 = query3.rstrip('|')

ags = open("query.txt", "w+")

ags.write("(" + query1 + ") and " + xml('//item[@key="time"]').text + "\n\n\n\n" + "(" + query2 + ") and " + xml(
    '//item[@key="time"]').text + "\n\n\n\n" + "(" + query3 + ") and " + xml(
    '//item[@key="time"]').text)





#
# agdata2 = agdata.rstrip('|')
#
# agdata2 = agdata2 + ") and " +  xml('//item[@key="time"]').text
#
#
# ags= open("query.txt","w+")
#
# ags.write(agdata2)
