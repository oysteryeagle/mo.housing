import sqlite3
import operator
conn = sqlite3.connect('database.db')
conn2 = sqlite3.connect('frequency.db')
cur1 = conn.cursor()
cur2 = conn2.cursor()
cur2.execute('''
CREATE TABLE IF NOT EXISTS Housing (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, coordinates INTEGER UNIQUE, lat TEXT, long TEXT, count INTEGER
)''')
priceSum = dict()
count = dict()
avg = dict()
for entry in cur1.execute('''SELECT name,price,lat,long FROM Housing WHERE lat is not null and lat is not 0'''):
    coordinates = entry[2],entry[3]
    priceSum[coordinates] = priceSum.get(coordinates,0) + entry[1]
    count[coordinates] = count.get(coordinates,0) + 1
for location in priceSum:
    #avg[location] = priceSum[location]/count[location]
    print(location[0])
    cur2.execute('''INSERT OR IGNORE INTO Housing (coordinates,lat,long,count) VALUES (?,?,?,?)''',(str(location),location[0],location[1],count[location]))
    conn2.commit()
conn.close()
conn2.close()
