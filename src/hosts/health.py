import sys
sys.path.append('../')
from Host import Host


class CertificateAuthority(Host):
	
	readables= {'gender': 'gender'
	            'blood type': 'bloodtype',
	            'weight': 'weight',
	            'height': 'height',
	            'allergies': 'allergies',
	            'medical considerations':'medicalConsiderations',
				'illnesses': 'illneses',
				'emergency contact': 'emergencyContact',
				'family doctor': 'familyDoctor'
				}
	writables= {'province':'province', 
	            'city':'city', 
	            'street address':'streetaddress', 
	            'email':'email'}
		
if __name__ == '__main__':
	c = CertificateAuthority(10001, '../keysAndCerts/certificates/myCA.crt' , '../keysAndCerts/certificates/host2.crt', "TODO", 'certAuth.db', 'people')
	c.listenForRequests()


