from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hey":"Lol"}

@app.get("/{report_id}")
def read_report(report_id: str):
    return {"Report_Id":report_id}
