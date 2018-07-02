
import time
import path
import csc.csclxmls


rulebase = path.path('rulebase.xml')
rules = csc.csclxmls.node(rulebase)
ag = "C.APAC.MY.WIN.EVT"

k = rules('//accept/item[@AG="%s"]' % ag)
abc = k['AG']
print k.Xpath
print abc
print k.text