from pymongo import MongoClient
import os
import pdb
import sys
sys.path.append('../')
import dgobs
import random
from User import User

def makeTemplate(fileName, orgName, shortDesc, dataMap):
	t = dgobs.Template(orgName = orgName, shortDesc = shortDesc, dataMap = dataMap)
	f = open(fileName, 'w')
	f.write(t.serialize())
	f.close()
	
def makeHostDb(dbName, collectionName, userAccounts):
	client = MongoClient()
	client.drop_database(dbName)
	collection = client[dbName][collectionName]
	collection.insert(userAccounts)
	client.close()

def makeUser(path, userID=None, privKey=None, cert=None):
	if userID == None:
		userID = hex(random.randrange(2**User.idLength))[2:].zfill(User.idLength/4)
	userFolder = path +'/u ' + userID + '/'
	
	# can combine both of these into one call to mkdirs  (notice extra s)
	# but haven't for clarity
	try:
		os.mkdir(userFolder)
		os.mkdir(userFolder+'dG_files')
	except Exception:
		pass
	
	if privKey == None:
		# TODO: generate private key file
		pass
	if cert == None:
		# TODO: generate cert
		pass
		
	f = open(userFolder+'cert.crt', 'w')
	f.write(cert)
	f.close()
	f = open(userFolder+'key.pem', 'w')
	f.write(privKey)
	f.close()

client1id = "3BFC8643C7AE9960".lower()

client1cert = """\
-----BEGIN CERTIFICATE-----
MIICDDCCAXWgAwIBAgIBCDANBgkqhkiG9w0BAQUFADArMQ0wCwYDVQQKEwRteUNB
MRowGAYDVQQDExE2ZTAzYzExMjhhMDJjNWE3IDAeFw0xMzA1MjAyMDAyMDBaFw0x
NDA1MjIyMDAyMDBaMBsxGTAXBgNVBAMTEDNCRkM4NjQzQzdBRTk5NjAwgZ8wDQYJ
KoZIhvcNAQEBBQADgY0AMIGJAoGBAMVamN2jF9r+dmO8SlAD9+E8ukDu6bRMFDz+
kRJRgUdh0pAzW5sTMO2b7lsJejETdVXaCEfPfQtyWhwC76QWM14xqDmT9QiPj1UD
YMaPE3qT+RcCxRoDXyjDxNEBiHZQHAbBFIANpcdSMxomXoxtrPk23UXB5AIbR87G
327HqBtlAgMBAAGjUDBOMAwGA1UdEwEB/wQCMAAwCwYDVR0PBAQDAgSwMBEGCWCG
SAGG+EIBAQQEAwIFoDAeBglghkgBhvhCAQ0EERYPeGNhIGNlcnRpZmljYXRlMA0G
CSqGSIb3DQEBBQUAA4GBALLeSu1IzRM+PO6Ys3EMiz9T7VNq59Mg1UnsY1SrGuXE
53WxnJq0ONXHjTMIHpGHiCDRH6GYATnkFZwR/9P8lu4wWtoUGmUHSEF7U5BQMOFv
+trChgYwsSnllV4yki3W2ZZdTnXg8mzGRh2skasshUi3hiEspnWxLHnpZCqrl+la
-----END CERTIFICATE-----
"""

