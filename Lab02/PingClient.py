#python 2.7.12
import sys
import os
import socket
import time

if (len(sys.argv) != 3):
	print("Require Arguments: Host, Port")
	os._exit(0)

host = sys.argv[1]
port = (int)(sys.argv[2])

#set socket 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(1)

#connect host
s.connect((host, port))

total = 0
sumRTT = 0
maxRTT = 0
minRTT = 1000

#send 10 ping requests to server
for sequence_number in range(0, 10):
	#send requests
	now_time = time.time()
	ping_message = "PING" + " " + str(sequence_number) + " " + str(now_time) + "\r\n"
	s.sendto(ping_message, (host, port))
	#receive response
	try:
		data, address = s.recvfrom(1024)
		recv_time = time.time()
		diff = recv_time - now_time
		rtt = (int)(1000 * diff + 0.5)
		# calculate info
		total = total + 1
		sumRTT = sumRTT + rtt
		if (rtt > maxRTT):
		    maxRTT = rtt
		if (rtt < minRTT):
		    minRTT = rtt 
		print("Ping to " + host + ", seq = " + str(sequence_number) + ", rtt = " + str(rtt) + "ms")
	except socket.timeout:
		print("Ping to " + host + ", seq = " + str(sequence_number) + ", time out")
	time.sleep(1)
	
	# print all
print("Average rtt: " + str(sumRTT/total) + "ms Max rtt: " + str(maxRTT) + "ms Min rtt: " + str(minRTT) + "ms")


s.close()


