import socket, ssl
import pdb
from dgobs import *


class ClientWebInterface:
	
	def __init__(self, user, ca_cert="ca_cert.crt"):
		self.user = user
		self.ca_cert = ca_cert

	def makeSocket(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.ssl_sock = ssl.wrap_socket(s,
		                   certfile=self.user.cert,
		                   ca_certs=self.ca_cert,
		                   keyfile=self.user.privKey,
		                   cert_reqs=ssl.CERT_REQUIRED)
	
	def connectTo(self, hostAddress, hostPort, hostUserID):
		self.makeSocket()
		self.ssl_sock.connect((hostAddress, hostPort))
		
		if self.ssl_sock.getpeercert()['subject'][0][0][1] != hostUserID:
			raise InvalidCert("Certificate contains wrong userID")
	
	def close(self):
		self.ssl_sock.close()
	
	
	def sendRequest(self, request):
		self.ssl_sock.sendall(request.serialize())		
		data = self.ssl_sock.recv(16384)
		return Response.deserialize(data)
	
	def sendRequestTo(self, hostAddress, hostPort, hostUserID, request):
		self.makeSocket()
		self.ssl_sock.connect((hostAddress, hostPort))
	
		if self.ssl_sock.getpeercert()['subject'][0][0][1] != hostUserID:
			raise ssl.CertificateError("Certificate contains wrong userID")
		
		self.ssl_sock.sendall(request.serialize())		
		data = self.ssl_sock.recv(16384)
		self.ssl_sock.close()
		return Response.deserialize(data)