client1key = """\
-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQDFWpjdoxfa/nZjvEpQA/fhPLpA7um0TBQ8/pESUYFHYdKQM1ub
EzDtm+5bCXoxE3VV2ghHz30LclocAu+kFjNeMag5k/UIj49VA2DGjxN6k/kXAsUa
A18ow8TRAYh2UBwGwRSADaXHUjMaJl6Mbaz5Nt1FweQCG0fOxt9ux6gbZQIDAQAB
AoGBAKTr+9kjxPi2M1tPa06IsmogZImE3fpUpYj/N152jDGJ1vu4X3ItTHMUHtEn
D1zZpPFUnhzckOOy8Qh9j6OxBcTU3SI2y30eJJTIRvW+7vI/SJuusk0vSLJiToP0
28cVXPyjxO6lmcsaPdynKrJSpXOATYZX0fNwv/5pwXF96SLBAkEA+Ntaa84sh1bS
QtTAj1HcixyjesRVfBlTkyyJ+GQh14gmc6SbZk/i9bHSv9lFzZ6bFHGBnag+D5vF
I2SNYGNoFQJBAMsEymJmdYZ/6Wkrq8Z5P4vYrLFDd21OrZ3lRHaL1/p7a4PaaQdY
NQy9+c5g2K2kDbygqHfA2kTSv/VA8zv/6hECQQC/79cuvOclP3aOay9VmwriFKWW
Q6W3QIVwRvLnLLvZU75shTICWG0xmQR2SesHq2PrAZy575BmU3taT+ymwiT9AkEA
qMBLpa065VivYH8vYmNoYcryCMpmm9I5WDS5SryFAyzRuqCyiqtUNUo4OcagdP0X
egIk5p3EEE8Jxkd9pxLasQJAYdJmdUUQXhfcXrXt4mOrmzoHQcqc4nXfkJsGcfAR
GCpbziXybrLK3Rq2GP3uaNFAuR/miEAOC+9AkyJs3TmtLA==
-----END RSA PRIVATE KEY-----
"""

client2cert = """\
-----BEGIN CERTIFICATE-----
MIIBujCCASOgAwIBAgIBCTANBgkqhkiG9w0BAQUFADArMQ0wCwYDVQQKEwRteUNB
MRowGAYDVQQDExE2ZTAzYzExMjhhMDJjNWE3IDAeFw0xMzA2MjgyMzI3MDBaFw0x
NDA2MjgyMzI3MDBaMBsxGTAXBgNVBAMTEDQ5Q0MwNzJCODhBMUFGREYwgZ8wDQYJ
KoZIhvcNAQEBBQADgY0AMIGJAoGBAKhJ/6jWtclGr95zN7m3rcQvcrEyJyJYHFWq
J+tTRtMpe6qft4oFAUaqYarLQz0ldtwaNNM44RmoH+Tr5YI5xIZX4/SUrK0aneV2
EQxJn2w27Ib8LE7phTYUAOuw5rv7KXKxTcg7AVAptCA8ZmDNHfK3VgHliObkdTdw
IzCKXPrxAgMBAAEwDQYJKoZIhvcNAQEFBQADgYEAKrAQpAqpVr3NNA9jxhOwqSEj
5OdcSRNMwUaB0jJiA6ytlvyI+XxkbQtV4PJu2dh7aFfhBph4AWqzBQWdVPSNJR+2
mYtSs3Gwr1s8WJvq/P62Os7FvugnwSOhZu0cu69zwzIJoNC3UjQjbrBTtCvyoLHL
w9mwzhx8wMKFbuyuf8k=
-----END CERTIFICATE-----
"""

client2id = "49CC072B88A1AFDF".lower()

client2key = """\
-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQCoSf+o1rXJRq/ecze5t63EL3KxMiciWBxVqifrU0bTKXuqn7eK
BQFGqmGqy0M9JXbcGjTTOOEZqB/k6+WCOcSGV+P0lKytGp3ldhEMSZ9sNuyG/CxO
6YU2FADrsOa7+ylysU3IOwFQKbQgPGZgzR3yt1YB5Yjm5HU3cCMwilz68QIDAQAB
AoGATKfISIPkshX8rfsVewbro91pBMWvhblUzsB/BnYcYLsYlZPC6p91AVdCvaVw
rz2NcpyNS1kxT5qBTKkXFcZyeXIBv/8sZqKd9cL1ztmqIqqrouHmeS/Tt3K1W4W6
xtlPdZ4iZ1KG01hXcUrNyfHlMMAfJQpZpqPA58IteJTJXEECQQDXCV/wv97NugqX
n3WZv4odQvm1tL3BckipOxYuU9/z7f42Dxak3LAOer9PY4/k/zjrfsO8U6gjuG7T
tJJ7Qc+tAkEAyFjmV1LxgNGr3dR3pdDAwFGWNw23lwjzmuRyc7w5MXkj5BuOLaOY
8bp6vIPbGOfacOfV1YVeDx9oXa6i+q3w1QJBAMTymSRvFyllU347VgJTI7RZO0vp
FkKu4U3eCBq2R0+qkkIA38RvO/CHC+EyVwBtoTxPBgbeuAi/SwIrSF4LkKECQQCa
ibhjc19F9nWTzufbx4Jm1ogAP1x17Dm8KKsACxgyyTaeJYMuQRsgmq9B6pN+Spl8
rdeLtCwxjhB68tJUewdhAkEAnsY67skUMOzm/k7Hkbkvapa/CCAtwgRibe5x5I4U
wciX+DAkJqPKiat55FrTJ6kt0eDUzzTjXWLRSjrLWxTmyQ==
-----END RSA PRIVATE KEY-----
"""

