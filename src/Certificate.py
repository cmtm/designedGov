from DG_file import DG_file

class Certificate(DG_file):
	def __init__(self, authorId = 0, content = {}):
		super().__init__("certificate", authorId, content)
	
	def setUser(self, userId, publicKey, validFrom = None, ValidTo = None, name = None, other = None):
		self.tree["content"]= {"user ID": userId, "public key": publicKey}
		if name != None:
			self.tree["content"]["name"] = name
			
		if validFrom != None:
			self.tree["content"]["valid from"] = validFrom
			
		if ValidTo != None:
			self.tree["content"]["valid to"] = ValidTo		
		
		if other != None:
			self.tree["content"].update(other)
	
		
