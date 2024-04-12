import sys
import psycopg2
import csv
from datetime import datetime,timedelta
import pytz

conn = psycopg2.connect(host="localhost", dbname="Loop", user="postgres", password="postgres", port=5432)

cur = conn.cursor()

cur.execute("Select * from store_status;")
stats = cur.fetchall()
current_time = "2023-01-01 00:00:00.634899 UTC"
for i in stats:
	if i[2] > current_time:
		current_time = i[2]
#print(current_time)

def convert_to_utc(time,zone):

  local_timezone = pytz.timezone(zone)

  local_time = datetime.strptime(time, "%H:%M:%S").replace(tzinfo=local_timezone)

  utc_time = local_time.astimezone(pytz.utc)

  return utc_time.strftime('%H:%M:%S UTC')

def uptime_hour(id,time):
	time = datetime.strptime(time.split()[1].split(".")[0],"%H:%M:%S")
	cur.execute(f"Select timestamp,status from store_status where store_id={id}")
	obs = cur.fetchall()
	last_hour = time - timedelta(hours=1)

	for i in obs:
		observation = datetime.strptime(i[0].split()[1].split(".")[0],"%H:%M:%S")
		if observation > last_hour and observation < time:
			if i[1] == "active":
				uptime = int((time - observation).total_seconds()/60)
				return uptime,60-uptime
			else:
				uptime = int((observation - last_hour).total_seconds()/60)
				return uptime, 60-uptime

def uptime_day(id,date,zone):
	uptime=0
	day = date.weekday()
	cur.execute(f"Select start_time,end_time from menu_hours where store_id={id} and day={day};")
	business_hours = [[convert_to_utc(i[0],zone),convert_to_utc(i[1],zone)] for i in cur.fetchall()]
	if business_hours == []:
		business_hours = [['00:00:00 UTC','23:59:59 UTC']]
	open_time = datetime.strptime(business_hours[0][0],"%H:%M:%S UTC")
	close_time = datetime.strptime(business_hours[0][1],"%H:%M:%S UTC")
	cur.execute(f"Select timestamp from store_status where store_id={id} and status='active';")
	observations = cur.fetchall()
	for i in observations:
		time = datetime.strptime(i[0].split()[1].split(".")[0],"%H:%M:%S")
		if open_time < close_time:
			if time > open_time and time < close_time and date == datetime.strptime(i[0].split()[0],"%Y-%m-%d"):
				uptime +=1
		else:
			if (time > open_time or time < close_time) and date == datetime.strptime(i[0].split()[0],"%Y-%m-%d"):
				uptime += 1

	business_hours = int((close_time - open_time).total_seconds() / 3600)%25
	if uptime > business_hours:
		uptime = business_hours
	downtime = int(business_hours-uptime)
	return uptime,downtime

def uptime_week(id,date,zone):
	uptime,downtime = 0,0
	for i in range(6):
		temp = uptime_day(id,date-timedelta(days=i),zone)
		uptime += temp[0]
		downtime += temp[1]
	return uptime,downtime

chicago_time_str = "00:00:00"
converted_utc_time = convert_to_utc(chicago_time_str,"America/Chicago")
print(f"Chicago time: {chicago_time_str} converted to UTC: {converted_utc_time}")

cur.execute("Select store_id from store_status")
ids = [i[0] for i in cur.fetchall()]
print(len(ids))
ids = list(set(ids))
print(len(ids))

report_name = sys.argv[1]
with open(report_name, 'w', newline='') as csvfile:
	csv_writer = csv.writer(csvfile)
	csv_writer.writerow(['store_id', 'uptime_last_hour(in minutes)', 'uptime_last_day(in hours)', 'update_last_week(in hours)', 'downtime_last_hour(in minutes)', 'downtime_last_day(in hours)', 'downtime_last_week(in hours)'])
	for id in ids:
		date = datetime.strptime("2023-01-25","%Y-%m-%d")
		cur.execute(f"Select timezone from timezones where store_id={id}")
		zone = cur.fetchall()
		zone = "America/Chicago" if zone == [] else zone[0][0]
		up_hour,down_hour = uptime_hour(id,current_time)
		up_day,down_day = uptime_day(id,date,zone)
		up_week,down_week = uptime_week(id,datetime.strptime(current_time.split()[0],"%Y-%m-%d"),zone)
		csv_writer.writerow([id,up_hour,up_day,up_week,down_hour,down_day,down_week])
		
with open("logs.txt",'a') as log_file:
	logfile.write(log_file.write(report_name.split(".")[0]+" Complete\n"))
def convert_to_utc(time,zone):

  local_timezone = pytz.timezone(zone)

  local_time = datetime.strptime(time, "%H:%M:%S").replace(tzinfo=local_timezone)

  utc_time = local_time.astimezone(pytz.utc)

  return utc_time.strftime('%H:%M:%S UTC')

"""
def uptime_day(id,date,zone):
	uptime=0
	day = date.weekday()
	cur.execute(f"Select start_time,end_time from menu_hours where store_id={id} and day={day};")
	business_hours = [[convert_to_utc(i[0],zone),convert_to_utc(i[1],zone)] for i in cur.fetchall()]
	cur.execute(f"Select timestamp from store_status where store_id={id} and status='active';")
	observations = cur.fetchall()
	for i in observations:
		if i[0].split()[1] > business_hours[0][0] and i[0].split()[1] < business_hours[0][1] and date == datetime.strptime(i[0].split()[0],"%Y-%m-%d"):
			uptime +=1
	return uptime

def uptime_day(id,date,zone):
	uptime=0
	day = date.weekday()
	cur.execute(f"Select start_time,end_time from menu_hours where store_id={id} and day={day};")
	business_hours = [[convert_to_utc(i[0],zone),convert_to_utc(i[1],zone)] for i in cur.fetchall()]
	cur.execute(f"Select timestamp from store_status where store_id={id} and status='active';")
	observations = cur.fetchall()
	for i in observations:
		if i[0].split()[1] > business_hours[0][0] and i[0].split()[1] < business_hours[0][1] and date == datetime.strptime(i[0].split()[0],"%Y-%m-%d"):
			uptime +=1
	business_hours = ((datetime.strptime(business_hours[0][1],"%H:%M:%S UTC") - datetime.strptime(business_hours[0][0],"%H:%M:%S UTC")).total_seconds() / 3600)
	downtime = int(business_hours-uptime)
	return uptime,downtime

date = datetime.strptime("2023-01-25","%Y-%m-%d")
day = date.weekday()
id = 3159131636399983291
cur.execute(f"Select timezone from timezones where store_id={id}")
zone = cur.fetchall()
zone = "America/Chicago" if zone == [] else zone[0][0]
cur.execute(f"Select * from store_status where store_id={3159131636399983291}")
x=[i for i in cur.fetchall() if date == datetime.strptime(i[2].split()[0],"%Y-%m-%d")]
for i in x:
	print(i)
cur.execute(f"Select start_time,end_time from menu_hours where store_id={3159131636399983291} and day={day};")
business_hours = [[convert_to_utc(i[0],zone),convert_to_utc(i[1],zone)] for i in cur.fetchall()]
print(business_hours)
print("Uptime day: ",uptime_day(id,date,zone))
"""