host1id = "9F32383582053809".lower()

host1cert = """\
-----BEGIN CERTIFICATE-----
MIICDDCCAXWgAwIBAgIBBzANBgkqhkiG9w0BAQUFADArMQ0wCwYDVQQKEwRteUNB
MRowGAYDVQQDExE2ZTAzYzExMjhhMDJjNWE3IDAeFw0xMzA1MjAyMDAwMDBaFw0x
NDA1MjIyMDAwMDBaMBsxGTAXBgNVBAMTEDlGMzIzODM1ODIwNTM4MDkwgZ8wDQYJ
KoZIhvcNAQEBBQADgY0AMIGJAoGBAKGs2kacikFGOKzDNcb8WSnLc4HEdwamR9XF
WO9B6TGhCm7dN5JGZOb9gUzbZY7xiHzDkGIaUulseFhnDTTDBsI7JmWJgIqWVeTS
eOpykZoNzwN4SCu9Uk0JjRFNohkU3Yiz96Y5yPFvzhrNhJwSrCo9ANzJI3l66cNZ
tUzlwyVTAgMBAAGjUDBOMAwGA1UdEwEB/wQCMAAwCwYDVR0PBAQDAgXgMBEGCWCG
SAGG+EIBAQQEAwIGQDAeBglghkgBhvhCAQ0EERYPeGNhIGNlcnRpZmljYXRlMA0G
CSqGSIb3DQEBBQUAA4GBAJRwTfHpPVePt5kDOgpjPcaWzWG8LtqQjSCi/MTBTVJE
fMHtlD2Oj5jlvgigRX5Vvwf7H/5TXkWIIUfqlI4bwxvXYjfKPwVeMj6Hcq1nF6Sf
IDvE/+Wg/Da5u+dwKK675XIjRe++3A6cOPG5Z2kFT1Ar+lysB00JDsa7DGATfgBD
-----END CERTIFICATE-----
"""

host1key = """\
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQChrNpGnIpBRjiswzXG/Fkpy3OBxHcGpkfVxVjvQekxoQpu3TeS
RmTm/YFM22WO8Yh8w5BiGlLpbHhYZw00wwbCOyZliYCKllXk0njqcpGaDc8DeEgr
vVJNCY0RTaIZFN2Is/emOcjxb84azYScEqwqPQDcySN5eunDWbVM5cMlUwIDAQAB
AoGBAI+H60hg1QTaGJqXu3hqs6W9L1B3YMwQdxm7WBcgxqv+skp2Lk24HQBM8quO
43yhxXAuFlJh2FXOrJCe/ERpF+eSYKsX55Yq7K+VFSAom56usdNlqBoJWFq7iVJ0
P9bZ8XnfQs8S/K3slnWqJE1fQDnYO6ToNwvqN9q5RcjcrLbRAkEAztv2ONu6hAAW
NnUgueHS0cdHcV9Ij/uucSEe0ClZ3QZMY6GXRtFyt0fogPWXT5FPaHGttG3rPCWt
HMitLTwOxwJBAMgVDDdMAM26ElyHV5QCYwBdOc6pmW+Ocjn2Z/H7ZTIDhJNxFybM
uR7iQHtiKtLwFQXDIAiXgxBLWNuM5a/3mRUCQGMQEb0u9QZr6DdSJkb+b3CI55zS
jbRuSh7hRplXhDKF5qU76G9AtJgzNpQziK/RHd8duZsTnLikLl//dneYMFcCQFMR
cf3vPxIqo37o7fJUP1giXGKxxTMsl7360FMFxZDLJxqzxCHmsyDgXFcdfZwP8xpu
VXlbth1out6EE8RH7rUCQQCMTdh7cLiLcTfWBT1CrvfUgfyyQA4aT7Yee+eXtwz/
s7O+PuDdDBlrhIVRcS08B17X9V/qRQYgrX8l3G3B9n2k
-----END RSA PRIVATE KEY-----
"""

