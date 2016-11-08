import json
import random

filter = ['apartments', 'commercial', 'school', 'theatre', 'office', 'church', 'warehouse', 'retail', 'college']
with open('geo_data_buildings_NewYork.json') as f:
    content = json.load(f)
    userId = []
    for data in content['features']:
        if data['buildings']:
            for type in data['buildings']:
                if type['type'] in filter:
                    userId.append(data['properties']['user_id'])

userId = list(set(userId))
print(len(userId))
users = []
user = []
indexes = []
indexes1 = []
index = 0
while len(users) < 100:
    index = random.randint(0, len(userId)-1)
    if index not in indexes:
        users.append(userId[index])
        indexes.append(index)
while len(user) < 10:
    index1 = random.randint(0, len(users)-1)
    if index1 not in indexes1:
        user.append(users[index1])
        indexes1.append(index1)

with open('users.txt','w') as u:
    for id in users:
        u.write(str(id))
        u.write('\n')
u.close()

with open('userSample.txt', 'w') as s:
    for id in user:
        s.write(str(id))
        s.write('\n')
s.close()


