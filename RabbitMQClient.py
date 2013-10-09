#!/usr/bin/env python
import pika, thread, time
import string, random

#change to specified name
def changeName(name=''):
	global nick
	if(name.__len__()==0):
		nick='027-'+generateRandom()
	else:
		nick=name
	return

def generateRandom(size=5,chars=string.ascii_uppercase+string.ascii_lowercase+string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def callback(ch,method,properties,body):
	print body

def startListening(dum1,dum2):
	global channel
	print 'Waiting for channel',ch,'...'
	channel.start_consuming()

def broadcast(msg):
	global chList
	if(chList.__len__()>0):
		global channel
		
		for mem in chList:
			x = mem + 'X'
#			create exchange if not exist
			channel.exchange_declare(exchange=x,type='fanout')
#			create message
			message='['+mem+'] ('+nick+') '+msg
#			publish message
			channel.basic_publish(exchange=x,routing_key='',body=message)
		time.sleep(1)

#constants
hostname='localhost'

#global variables
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
channel=connection.channel()
result=channel.queue_declare(exclusive=True)
queue_name=result.method.queue

nick='027-'+generateRandom()
chList = []

while 1:
	cmd=raw_input('> ')
	param=cmd.split(' ')
	
#	print 'command',param[0]
	if(param[0].strip()=='/EXIT'):
		broadcast('left channel')
		print "program closed"
		break
	elif(param[0].strip()=='/NICK'):
		if(param.__len__()>1):
#			change as param
			changeName(param[1])
			print "Successfully change nickname to",nick
		else:
#			generate random nickname
			changeName()
			print "Generated random nickname: ",nick
	elif(param[0].strip()=='/JOIN'):
		if(param.__len__()>1):
			ch = param[1]

#			insert channel name to list
			if(not chList.__contains__(ch)):
				chList.append(ch)

#			declare exchange, create if not exist
			x = ch + 'X'
			channel.exchange_declare(exchange=x,type='fanout')

#			bind to queue with random name
			channel.queue_bind(exchange=x,queue=queue_name)
			
#			start listening mode on different thread
			channel.basic_consume(callback,queue=queue_name,no_ack=True)
			try:
				thread.start_new_thread(startListening,('',''))
			except Exception, errtxt:
				print errtxt
				print "Error: unable to start thread"
			print "Successfully join to channel",ch
			time.sleep(1)
		else:
			print "Error Format: /JOIN <channelname>"			
	elif(param[0].strip()=='/LEAVE'):
		if(param.__len__()>1):
			ch = param[1]
			if(chList.__contains__(ch)):
#				delete from chList
				idx = chList.index(ch)
				del chList[idx]
				
#				unbind queue
				x = ch + 'X'
				channel.queue_unbind(exchange=x,queue=queue_name)
				print "Successfully left channel",param[1]
			else:
				print "You never join that channel"
		else:
			print "Error Format: /LEAVE <channelname>"
	elif(param[0][0].strip()=='@'):
		if(param.__len__()>1):
			ch = param[0][1:]
			if(chList.__contains__(ch)):
				x = ch + 'X'
#				create exchange if not exist
				channel.exchange_declare(exchange=x,type='fanout')
				
#				create message
				message='['+ch+'] ('+nick+')'
				del param[0]
				for item in param:
					message = message + ' ' + item
				
#				publish message
				channel.basic_publish(exchange=x,routing_key='',body=message)
				print "sent to channel",ch
				time.sleep(1)
			else :
				print "You can't send to channel you've not joined"
		else:
			print "Error Format: NO Text Found. @<channelname> <text>"
	else:
#		not empty parameter
		if(param.__len__()>0):
#			send to all channels joined
			if (chList.__len__()>0):
				msg = ''
				for m in param:
					msg = msg + ' ' + m
				broadcast(msg)
				print "Successfully sent to all joined channel"
			else:
				print "You don't have any channel yet"
		else:
			print "no command found"