ca_cert = """\
-----BEGIN CERTIFICATE-----
MIICPjCCAaegAwIBAgIBATANBgkqhkiG9w0BAQUFADArMQ0wCwYDVQQKEwRteUNB
MRowGAYDVQQDExE2ZTAzYzExMjhhMDJjNWE3IDAeFw0xMzA1MjAwOTI0MDBaFw0y
MzA1MjAwOTI0MDBaMCsxDTALBgNVBAoTBG15Q0ExGjAYBgNVBAMTETZlMDNjMTEy
OGEwMmM1YTcgMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDXa9/njEqJr7o
YmEScPHdDw2jfDnS5+34r1I7QM9iMaVqhq1IKfa88Ij4hcuBRNJz+mMT+KZBTV6x
G3meb/uYjlGITWggFMMWAq5fRhBLdYRaANuSuJZwSuE9WF7J0Ba2uoKbYVIlSGjB
eiAplVAwegQN7wkslC2HWPQlWo9vpQIDAQABo3IwcDAPBgNVHRMBAf8EBTADAQH/
MB0GA1UdDgQWBBSMpv2G603K6F9KB3heQ1Be+6kDxjALBgNVHQ8EBAMCAQYwEQYJ
YIZIAYb4QgEBBAQDAgAHMB4GCWCGSAGG+EIBDQQRFg94Y2EgY2VydGlmaWNhdGUw
DQYJKoZIhvcNAQEFBQADgYEAG3tmTMYyQ0Wl3TB3i/GMmPYODXPOcCJwrZcGvPjW
HCH0Ew+qiIZdJPMG/kN3+l3ueiUld7uWHxZ0w+5zyAJQSvQLAUgAPC8JYIjy6OpZ
Zwv32SohKmal7LwnwzjXFX/HUNH0DAXKfrU7obYwD8/VQn+S30iCHDFnxastVgVc
T28=
-----END CERTIFICATE-----
"""

