import sys
sys.path.append('../')
from Host import Host


class CertificateAuthority(Host):
	
	readables= {'name': 'name', 'certificate': 'certificate'}
	writables= {}
		
if __name__ == '__main__':
	c = CertificateAuthority(10001, '../keysAndCerts/certificates/myCA.crt' , '../keysAndCerts/certificates/host1.crt', "TODO", 'certAuth.db', 'people')
	c.listenForRequests()
