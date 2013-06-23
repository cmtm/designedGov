import socket, ssl
import sqlite3
import dgobs


class Host(object):
	readables = {}
	writables = {}

	def __init__(self, port, ca_certs, certfile, keyfile, dbFile=None, table = None):
		self.bindsocket = socket.socket()
		self.bindsocket.bind(('localhost', port))
		self.bindsocket.listen(5)
		self.ca_certs = ca_certs
		self.certfile = certfile
		self.keyfile = keyfile
		if dbFile != None:
			self.dbConn = sqlite3.connect(dbFile)
			self.table = table
		else:
			self.dbConn = None
		
	def listenForRequests(self):
		while True:
			newsocket, fromaddr = self.bindsocket.accept()
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
	
	def handleClient(self, connstream):
		userID = connstream.getpeercert()['subject'][0][0][1]
		# TODO: develop better implementation than a max recieve size
		data = connstream.recv(16384)
		req = dgobs.Dgob.deserialize(data)
		resp = Response()
		for r in req.getReqs():
			try:
				if r['type'] == 'read':
					resp.addRead(*self.handleRead(userID, r['data_path']))
				elif r['type'] == 'write':
					resp.addWrite(*self.handleRead(userID, r['data_path'], newVal))
				elif r['type'] == 'action':
					resp.addAction(*self.handleRead(userID, r['name'], r['parameters']))
				else:
					resp.addUnrecognized()
			except Exception:
				resp.addError() 
		
		
		
	def handleRead(self, userID, path):
		column = self.readables.get(path, None)
		if column == None:
			return (False, "data doesn't exist or can't be read")
		else:
			row = self.dbConn.execute('SELECT {} FROM {} WHERE userID = {}'.  \
			                format(column, self.table, userID)).fetchone()
			if row == None:
				return (False, "Couldn't find data for this client")
			else:
				return (True, None, row[0])
				
	def handleWrite(self, userID, path, newVal):
		column = self.writeables.get(path, None)
		if column == None:
			return (False, "data doesn't exist or can't be written")
		else:
			self.dbConn.execute('UPDATE {} SET {}={} WHERE userID = {}'.  \
			        format(self.table, column, newVal, userID))
			row = self.dbConn.execute('SELECT {} FROM {} WHERE userID = {}'.  \
			                format(column, self.table, userID)).fetchone()
			if row == None or row[0] != newVal:
				return (False, "Couldn't write data for this client")
			else:
				return (True,)
	
	def handleAction(self, userID, name, actionArgs):
		pass
