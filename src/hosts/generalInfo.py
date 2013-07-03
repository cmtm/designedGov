import sys
sys.path.append('../')
from Host import Host


if __name__ == '__main__':
	c = Host(10001, '../keysAndCerts/certificates/myCA.crt' , '../keysAndCerts/certificates/host1.crt', "../keysAndCerts/keys/host1.pem", 'genInfo.dgob', 'genInfo', 'people')
	c.listenForRequests()

