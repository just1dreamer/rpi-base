import serial
import mariadb
import time
import datetime
import sys
import socket
import os

user = "rem_acc"
password = "remotacc"
host ="192.168.1.111"
port = 3306
database = "lot_data"
greenhouse_ip = "192.168.1.185"
foilhouse_ip = "192.168.1.184"

greenh = [b'0',b'0',b'0']
foilh = [b'0',b'0',b'0']

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(8)

class Module:
	def __init__(self, address, port):
		self.address = address
		self.port = port

greenhouse = Module(greenhouse_ip, 8888)
foilhouse = Module(foilhouse_ip, 8888)

nextupdate = datetime.datetime.now()
nextsave = datetime.datetime.now()

def eventHandler(event, ids):
	now = datetime.datetime.now()
	today = datetime.date.today()
	current_time = now.strftime("%H:%M:%S")
	#print(f"Current time {today}, {current_time}")
	sql = "INSERT INTO event (date, time, area, message, value, limi, prio) VALUES (?, ?, ?, ?, ?, ?, ?)"
	if event == "connect" and ids == 0:
		message = "New connection to database server"
		val = (today, current_time, 'Server', 'New connection to database', '0', '0', '1')
		cur.execute(sql, val)
		print(message)
	if event == "error" and ids == 1:
		message = "Greenhouse module error. Connection timeout."
		print(message)
	if event == "error" and ids == 2:
		message = "Foilhosue module error. Connection timeout."
		print(message)
	if event == "high" and ids == 11:
		message = "Greenhouse temp 1 reach high limit!"
		val = (today, current_time, 'Greenhouse', message, '0', '0', '0')
		cur.execute(sql, val)
		print(message)

try:
	conn = mariadb.connect(user = user, password = password, host = host, port = port, database = database)
	cur = conn.cursor()
	print("Database connection succesful!")
	eventHandler("connect", 0)
except mariadb.Error as e:
	print(f"Error connecting: {e}")
	sys.exit(1)

def UDPread(address, port, data):
	try:
		#print(f"{address} {port} {data}")
		sock.sendto(data, (address, port))
		recv, addr = sock.recvfrom(1024)
		#print(f"{recv}")
		#time.sleep(1)
	except socket.timeout:
		#print(f"Connection timout at {address}")
		recv = b'00.00'
	except socket.error as error:
		print(os.strerror(error.errno))
	if recv == b'nan':
		recv = b'00.00'
	return recv

def moduleUpdate(name, address, port):
	name[0] = UDPread(address, port, b'a')
	name[1]= UDPread(address, port, b'b')
	name[2] = UDPread(address, port, b'c')

def checkSetlist(temp):

	cur.execute("SELECT MAX(id) FROM setlist")
	res = cur.fetchone()
	for i in range(4,int(res[0])):
		cur.execute("SELECT * FROM setlist WHERE id= " + str(i))
		res = cur.fetchone()

		#print(res[0], res[1], res[2], res[3], res[4], res[5], res[6])
		if res[3] == "gh":
			if "temp" in res[4]:
				if float(temp) >= float(res[5]):
					eventHandler("high", 11)

while True:

	#print("Starting program")
	now = datetime.datetime.now()
	today = datetime.date.today()
	current_time = now.strftime("%H:%M:%S")
	#print(f"Current time {today}, {current_time}")



	if nextupdate <= now:
		#print("Getting data from modules")
		moduleUpdate(greenh, greenhouse.address, greenhouse.port)
		moduleUpdate(foilh, foilhouse.address, foilhouse.port)
		cur = conn.cursor()
		cur.execute("UPDATE single SET date = ?, time = ?, temp_in =?, temp_out = ?, humidity_in = ?, humidity_out = ?, kazan1 = ?, kazan2 = ?, foil1 = ?, foil2 = ?, foilhum = ?, gh1 = ?, gh2 = ?, ghhum = ? WHERE id = 1", (today, current_time, 0, 0, 0, 0, 0, 0, foilh[0], foilh[1], foilh[2], greenh[0], greenh[1], greenh[2]))       
		conn.commit()
		nextupdate = now + datetime.timedelta(seconds = 60)

		os.system('clear')

		print("========================================================================================")
		print("= " + f"Last updated {today}, {current_time}" + "                                                    =")
		print("========================================================================================")
		print("=               GREENHOUSE                =                 FOILHOUSE                  =")
		print("=       "+ greenh[0].decode("utf-8") +"˚C  "+greenh[1].decode("utf-8")+"˚C   "+greenh[2].decode("utf-8")+"%         =        "+foilh[0].decode("utf-8")+"˚C    "+foilh[1].decode("utf-8")+"˚C   "+foilh[2].decode("utf-8")+"%         =")
		print("========================================================================================")
		print("= " + f"Next saving to Archive {nextsave}" + "                                    =")
		print("========================================================================================")

	if nextsave <= now:
		#print("Archive")
		cur = conn.cursor()
		cur.execute("INSERT INTO archive (date,time,temp_in,temp_out, humidity_in, humidity_out,kazan1, kazan2, foil1, foil2, foilhum,gh1,gh2,ghhum) VALUES ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(today, current_time, 0, 0, 0, 0, 0, 0, foilh[0], foilh[1], foilh[2], greenh[0], greenh[1], greenh[2]))
		conn.commit()
		nextsave = now + datetime.timedelta(seconds = 300)
        
	
	
	
	#print("Check Settings")
	#checkSetlist(foilh[0])
	#print("Update data to database")
	
