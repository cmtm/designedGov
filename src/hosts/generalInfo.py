import sys
sys.path.append('../')
from Host import Host


class CertificateAuthority(Host):
	
	readables= {'name': 'name',
	            'birthday': 'birthday',
	            'gender':'gender',
	            'province':'province', 
	            'city':'city', 
	            'street address':'streetaddress', 
	            'email':'email'}
	writables= {'province':'province', 
	            'city':'city', 
	            'street address':'streetaddress', 
	            'email':'email'}
		
if __name__ == '__main__':
	c = CertificateAuthority(10001, '../keysAndCerts/certificates/myCA.crt' , '../keysAndCerts/certificates/host2.crt', "TODO", 'certAuth.db', 'people')
	c.listenForRequests()

