import socket
import sys
import thread
if len(sys.argv) <= 1: 
	print 'Usage: "python S.py port"\n[port] : It is the port of the Proxy Server'
	sys.exit(2)

# Server socket created, bound and starting to listen
Serv_Port = int(sys.argv[1]) # sys.argv[1] is the port number entered by the user
Serv_Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.socket function creates a socket.

# Prepare a server socket
print "Starting server ...."
Serv_Sock.bind(('', Serv_Port))
Serv_Sock.listen(5) # Maximum 5 requests in a queue

cache={}

def request(splitMessage, Cli_Sock):
	Req_Type = splitMessage[0]
	Req_path = splitMessage[1]
	print "Request is ", Req_Type, " to URL : ", Req_path

	#Searching available cache if url exists
	if Req_path in cache:
		print "Page Present in Cache\n"

		#Proxy Server Will Send Data
		for i in range(0, len(cache[Req_path])):
			print (cache[Req_path][i])
			Cli_Sock.send(cache[Req_path][i])
		print "Reading page from cache\n"

	else:
		print "Page Doesn't Exists In Cache\n Fetching page from server"
		serv_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host_name=Req_path
		if 'http' in Req_path :
			host_name = (Req_path.split('//')[1]+'/').split('/')[0]
		print "##",Req_path
		host_name1=host_name
		portno=int(Req_path.split(':')[2][0:4])
		print portno
		if 'iiit.ac.in' not in host_name:
		   host_name='proxy.iiit.ac.in'
		   portno=8080
		try:
			serv_proxy.connect(('localhost', portno))
			print 'Socket connected to port '+str(portno)+' of the host'
			fileobj = serv_proxy.makefile('r', 0)
			fileobj.write("GET " + "./"+ " HTTP/1.0\n\n")

			# Read the response into buffer
			buffer = fileobj.readlines()
			
			# add page into cache
			cache[Req_path]=buffer
			
			for i in range(0, len(buffer)):
				Cli_Sock.send(buffer[i])
			
		except Exception,e:
			print Cli_Sock.send("<h1>"+str(e)+"</h1>")

	Cli_Sock.close()
while True:
	# Start receiving data from the client
	print 'Accepting connection\n'
	Cli_Sock, addr = Serv_Sock.accept() # Accept a connection from client
	message = Cli_Sock.recv(1024) #Recieves data from Socket
	print message

	splitMessage = message.split()
	if len(splitMessage) <= 1:
		continue

	thread.start_new_thread(request,(splitMessage, Cli_Sock))