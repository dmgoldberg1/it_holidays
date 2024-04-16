import sqlite3

con = sqlite3.connect("vacancy.db") #подразумеваю, что таблицу ты уже создал
cur = con.cursor()
cur.execute("Delete from vacancy")
# local_company = cur.execute('SELECT company_name FROM vacancy WHERE user_id=?', (885562281,)).fetchall()[0]
# print(len(local_company))
con.commit()
cur.execute("Delete from workers")
con.commit()
con.close()

