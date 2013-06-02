import argparse
import random
import os
from User import User

def makeUser(path, idNum=None, privKey=None, cert=None):
	if idNum == None:
		idNum = random.randrange(2**User.idLength)
	userFolder = User(idNum).getIdHex()
	
	# can combine both of these into one call to mkdirs  (notice extra s)
	# but haven't for clarity
	os.mkdir(userFolder)
	os.mkdir("{}/dG_files".format(userFolder)
	
	if privKey == None:
		# TODO: generate private key file
		pass
	if cert == None:
		# TODO: generate cert
		pass
