import kivy
kivy.require('1.7.0')

#from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.listview import ListView, ListItemButton
from kivy.app import App
from kivy.adapters.listadapter import ListAdapter
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.lang import Builder

class MyListView(ListView):
	
	

	data = ListProperty()
	@staticmethod
	def args_converter(row_index, obj):
		return {'text': obj,
		        'size_hint_y': None,
		        'height':25}
	
	
	
	def on_data(self, instance, val):
		list_adapter = ListAdapter(data=self.data,
		                    args_converter=self.args_converter,
		                    cls=ListItemButton,
		                    selection_mode='single')
		self.adapter = list_adapter
		        
	def __init__(self, **kwargs):		
		super(MyListView, self).__init__()
		
        
	

		
class Main(Screen):
	hostList = ListProperty(['a1', 'a2', 'a3'])
	
class BeaconsfieldLibrary(Screen):
	pass
	
class HealthCanada(Screen):
	pass

class ClientInterface(App):
	def build(self):
		kvFiles = ['mainScreen.kv', 
		           'healthCanada.kv', 
		           'beaconsfieldLibrary.kv']
		           
		sm = ScreenManager()
		for file in kvFiles:
			sm.add_widget(Builder.load_file(file))
		"""
		sm.add_widget(Main(name='main'))
		sm.add_widget(BeaconsfieldLibrary(name='library'))
		sm.add_widget(HealthCanada(name='health'))
		"""

		
		return sm
		
		#return Builder.load_file('beaconsfieldLibrary.kv')
		# return Builder.load_file('mainScreen.kv')
		# return Builder.load_file('healthCanada.kv')


if __name__ == '__main__':
    ClientInterface().run()
