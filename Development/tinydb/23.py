from tinydb import TinyDB, Query
db = TinyDB('db.json')



db.insert({'type': 'apple', 'count': 7})




print db.all()