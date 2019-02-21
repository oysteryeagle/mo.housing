import sqlite3
import operator
conn = sqlite3.connect('database.db')
cur1 = conn.cursor()
dct = dict()
count = dict()
avg = dict()
for entry in cur1.execute('''SELECT name,price,lat,long FROM Housing WHERE lat is not null and lat is not 0'''):
    coordinates = entry[2],entry[3]
    dct[coordinates] = dct.get(coordinates,0) + entry[1]
    count[coordinates] = count.get(coordinates,0) + 1
for location in dct:
    avg[location] = dct[location]/count[location]

sorted_x = sorted(avg.items(), key=operator.itemgetter(1))
#print(sorted_x)
#for x in sorted_x:
#    print(x)

with open('avg.txt','w') as f:
    for tuple in sorted_x:
        cur2 = conn.cursor()
        for item in cur2.execute('''SELECT name FROM Housing WHERE lat is (?)''',(tuple[0][0],)):
            f.write(str(item[0])+'\n')
        f.write(str(tuple[1])+'\n\n')



#print(avg)
