import yaml
import Crypto.Hash.SHA512
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5

import User

class WrongFileType(Exception):
	pass

class Dgob(object):
	
	typeName = None
	
	
	def __init__(self, authorId = 0, content = None):
		# self.typeName should really be <className>.typeName
		# this would require overriding __new__. I might do this later
		self.tree = {"dG_type": self.typeName, "content": content, "author ID" : authorId}	
	
	def sign(self, privateKey):

		# only sign content or dG file
		h = Crypto.Hash.SHA512.new(yaml.dump(self.tree["content"]).encode('utf-8'))
		
		key = Crypto.PublicKey.RSA.importKey(privateKey)
		signer = Crypto.Signature.PKCS1_v1_5.new(key)
		self.tree["signature"] = signer.sign(h)
			
	def addPublicKey(self, publicKey):
		self.tree["author key"] = publicKey
	
	def verifySignature(self, publicKey = None):
		if publicKey == None:
			# might throw more specific exception if author key doesn't exist
			publicKey = self.tree["author key"]
		h = Crypto.Hash.SHA512.new(yaml.dump(self.tree["content"]).encode('utf-8'))
		key = Crypto.PublicKey.RSA.importKey(publicKey)
		verifier = Crypto.Signature.PKCS1_v1_5.new(key)
		
		return verifier.verify(h, self.tree["signature"])
	
	
	
	def serialize(self):
		return yaml.dump(self.tree)
		
	@classmethod
	def deserialize(cls, serialized):
		tree = yaml.safe_load(serialized)
		
		if cls.typeName != None and cls.typeName != tree["dG_type"]:
			raise WrongFileType()
		
		new_dG = cls(tree["author ID"], tree["content"])
		
		if "signature" in serialized:
			new_dG["signature"] = tree["signature"]
			
		if "author key" in serialized:
			new_dG["author key"] = tree["author key"]
		
		return new_dG


class Request(Dgob):
	
	typeName = "request"
	
	def __init__(self, authorId = 0, content = []):
		super(Request, self).__init__(authorId, content)
	
	def addRead(self, data_path):
		self.tree["content"].append({"type": "read", "data path": data_path})
		
	def addWrite(self, data_path, new_value):
		self.tree["content"].append({"type": "write", "data path": data_path, "new value": new_value})
	
	def addAction(self, action_name, parameters = {}):
		self.tree["content"].append({"type": "action call", "action name": action_name, "parameters": parameters})
	
	def getReqs(self):
		return self.tree['content']
	

class Response(Dgob):
	
	typeName = "response"
	
	def __init__(self, authorId = 0, content = []):
		super(Response, self).__init__(authorId, content)
	
	def addRead(self, wasSuccessful, failureCause = None, valueRead = None):
		self.tree["content"].append({"type": "read", "was successful": wasSuccessful})
		if wasSuccessful:
			self.tree["content"][-1]["value read"] = valueRead
		else:
			self.tree["content"][-1]["failure cause"] = failureCause
		
	def addWrite(self, wasSuccessful, failureCause = None):
		self.tree["content"].append({"type": "write", "was successful": wasSuccessful})
		if not wasSuccessful:
			self.tree["content"][-1]["failure cause"] = failureCause
		
	def addActionItem(self, response):
		self.tree["content"].append({"type": "action call", "was successful": wasSuccessful})
		if wasSuccessful:
			self.tree["content"][-1]["returned"] = returned
		else:
			self.tree["content"][-1]["failure cause"] = failureCause

	def getResps(self):
		return self.tree['content']
