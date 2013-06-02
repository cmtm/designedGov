import random
import unittest
import subprocess

from ClientWebInterface import ClientWebInterface
from Request import Request
from Response import Response

class TestSequenceFunctions(unittest.TestCase):
	
	def setUp(self):
		self.proc = subprocess.Popen(["python", "dummyServer.py"], stdout=subprocess.PIPE)
		self.myClient = ClientWebInterface(certfile="keysAndCerts/certificates/client1.crt",
		                              ca_cert="keysAndCerts/certificates/myCA.crt",
		                              keyfile="keysAndCerts/keys/client1.pem")
	
	def tearDown(self):
		self.proc.terminate()

	def test_ping(self):
		req = Request()
		self.proc.stdout.readline()
		resp = self.myClient.sendRequestTo('localhost', 10023, \
		                                 u'9F32383582053809', req)
		self.assertTrue(resp.typeName == 'response')


if __name__ == '__main__':
    unittest.main()

