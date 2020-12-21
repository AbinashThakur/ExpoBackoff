from flask import Flask, request
import json
import pika
import time
import uuid
import datetime as dt

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def dummy_api():
	if request.method == 'POST':
		pid = uuid.uuid4().hex[:10]
		tss = dt.datetime.now()
		nextTime = dt.datetime.now() + dt.timedelta(minutes = 1)
		# print(pid + " Current request @ " + tss.strftime("%Y-%m-%d %H:%M:%S") + " Next request @ " + nextTime.strftime("%Y-%m-%d %H:%M:%S"))
		x = {"pid" : pid, "deltatime" : int(nextTime.strftime("%s"))*1000}
		# x = {"pid" : pid, "deltatime" : nextTime.timestamp()*100000}
		content = json.dumps(x)
		# content = pid + " Current request @ " + tss.strftime("%Y-%m-%d %H:%M:%S") + " Next request @ " + nextTime.strftime("%Y-%m-%d %H:%M:%S")
		result = rbmq_sender(content)
		if result:
			print("Sent " + content)
			return content

def rbmq_sender(data):
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='task_queue', durable=True)
	channel.basic_publish(exchange='',
						  routing_key='task_queue',
						  body=data,
						  properties=pika.BasicProperties(delivery_mode=2,	
						  ))
	connection.close()
	return data