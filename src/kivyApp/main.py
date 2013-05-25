import kivy
kivy.require('1.7.0')

#from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder


class MainScreen(TabbedPanel):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''
    label_wid = ObjectProperty()
    info = StringProperty()

    def do_action(self):
        self.label_wid.text = 'My label after button press'
        self.info = 'New info text'

class BeaconsfieldLibrary(BoxLayout):
	pass

class HealthCanada(TabbedPanel):
	pass

class DG_ClientApp(App):
	def build(self):
		# return Builder.load_file('beaconsfieldLibrary.kv')
		# return Builder.load_file('mainScreen.kv')
		return Builder.load_file('healthCanada.kv')


if __name__ == '__main__':
    DG_ClientApp().run()
