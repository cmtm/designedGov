import kivy
kivy.require('1.0.5')

#from kivy.uix.widget import Widget
#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty


class DG_Client(TabbedPanel):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''
    label_wid = ObjectProperty()
    info = StringProperty()

    def do_action(self):
        self.label_wid.text = 'My label after button press'
        self.info = 'New info text'


class DG_ClientApp(App):
	pass
"""
    def build(self):
        return DG_Client(info='Hello world')
"""
if __name__ == '__main__':
    DG_ClientApp().run()
