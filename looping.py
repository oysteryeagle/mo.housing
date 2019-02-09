import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur2 = conn.cursor()
for x in cur.execute('''SELECT coordinates,id FROM Housing WHERE coordinates is not null'''):
    id = x[1]
    print(id)
    coordinates = x[0].split(', ')
    print(coordinates)
    cur2.execute('''UPDATE Housing SET lat = ? where id = ?''',(coordinates[0],id))
    cur2.execute('''UPDATE Housing SET long = ? where id = ?''',(coordinates[1],id))
conn.commit()
conn.close()
