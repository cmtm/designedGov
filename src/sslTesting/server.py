import socket, ssl

def deal_with_client(connstream):
	data = connstream.recv(4096)
	print(connstream.getpeercert()['subject'][0][0][1])
	print(data)
	connstream.sendall("""Hi to you too!""")

bindsocket = socket.socket()
bindsocket.bind(('localhost', 10023))
bindsocket.listen(5)

# When one did, you'd call accept() on the socket to get the new socket from the other end, and use wrap_socket() to create a server-side SSL context for it:

while True:
	newsocket, fromaddr = bindsocket.accept()
	connstream = ssl.wrap_socket(newsocket,
								 server_side=True,
								 ca_certs="../keysAndCerts/certificates/myCA.crt",
								 certfile="../keysAndCerts/certificates/host1.crt",
								 keyfile="../keysAndCerts/keys/host1.pem",
								 ssl_version=ssl.PROTOCOL_TLSv1,
								 cert_reqs=ssl.CERT_REQUIRED)
	try:
		deal_with_client(connstream)
	finally:
		connstream.shutdown(socket.SHUT_RDWR)
		connstream.close()

# Then you'd read data from the connstream and do something with it till you are finished with the client (or the client is finished with you):


