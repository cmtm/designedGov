import socket, ssl
import sqlite3
import dgobs


class Host(Object):

	def __init__(self, port, ca_certs, certfile, keyfile, dbFile=None):
		self.bindsocket = socket.socket()
		self.bindsocket.bind(('localhost', port))
		self.bindsocket.listen(5)
		self.ca_certs = ca_certs
		self.certfile = certfile
		self.keyfile = keyfile
		if dbFile != None:
			self.dbConn = sqlite3.connect(dbfile)
		else:
			self.dbConn = None
		
	def listenForRequests(self):
		while True:
		newsocket, fromaddr = bindsocket.accept()
		connstream = ssl.wrap_socket(newsocket,
									 server_side=True,
									 ca_certs=self.ca_certs,
									 certfile=self.certfile,
									 keyfile=self.keyfile,
									 ssl_version=ssl.PROTOCOL_TLSv1,
									 cert_reqs=ssl.CERT_REQUIRED)
		try:
			handleClient(connstream)
		finally:
			connstream.shutdown(socket.SHUT_RDWR)
			connstream.close()
	
	def handleClient(connstream):
		# userID = connstream.getpeercert()['subject'][0][0][1]
		# data = connstream.recv(16384)
		pass
		
		
