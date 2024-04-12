import psycopg2
import csv

conn = psycopg2.connect(host="localhost", dbname="Loop", user="postgres", password="postgres", port=5432)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS store_status(store_id BIGINT,
							status VARCHAR(10),
							timestamp VARCHAR(50));""")

with open("store status.csv","r") as file:
	reader = csv.reader(file)
	next(reader)
	for row in reader:
		cur.execute(f"INSERT INTO store_status(store_id,status,timestamp) VALUES({row[0]},'{row[1]}','{row[2]}');")


cur.execute("""CREATE TABLE IF NOT EXISTS menu_hours(store_id BIGINT,
							day INT,
							start_time VARCHAR(10),
							end_time VARCHAR(10));""")


with open("Menu hours.csv","r") as file:
	reader = csv.reader(file)
	next(reader)
	for row in reader:
		cur.execute(f"INSERT INTO menu_hours(store_id,day,start_time,end_time) VALUES({row[0]},{row[1]},'{row[2]}','{row[3]}');")

cur.execute("""CREATE TABLE IF NOT EXISTS timezones(store_id BIGINT,
							timezone VARCHAR(30));""")

with open("bq-results-20230125-202210-1674678181880.csv","r") as file:
	reader = csv.reader(file)
	next(reader)
	for row in reader:
		cur.execute(f"INSERT INTO timezones(store_id,timezone) VALUES({row[0]},'{row[1]}');")

conn.commit()
cur.close()
conn.close()

