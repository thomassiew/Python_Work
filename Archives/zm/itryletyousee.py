import csc.csclxmls, path
#
test = path.path("tryletyousee.xml")
# start= csc.csclxmls.node('<root/>')
#
#
# e_head = start + 'email'
# item1 = e_head + 'item'
# item1['key'] = "i"
# item1.text = "c"
# item2 = e_head + 'item'
# item2['key'] = "try"
# item2.text = "ac"
# item3 = e_head + 'item'
# item3['key'] = "let"
# item3.text = "ac"
# item4 = e_head + 'item'
# item4['key'] = "you"
# item4.text = "see"
#
# start.write(test)




cc = csc.csclxmls.node(test)
a = cc('//item')
b = a.dict

dict2 = {}
for x,y in b: dict2[x['key']] = y

print dict2
print b

# i = 0
# for abc in a:
#     c = dict(zip(abc[i]['key'],abc.text))
#     i += 1
#     print c