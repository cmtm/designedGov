from DG_file import DG_file

class Request(DG_file):
	def __init__(self, authorId = 0, content = []):
		super().__init__("request", authorId, content)
	
	def addReadItem(self, data_path):
		self.tree["content"].append({"type": "read", "data path": data_path})
		
	def addWriteItem(self, data_path, new_value):
		self.tree["content"].append({"type": "write", "data path": data_path, "new value": new_value})
	
	def addActionItem(self, action_name, parameters = {}):
		self.tree["content"].append({"type": "action call", "action name": action_name, "parameters": parameters})