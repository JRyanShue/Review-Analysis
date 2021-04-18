import json

testlist = ["0", "1", "2"]

with open('test.txt', 'w') as file:
    json.dump(testlist, file)
