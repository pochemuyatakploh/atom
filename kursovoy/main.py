from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.button import Button
from threading import Thread
from kivy.clock import Clock
import bluetooth
import threading

Window.size = (480,853)
mutex = threading.Lock()

class Container(BoxLayout):

    def __init__(self):
        super().__init__()
        self.tr1 = Thread(target=self.devices())
        self.tr1.start()

    def changename(self):
        self.toolbar.title = "Robot controls"
        self.remove_widget(self.lay)
        self.layout = GridLayout(cols=3, padding=50, spacing=10)
        #list = ['arrow-top-left','arrow-up-bold-outline','arrow-top-right','arrow-left-bold-outline','car-light-dimmed','arrow-right-bold-outline','arrow-bottom-left','arrow-down-bold-outline','arrow-bottom-right']
        list = ['turn left','forward','turn right','left','<3','right','smth','back','smth']
        for i in range(9):
            self.ctrl = Button(text = str(list[i]))
            self.ctrl.bind(on_press=self._on_press)
            self.ctrl.bind(on_release=self._on_release)
            self.layout.add_widget(self.ctrl)

        self.add_widget(self.layout, index = 1)

    def changenameback(self):
        self.toolbar.title = "Connection"
        self.lay = BoxLayout(orientation='vertical')
        self.remove_widget(self.layout)
        self.tr2 = Thread(target=self.devices())
        self.tr2.start()


    def start_movement(self):
        Clock.schedule_interval(self._move_right,0.01)

    def stop_movement(self):
        Clock.unschedule(self._move_right)

    def _move_right(self, dt):
        print("wtf")


    def devices(self):
        devicee = bluetooth.discover_devices(lookup_names=True)
        with mutex:
            self.lay = StackLayout()
            for device in devicee:
                line = OneLineListItem(text=str(device[1]))
                self.lay.add_widget(line)
            self.add_widget(self.lay, index=1)

    def _on_press(self, button):
        self.start_movement()
        print(button.text)

    def _on_release(self, button):
        self.stop_movement()

class mainapp(MDApp):

    def build(self):
        c = Container()
        return c


if __name__ == '__main__':
    mainapp().run()
