import socket, ssl 
import pymongo
import dgobs
import pdb


class Host(object):

	def __init__(self, port, ca_certs, certfile, keyfile, template = None, dbName=None, collection = None):
		self.bindsocket = socket.socket()
		self.bindsocket.bind(('localhost', port))
		self.bindsocket.listen(5)
		self.ca_certs = ca_certs
		self.certfile = certfile
		self.keyfile = keyfile
		if template != None:
			f = open(template, 'r')
			self.template = dgobs.Template.deserialize(f.read())
			f.close()
		if dbName != None:
			self.dbCollection = pymongo.MongoClient()[dbName][collection]
		else:
			self.dbCollection = None
		
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
				self.handleClient(connstream)
			finally:
				connstream.shutdown(socket.SHUT_RDWR)
				connstream.close()
	
	def handleClient(self, connstream):
		userID = connstream.getpeercert()['subject'][0][0][1]
		# TODO: develop better implementation than a max receive size
		data = connstream.recv(16384)
		req = dgobs.Request.deserialize(data)
		resp = dgobs.Response()
		for r in req.getReqs():
			try:
				if r['type'] == 'read' or r['type'] == 'write':
					if r['data path'] == '':
						path = []
					else:
						path = r['data path'].split('.')
					if r['type'] == 'read':
						resp.addRead(*self.handleRead(userID, path))
					else: # r['type'] == 'write'
						resp.addWrite(*self.handleRead(userID, path, newVal))
				elif r['type'] == 'action':
					resp.addAction(*self.handleRead(userID, r['name'], r['parameters']))
				else:
					resp.addUnrecognized()
			except Exception as e:
				raise e
				resp.addError() 
		connstream.sendall(resp.serialize())
		
	def handleRead(self, userID, path):
		
		def traverseTree(root, path):
			if len(path) == 0:
				return root
			else:
				return self.traverseTree(root[path[0]], path[1:])
				
		
		if self.template.checkPolicy(path, 'r'):
			entry = self.dbCollection.find_one({'_id': userID.lower()})
			# suppress projection to get working with root directory
			# TODO: fix this
			# entry = self.dbCollection.find_one({'_id': userID.lower()}, {'.'.join(path):1, '_id': 0})

			return (True, traverseTree(entry, path))
		else:
			return (False, None, "data doesn't exist or can't be read")
				
	def handleWrite(self, userID, path, newVal):
		if self.template.checkPolicy(path, 'w'):
			self.dbCollection.update({'_id': userID}, {'$set': {'.'.join(path):newVal}})
		else:
			return (False, None, "data doesn't exist or can't be written")
	
	def handleAction(self, userID, name, actionArgs):
		pass
