class User:
	idLength = 64
	keyLength = 1024
	
	def __init__(self, idNum = None, cert = None, privKey = None):
		self.idNum = idNum
		self.cert = cert
		self.privKey = privKey
"""
	def getIdHex(self):
		return hex(self.idNum).zfill(self.idLength/4)
"""