if __name__ == '__main__':
	# ---- make users ------
	makeUser('kivyApp/', userID=client1id, privKey=client1key, cert=client1cert)
	makeUser('kivyApp/', userID=client2id, privKey=client2key, cert=client2cert)

	# ---- make hosts ------
	# certificate Authority host
	dataMap = {
		'children': {
			'name': {'type': 'regular', 'isOptional': False},
			'certificate': {'type': 'regular', 'isOptional':False}
		}
	}
			
	makeTemplate(fileName = 'certAuth.dgob',
				 orgName = 'certificate authority',
				 shortDesc = 'creates certificates for all users',
				 dataMap = dataMap)
	clientData = []
	clientData.append( {'_id': client1id, 'certificate': client1cert} )
	clientData.append( {'_id': client2id, 'certificate': client2cert} )
	makeHostDb('certAuth', 'people', clientData)

	# general information host
	dataMap = {
		'children': {
			'name': {'type': 'regular', 'isOptional': False},
			'birthday': {'type': 'regular', 'isOptional':False},
			'gender': {'type': 'regular', 'isOptional':False},
			'province': {'type': 'regular', 'isOptional':False},
			'city': {'type': 'regular', 'isOptional':False},
			'street address': {'type': 'regular', 'isOptional':False},
			'email address': {'type': 'regular', 'isOptional':True},
			'citizenship': {'type': 'regular', 'isOptional':False}
		}
	}
				 
	makeTemplate(fileName = 'genInfo.dgob',
				 orgName = 'general information',
				 shortDesc = 'maintains general information on people',
				 dataMap = dataMap)

	clientData = []

	clientData.append( {'_id': client1id, 'name': 'Joe Blow',
						'birthday': '1983-04-13', 'gender': 'male', 
						'province': 'QC', 'city': 'Westmount',
						'street address': '132 fakestreet',
						'citizenship': 'citizen'} )                
	clientData.append( {'_id': client2id, 'name': 'Sue Streisand',
				'birthday': '1993-06-01', 'gender': 'female', 
				'province': 'AB', 'city': 'Calgary',
				'street address': '7332 main',
				'citizenship': 'citizen'} )
				
	makeHostDb('genInfo', 'people', clientData)
	
	# health host
	dataMap = {
		'children': {
			'basic': {'type': 'inode', 'isOptional': False, 'children':{
				'weight': {'type': 'regular', 'isOptional':False},
				'height': {'type': 'regular', 'isOptional':False},
				'blood': {'type': 'regular', 'isOptional':False}}
			},
			'allergies': {'type': 'list', 'isOptional': False, 'children':{
				'allergen': {'type': 'regular', 'isOptional':False},
				'severity': {'type': 'regular', 'isOptional':False}}
			},
			'illnesses': {'type': 'list', 'isOptional': False, 'children':{
				'illness': {'type': 'regular', 'isOptional':False}}
			},
			'considerations': {'type': 'list', 'isOptional': False, 'children': {
				'issue code': {'type': 'regular', 'isOptional':False},
				'description': {'type': 'regular', 'isOptional':False}}
			},
			'history': {'type': 'list', 'isOptional': False, 'children':{
				'date': {'type': 'regular', 'isOptional':False},
				'location': {'type': 'regular', 'isOptional':False},
				'event': {'type': 'regular', 'isOptional':False}, # this could be elaborated
				'medical professional': {'type': 'regular', 'isOptional':False}}
			},
			'appointments': {'type': 'list', 'isOptional': False, 'children':{
				'date': {'type': 'regular', 'isOptional':False},
				'location': {'type': 'regular', 'isOptional':False},
				'short reason': {'type': 'regular', 'isOptional':False},
				'medical professional': {'type': 'regular', 'isOptional':False}}
			},
			'family doctor': {'type': 'regular', 'isOptional':True},
			'emergency contact': {'type': 'regular', 'isOptional':True}
		}
	}
				 
	makeTemplate(fileName = 'health.dgob',
				 orgName = 'health canada',
				 shortDesc = 'Provides health care to people',
				 dataMap = dataMap)

	clientData = []

	clientData.append( {'_id': client1id,
		'basic': {'weight': 150, 'height': 170, 'blood': 'O-'},
		'allergies': [{'allergen': 'seedless grapes', 'severity': 'life threatening'}],
		'illnesses': [{'illness': 'athsma'}],
		'considerations': [{'issue code': 02254, 'description': 'high cholesterol'}],
		'history': [{'date': '2011-08-04', 'location': 'CLSC Pointe Claire', 'event': 'routine checkup', 'medical professional':'02947ab93ef94556'},
		            {'date': '2011-01-06', 'location': 'Lakeshore Hospital', 'event':'sprained ankle', 'medical professional': '9de431237582a92b'}],
		'appointments': [{'date': '2013-09-12', 'location': 'Sacred Heart Hospital', 'short reason': 'chest x-ray', 'medical professional': '039287235939843b'},
		                 {'date': '2013-12-02', 'location': 'CLSC Pointe Claire', 'short reason': 'routine checkup', 'medical professional': '02947ab93ef94556'}],
		'family doctor': '02947ab93ef94556',
		'emergency contact': '7936a58ede922fed'
	})
	# TODO client2
				
	makeHostDb('health', 'people', clientData)


	# library host
	dataMap = {
		'children': {
			'amount due': {'type': 'regular', 'isOptional':False},
			'books on loan': {'type': 'list', 'isOptional':False, 'children':{
				'title': {'type': 'regular', 'isOptional':False},
				'ISBN': {'type': 'regular', 'isOptional':False},
				'date due': {'type': 'regular', 'isOptional':False},
				'fines': {'type': 'regular', 'isOptional':False}}
			}
		}
	}
				 
	makeTemplate(fileName = 'library.dgob',
				 orgName = 'Beaconsfield Library',
				 shortDesc = 'Beaconsfield city Library',
				 dataMap = dataMap)

	clientData = []

	clientData.append({'_id': client1id, 'amount due': 4.20, 'books on loan': [
	   {'title':'The Golden Compass', 'ISBN':9780440238133, 'date due': '2013-07-15', 'fines': 0.00},
	   {'title': 'The Cat in the Hat', 'ISBN':9780394800011, 'date due': '2013-08-01', 'fines': 0.00}]
	})

				
	makeHostDb('library', 'people', clientData)
