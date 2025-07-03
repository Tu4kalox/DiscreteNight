from turtle import update
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
from os import close
from tokenize import String
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ListProperty, StringProperty
from pyproj import Transformer
from Classes.Transmitter import Transmitter



Builder.load_file('UI.kv')

class MenuScreen(Screen):
    def __init__(self, **kwargs):
       super().__init__(**kwargs)
       self.load_data()

    def load_data(self):
        try:
            with open('antennas.txt', 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
            App.get_running_app().antennas_list = lines

        except FileNotFoundError:
            self.ids.debug.text += '\nТы зачем удалил тхтшник c антеннами?'

        try:
            with open('satellites.txt', 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
            App.get_running_app().satellites_list = lines
        except FileNotFoundError:
            self.ids.debug.text +='\nА тхт со спутниками чоте сделал?'

    def save_and_exit(self):
        with open('antennas.txt', 'w', encoding='utf-8') as f:
            f.writelines(line + '\n' for line in App.get_running_app().antennas_list)
        with open('satellites.txt', 'w', encoding='utf-8') as f:
            f.writelines(line + '\n' for line in App.get_running_app().satellites_list)
        App.get_running_app().stop()


class CalcScreen(Screen):
    def calculate(self, direction='from_antenna'):
        try:
            selected_antenna_name = self.ids.antenna_spinner.text
            selected_satellite_name = self.ids.satellite_spinner.text

            with open('antennas.txt', 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
                for line in lines:
                    params = line.split(';')
                    if params[0] == selected_antenna_name:
                        cords = self.ids.ant_cords_input.text.split(';')
                        antenna = Transmitter(*params[1:7], *cords, True)

            with open('satellites.txt', 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
                for line in lines:
                    params = line.split(';')
                    if params[0] == selected_satellite_name:
                        cords = self.ids.sat_cords_input.text.split(';')
                        satellite = Transmitter(*params[1:7], *cords, False)

            other_params = self.ids.other_params_input.text.split(';')

            if direction == 'from_antenna':
                result = antenna.Calculate_signal_noise_ratio(satellite, *other_params)
            else:
                result = satellite.Calculate_signal_noise_ratio(antenna, *other_params)

        except :
            result = 'Ошибка: некорректный ввод, мало чисел?'

        self.ids.result_label.text = str(result)

class OptimizeScreen(Screen): 
    def optimize(self):
        pass


class BaseConstructorScreen(Screen):
    file_name = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class AntennaConstructorScreen(BaseConstructorScreen):
    title_text = "Конструктор антенны"
    choose_text = "Выберете антенну"
    file_name = "antennas.txt"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SatelliteConstructorScreen(BaseConstructorScreen):
    title_text = "Конструктор спутника"
    choose_text = "Выберете спутник"
    file_name = "satellites.txt"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CalcApp(App):
    antennas_list = ListProperty()
    satellites_list = ListProperty()
    antennas_names = ListProperty()
    satellites_names = ListProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(antennas_list = self.update_antennas_names)
        self.bind(satellites_list = self.update_satellites_names)

    def update_antennas_names(self, instance, value):
        self.antennas_names = [line.split(';')[0] for line in value]

    def update_satellites_names(self, instance, value):
        self.satellites_names = [line.split(';')[0] for line in value]

    def build(self):
        sm = ScreenManager()
        
        with sm.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.07, 0.07, 0.07, 1) 
            self.bg_rect = Rectangle(size=sm.size, pos=sm.pos)

        sm.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(CalcScreen(name="calc"))
        sm.add_widget(OptimizeScreen(name="optimize"))
        sm.add_widget(AntennaConstructorScreen(name="antedit"))
        sm.add_widget(SatelliteConstructorScreen(name="satedit"))
        return sm

    def _update_bg_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos



CalcApp().run()