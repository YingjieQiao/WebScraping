import json

with open('material science_2019.json', 'r') as file:
     data = file.read() # use `json.loads` to do the reverse
     

print(type(json.loads(data)))
print(len(data))
     
     