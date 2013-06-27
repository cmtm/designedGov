import yaml
import Crypto.Hash.SHA512
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5

import pdb

import User

class WrongFileType(Exception):
	pass

class Dgob(object):
	
	typeName = None
	
	
	def __init__(self, authorId = 0, content = None):
		# self.typeName should really be <className>.typeName
		# this would require overriding __new__. I might do this later
		self.tree = {"dgob type": self.typeName, "content": content, "author ID" : authorId}	
	
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
		tree = yaml.load(serialized)
		
		if cls.typeName != None and cls.typeName != tree["dgob type"]:
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
	
	def addRead(self, data_path, otherUserID = None):
		self.tree["content"].append({"type": "read", "data path": data_path})
		if otherUserID != None:
			self.tree["content"][-1]['other userID'] = otherUserID
			
	def addWrite(self, data_path, new_value, otherUserID = None):
		self.tree["content"].append({"type": "write", "data path": data_path, "new value": new_value})
		if otherUserID != None:
			self.tree["content"][-1]['other userID'] = otherUserID
			
	def addAction(self, action_name, parameters = {}, otherUserID = None):
		self.tree["content"].append({"type": "action call", "name": action_name, "parameters": parameters})
		if otherUserID != None:
			self.tree["content"][-1]['other userID'] = otherUserID
			
	def getReqs(self):
		return self.tree['content']
	

class Response(Dgob):
	
	typeName = "response"
	
	def __init__(self, authorId = 0, content = []):
		super(Response, self).__init__(authorId, content)
	
	def addRead(self, wasSuccessful, valueRead = None, failureCause = None):
		self.tree["content"].append({"type": "read", "was successful": wasSuccessful})
		if wasSuccessful:
			self.tree["content"][-1]["value read"] = valueRead
		else:
			self.tree["content"][-1]["failure cause"] = failureCause
		
	def addWrite(self, wasSuccessful, failureCause = None):
		self.tree["content"].append({"type": "write", "was successful": wasSuccessful})
		if not wasSuccessful:
			self.tree["content"][-1]["failure cause"] = failureCause
		
	def addAction(self, wasSuccessful, failureCause = None, returned = ""):
		self.tree["content"].append({"type": "action call", "was successful": wasSuccessful})
		if wasSuccessful:
			self.tree["content"][-1]["returned"] = returned
		else:
			self.tree["content"][-1]["failure cause"] = failureCause

	def addUnrecognized(self):
		self.tree["content"].append({"type": "unrecognized"})
	
	def addError(self, message = "Unknown Error"):
		self.tree['content'].append({'type': 'error', 'message':message})
	
	def getResps(self):
		return self.tree['content']

class Template(Dgob):
	typeName = "template"
	
	def __init__(self, authorId = 0, orgName = "", shortDesc = "", longDesc = None, dataMap = {'children': {}}, actions = {}):
		templateContent = {'organization name': orgName,
		                   'short description': shortDesc, 
		                   'data tree': dataMap, 
		                   'actions': actions}
		if longDesc != None:
			templateContent['long description'] = longDesc
			
		super(Template, self).__init__(authorId, content=templateContent)
	# path is a list of nodes needed to be traversed
	def addData(self, path, dataType, isOptional = False, accessPolicy = None, description=None, children = {}):
		newItem = {'type': dataType, 'is optional': isOptional}
		if accessPolicy != None:
			newItem['access policy'] = accessPolicy
		if description != None:
			newItem['description'] = description
		if dataType == 'inode':
			newItem['children'] = children
		
		parent = self.getNode(self.tree['content']['data tree'], path[:-1])
		parent['children'][path[-1]] = newItem
	
	def getNode(self, root, path):
		if len(path) == 0:
			return root
		else:
			return self.getNode(root['children'][path[0]], path[1:])

	def checkPolicy(self, path, policy, otherUser = None):
		# TODO: support other user
		# if no policy is exist, default behavior is to allow owner to read but not write
		node = self.getNode(self.tree['content']['data tree'], path)
		if 'access policy' not in node:
			return policy == 'r'
		elif (policy in node['access policy']):
			return True
		else:
			return False
		
	# policy can be any item from this list: ['', 'r', 'w', 'rw']
	def setAccessPolicy(self, path, user, policy):
		n = self.getNode(self.tree['content']['data tree'], path)

		if policy == '':
			del n['access policy'][user]
		else:
			n['access policy'][user] = policy
	
		
