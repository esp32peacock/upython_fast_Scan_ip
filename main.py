import network
import socket
import urequests
import time
import machine
import select

station = network.WLAN(network.STA_IF)
if not station.isconnected():
	print('connecting to network...')
	station.active(True)
	station.connect('phloenlom_2.4GHz', '248248248')
	while not station.isconnected():
		pass

url = 'http://192.168.1.28/scan'


print(station.ifconfig())
try:
	response = urequests.get(url)
	print(response.text)
except:
	pass

def do_client(ip, port):
	addr = socket.getaddrinfo(ip, port)[0][-1]
	try:
		s = socket.socket()
		s.setblocking(False)
		s.connect(addr)
	except:
		pass
	p = select.poll()
	p.register(s, select.POLLERR | select.POLLOUT | select.POLLIN | select.POLLHUP)
	for event in p.poll(100):
		# print("event:", event)
		if event[1] & select.POLLOUT:
			# print("new connection")
			s.close()
			return ip
	s.close()
	return 'failed'

for i in range(2,255):
	url = '192.168.1.'+str(i)
	print(url)
	cb = do_client(url, 80)
	if cb!='failed':
		try:
			response = urequests.get('http://'+cb+'/scan')
			print(response.text)
		except:
			pass

