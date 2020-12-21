import pika
from server import get_status

def rbmq_receiver():

	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='task_queue', durable=True)
	
	def callback(ch, method, properties, body):
	    
	    cmd = body.decode()

	    if cmd:
	    	print("received {}".format(cmd))
	    	print(get_status(cmd))
	    ch.basic_ack(delivery_tag=method.delivery_tag)
	    
	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(queue='task_queue', on_message_callback=callback)
	channel.start_consuming()
	

rbmq_receiver()