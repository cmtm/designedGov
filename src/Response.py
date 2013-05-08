from DG_file import DG_file

class Response(DG_file):
	def __init__(self, authorId = 0, content = []):
		super().__init__("response", authorId, content)
	
	def addReadItem(self, wasSuccessful, failureCause = None, valueRead = None):
		self.tree["content"].append({"type": "read", "was successful": wasSuccessful})
		if wasSuccessful:
			self.tree["content"][-1]["value read"] = valueRead
		else:
			self.tree["content"][-1]["failure cause"] = failureCause
		
	def addWriteItem(self, wasSuccessful, failureCause = None):
		self.tree["content"].append({"type": "write", "was successful": wasSuccessful})
		if not wasSuccessful:
			self.tree["content"][-1]["failure cause"] = failureCause
		
	def addActionItem(self, response):
		self.tree["content"].append({"type": "action call", "was successful": wasSuccessful})
		if wasSuccessful:
			self.tree["content"][-1]["returned"] = returned
		else:
			self.tree["content"][-1]["failure cause"] = failureCause
	
		
