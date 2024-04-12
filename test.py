with open("logs.txt",'r') as log_file:
	logs = log_file.readlines()
	print(logs)
	if "7ee9d05f3d1e7b13811d066c1b4157af Complete\n" in logs:
		status = "complete"
	elif "7ee9d05f3d1e7b13811d066c1b4157af Running\n" in logs:
		status = "running"
	else:
		status = "invalid report id"
print(status)