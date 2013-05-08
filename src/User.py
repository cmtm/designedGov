class User:
	idLength = 64
	keyLength = 1024
	
	def __init__(self, userId = 0, userPublicKey = 0, userPrivateKey = 0):
		self.Id = userId
		self.PublicKey = userPublicKey
		self.PrivateKey = userPrivateKey
