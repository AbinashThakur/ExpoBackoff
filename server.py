import requests
import backoff
import datetime as dt
from datetime import datetime
from backoff import on_predicate, constant
from backoff._jitter import full_jitter
import json

def get_status(data):
	try:
		res = status(data)
		
	except Exception as e:
		return 'Error, 500'
	return 'ok, 204'


def fatal_code(e):
    print("Fatal Error !!!")
    raise Exception("Error")
# max try provided here is 10 to show all possible response
@on_predicate(backoff.expo, max_tries=10, on_giveup=fatal_code, jitter=full_jitter)
def status(data):
	final_data = json.loads(data)
	currTime = int(dt.datetime.now().strftime("%s")) * 1000

	fstatus = False
	print("trying to fetch data...")
	
	if final_data["deltatime"] < currTime:
		fstatus = True
		print("True returned")
		return fstatus
	print("False returned")
	return fstatus

