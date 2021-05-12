import kivy
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import time
Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')

class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class TestCamera(App):

    def build(self):
        return CameraClick()

if __name__ == "__main__":
    TestCamera().run()