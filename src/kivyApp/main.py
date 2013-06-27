import kivy
kivy.require('1.7.0')

#from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
from kivy.adapters.listadapter import ListAdapter
from kivy.properties import *
from kivy.lang import Builder
from kivy.clock import Clock

import os, os.path
import urllib2
import yaml

import pdb
# for import path extension
import sys
sys.path.append('../')

from ClientWebInterface import ClientWebInterface
import User
from dgobs import *


class ButtonList(AnchorLayout):
	displays = ListProperty()
	args = ListProperty()
	callback = ObjectProperty()
	
	def __init__(self, **kwargs):
		super(ButtonList, self).__init__(**kwargs)
		Clock.schedule_once(self.late_init, 0)
	
	def late_init(self, *largs):
		box = BoxLayout(orientation='vertical')
		for (disp, arg) in zip(self.displays, self.args):
			btn = Button(text=disp, size_hint_y=None, height=25)
			btn.bind(on_press=lambda inst:self.callback(arg))
			box.add_widget(btn)
		scrollable = ScrollView(size_hint_x=0.7, do_scroll_x=False)
		scrollable.add_widget(box)
		self.add_widget(scrollable)    

class Main(Screen):
	pass

	# TODO: scan for local hosts and rescan on clock


class HostInterface(Screen):
	name = StringProperty()

	hostId = StringProperty()
	address = StringProperty()
	port = NumericProperty()

	def connect(self, cwi):
		self.cwi = cwi
		self.cwi.connectTo(self.address, self.port, self.hostId)
		# send default request

	def sendRequest(self, req):
		return self.cwi.sendRequest(req)

class BeaconsfieldLibrary(HostInterface):
	pass
	
class HealthCanada(HostInterface):
	pass

class DemoInterface(App):
	user = ObjectProperty()
	userInfo = DictProperty({})
	userList = ListProperty()
	hosts = ListProperty()
	socket = ObjectProperty()
	
	def connectToHost(self, hostName):
		if hostName != None:
			self.sm.current = hostName
			self.sm.current_screen.connect(self.socket)
	
	def wget(self, url):
		try:
			f = urllib2.urlopen(url)		
			localCopy = open(url.split('/')[-1], 'w')
			localCopy.write(f.read())
			localCopy.close()
		except urllib2.URLError as e:
			msg = "Error: {}".format(e.reason)
		except IOError as e:
			msg = "Error: {}".format(e.strerror)
		else:
			msg = "Download Successful."
			
		btnclose = Button(text='OK', size_hint_y=None, height='50sp')
		content = BoxLayout(orientation='vertical')
		content.add_widget(Label(text=msg))
		content.add_widget(btnclose)
		popup = Popup(content=content, title='File Download',
		              size_hint=(None, None), size=('300dp', '300dp'))
		btnclose.bind(on_release=popup.dismiss)
		
		popup.open()
	
	def __init__(self, **kwargs):		
		super(DemoInterface, self).__init__(**kwargs)
		
		self.findUsers()		
		# arbitrarily set first		
		self.setUser(self.userList[0])
		
		# TODO: fix kludge
		# self.userInfo = {'name': 'Joe Blow', 'birth': '1985-06-08', 'sex': 'male', 'image': 'u '+self.userList[0]+'/portrait.png'}
			
	def findUsers(self):
		dirs = [entry for entry in os.listdir('./') if os.path.isdir(entry)]
		self.userList = [d[2:] for d in dirs if d[:2]=='u ']		
	
	def setUser(self, name):
		usrDir = 'u '+name
		ls = os.listdir(usrDir)
		privKey = next(k for k in ls if '.pem' == k[-4:])
		cert = next(k for k in ls if '.crt' == k[-4:])
		userDir = os.getcwd() + '/u {}/'.format(name)
		self.user = User.User(name, '{}/{}'.format(userDir, cert), '{}/{}'.format(userDir, privKey))
		self.socket = ClientWebInterface(userDir+cert, './CA.crt', userDir+privKey)
		self.getUserInfo()
		self.userInfo['portrait'] = userDir + 'portrait.png'
	
	def getUserInfo(self):		
		req = Request(self.user.idNum)
		req.addRead('')
		
		args = ('localhost', 10001, u'9F32383582053809', req)
		resp = self.socket.sendRequestTo( *args)
		# TODO: fix the kludges, add security
		pdb.set_trace()
		self.userInfo = resp.getResps()[0]['value read']
	
	def build(self):
		self.sm = ScreenManager()
		self.sm.add_widget(Builder.load_file('mainScreen.kv'))
		
		kvFiles = ['healthCanada.kv',
		           'beaconsfieldLibrary.kv']
		
		self.hosts = []
		for file in kvFiles:
			host = Builder.load_file(file)
			self.hosts.append(host)
			self.sm.add_widget(host)

		
		return self.sm
		
		#return Builder.load_file('beaconsfieldLibrary.kv')
		# return Builder.load_file('mainScreen.kv')
		# return Builder.load_file('healthCanada.kv')


if __name__ == '__main__':
    DemoInterface().run()
