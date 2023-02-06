import json

with open(f'file_system/total.json', 'r') as file:
    curr = json.load(file)
    curr['global']
    k = 'bla'
    v = 10
    count = curr['global'].get(k)
    if count:
        curr['global'][k] = count + v
print(curr['global'])
with open('file_system/total.json', 'w+') as jf:
    json.dump(curr, jf)
