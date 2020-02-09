import json

abstracts = {'a':1,'b':2}

with open('file1', 'w') as file1:
    file1.write(json.dumps(abstracts))