import yaml
import Crypto.Hash.SHA512
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5

import User

class WrongFileType:
	pass

class DG_file(object):
	
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

"""
	def header(self):
		return "---\n"
	
	def footer(self):
		ft = "author ID: {0:{1}x}\n".format(self.authorID, User.idLength/4))
		ft.append("author key: {0:{1}x}\n".format(self.authorID, User.keyLength/4))
		if hasSignature:
			ft.append("signature: {}\n".format(signature))
		ft.append("...")
		return ft
"""
