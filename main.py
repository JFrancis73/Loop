from fastapi import FastAPI, staticfiles, Response
import os
import time
import hashlib
import subprocess

app = FastAPI()

app.mount("/static", staticfiles.StaticFiles(directory="."), name="static")

@app.get("/")
def read_root():
    return {"Hey":"Lol"}

@app.get("/get_report/{report_id}")
def read_report(report_id: str):
    with open("logs.txt",'r') as log_file:
        logs = log_file.readlines()
        if report_id +" Complete\n" in logs:
            with open(f"{report_id}.csv", "rb") as f:
                file_data = f.read()
            response = Response(content=file_data, media_type="text/csv")
            response.headers["Content-Disposition"] = f"attachment; filename={report_id}.csv"
            return response
        elif report_id +" Running\n" in logs:
            return {"status":"running"}
        else:
            return {"Error":"Invalid Report id"}

@app.get("/trigger_report")
def make_report():
	report_id = hashlib.md5(str(time.time()).encode()).hexdigest()
	with open("logs.txt","a") as log_file:
		log_file.write(report_id+" Running\n")
	subprocess.Popen(["python", "generate_report.py", report_id+".csv"])
	return {"Report_Id":report_id}		