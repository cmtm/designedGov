from pymongo import MongoClient
import os
import pdb
import sys
sys.path.append('../')
import dgobs


def makeCertAuthTemplate(templateFile):
	t = dgobs.Template(orgName = 'certificate authority', 
	                   shortDesc = 'creates certificates for all users')
	t.addData(['name'], 'regular')
	# TODO: add certificate
	
	f = open(templateFile, 'w')
	f.write(t.serialize())
	f.close()
	
def makeCertAuthDb(sourceData):
	client = MongoClient()
	client.drop_database('certAuth')
	db = client.certAuth
	people = db.people
	
	for row in sourceData:
		people.insert({k:row[k] for k in ['_id', 'name']})

def makeGeneralInfoTemplate(templateFile):
	t = dgobs.Template(orgName = 'general Information', 
	                   shortDesc = 'maintains general information on people')
	ds = ['guid', 'name', 'birthday', 'gender', 'state', 'city', 'streetaddress', 'emailaddress']
	for d in ds:
		t.addData([d], 'regular')

	# TODO: add certificate
	
	f = open(templateFile, 'w')
	f.write(t.serialize())
	f.close()
	
def makeGeneralInfoDb(sourceData):
	client = MongoClient()
	client.drop_database('genInfo')
	db = client.genInfo
	people = db.people
	
	for row in sourceData:
		people.insert({k:row[k] for k in ['_id', 'name', 'birthday', 'gender', 'state', 'city', 'streetaddress', 'emailaddress']})

# changes some columns from fakenames to make it more suitable
def genData(sourceFile):
	f = open(sourceFile, 'r')
	data = []
	
	for line in f.readlines():
		data.append(line.strip().split(','))
	f.close()
	assert len(data[0]) == len(data[1])
	
	# make column names lowercase
	data[0] = [s.lower() for s in data[0]]
	
	guidIndex = data[0].index('guid')
	data[0][guidIndex] = '_id'
	
	for row in data[1:]:
		guid = row[guidIndex]
		row[guidIndex] = guid[:8]+guid[9:13]+guid[14:18]
	
	# put userID as first column
	for row in data:
		row[0], row[guidIndex] = row[guidIndex], row[0]
	
	birthdayIndex = data[0].index('birthday')
	# fix birthday
	for row in data[1:]:
		bd = row[birthdayIndex].split('/')
		row[birthdayIndex] = bd[2]+'-'+bd[0]+'-'+bd[1]
	
	# add full name
	givenName = data[0].index('givenname')
	surname = data[0].index('surname')
	
	data[0].append('name')
	
	for row in data[1:]:
		row.append(row[givenName] + ' ' + row[surname])
	
	
	# make data into dictionary
	structuredData = []
	for row in data[1:]:
		structuredData.append({column: val for column, val in zip(data[0], row)})
	
	return structuredData
	
if __name__ == '__main__':
	data = genData('fakenames.csv')
	pdb.set_trace()
	makeCertAuthTemplate('certAuth.dgob')
	makeCertAuthDb(data)
	makeGeneralInfoTemplate('genInfo.dgob')
	makeGeneralInfoDb(data)
