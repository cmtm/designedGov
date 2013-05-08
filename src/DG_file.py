import yaml
import Crypto.Hash.SHA512
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5


import User

class DG_file:
	def __init__(self, dG_type = "", authorId = 0, content = None):
		self.tree = {"dG_type": dG_type, "content": content, "author ID" : authorId}	
	
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
		
	#static factory
	def deserialize(serialized):
		serialized = yaml.safe_load(serialized)
		new_dG = DG_file(serialized["dG_type"], serialized["author ID"], serialized["content"])
		
		if "signature" in serialized:
			new_dG["signature"] = serialized["signature"]
			
		if "author key" in serialized:
			new_dG["author key"] = serialized["author key"]
		
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
