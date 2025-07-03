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
            self.ids.debug.text +='\nА тхт со спутниками тебе что сделал?'

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


            for line in App.get_running_app().antennas_list:
                params = line.split(';')
                if params[0] == selected_antenna_name:
                    cords = self.ids.ant_cords_input.text.split(';')
                    antenna = Transmitter(*params[1:7], *cords, True)


            for line in App.get_running_app().satellites_list:
                params = line.split(';')
                if params[0] == selected_satellite_name:
                    cords = self.ids.sat_cords_input.text.split(';')
                    satellite = Transmitter(*params[1:7], *cords, False)

            other_params = self.ids.other_params_input.text.split(';')

            if direction == 'from_antenna':
                result = antenna.Calculate_signal_noise_ratio(satellite, *other_params)
            else:
                result = satellite.Calculate_signal_noise_ratio(antenna, *other_params)

        except:
            result = 'Ошибка: некорректный ввод'

        self.ids.result_label.text = str(result)


class TempAntennaConstructorScreen(Screen):
    pass

class TempSatelliteConstructorScreen(Screen):
    pass

class OptimizeScreen(Screen): 
    def optimize(self):
        pass


class BaseConstructorScreen(Screen):
    file_name = StringProperty()
    obj_list = ListProperty()
    selected_object = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fill_inputs(self):
        selected_name = self.ids.spinner.text
        if selected_name != 'Добавить':
            for line in self.obj_list:
                sline = line.split(';')
                if sline[0] == selected_name:
                    self.ids.name.text = sline[0]
                    self.ids.output_transmitter.text = sline[1]
                    self.ids.loss_transmitter.text = sline[2]
                    self.ids.antenna_diameter.text = sline[3]
                    self.ids.focus_antenna.text = sline[4]
                    self.ids.antenna_efficiency.text = sline[5]
                    self.ids.frequency.text = sline[6]
                    break
        else:
            self.ids.output_transmitter.text = ''
            self.ids.loss_transmitter.text = ''
            self.ids.antenna_diameter.text = ''
            self.ids.focus_antenna.text = ''
            self.ids.antenna_efficiency.text = ''
            self.ids.frequency.text = ''

    def save_params(self):

            if self.ids.spinner.text == 'Добавить':
                name = self.ids.name.text
                output_transmitter = self.ids.output_transmitter.text
                loss_transmitter = self.ids.loss_transmitter.text 
                antenna_diameter = self.ids.antenna_diameter.text
                focus_antenna = self.ids.focus_antenna.text
                antenna_efficiency = self.ids.antenna_efficiency.text
                frequency = self.ids.frequency.text
                self.obj_list.append(f'{name};{output_transmitter};{loss_transmitter};{antenna_diameter};{focus_antenna};{antenna_efficiency};{frequency}')
                self.ids.title_label.text = 'Успешно добавлено!'
            else:
                name = self.ids.name.text
                output_transmitter = self.ids.output_transmitter.text
                loss_transmitter = self.ids.loss_transmitter.text 
                antenna_diameter = self.ids.antenna_diameter.text
                focus_antenna = self.ids.focus_antenna.text
                antenna_efficiency = self.ids.antenna_efficiency.text
                frequency = self.ids.frequency.text
                i = -1
                for obj_name in self.obj_names:
                    if name == obj_name:
                        print(self.obj_list[i])
                        print(f'{name};{output_transmitter};{loss_transmitter};{antenna_diameter};{focus_antenna};{antenna_efficiency};{frequency}')
                        self.obj_list[i] = f'{name};{output_transmitter};{loss_transmitter};{antenna_diameter};{focus_antenna};{antenna_efficiency};{frequency}'
                    i += 1
                    self.ids.title_label.text = 'Успешно изменено!'


    @property
    def obj_names(self):
        return []
    @property
    def obj_list(self):
        return []


class AntennaConstructorScreen(BaseConstructorScreen):
    title_text = "Конструктор антенны"
    choose_text = "Выберете антенну"
    file_name = "antennas.txt"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def obj_names(self):
        return App.get_running_app().antennas_names_with_add

    @property
    def obj_list(self):
        return App.get_running_app().antennas_list


class SatelliteConstructorScreen(BaseConstructorScreen):
    title_text = "Конструктор спутника"
    choose_text = "Выберете спутник"
    file_name = "satellites.txt"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def obj_names(self):
        return App.get_running_app().satellites_names_with_add

    @property
    def obj_list(self):
        return App.get_running_app().satellites_list

class CalcApp(App):
    antennas_list = ListProperty()
    satellites_list = ListProperty()
    antennas_names = ListProperty()
    satellites_names = ListProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(antennas_list = self.update_antennas)
        self.bind(satellites_list = self.update_satellites)

    def update_antennas(self, instance, value):
        self.antennas_names = [line.split(';')[0] for line in value]

    def update_satellites(self, instance, value):
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
        sm.add_widget(TempAntennaConstructorScreen(name="tempant"))
        sm.add_widget(TempSatelliteConstructorScreen(name="tempsat"))
        sm.add_widget(OptimizeScreen(name="optimize"))
        sm.add_widget(AntennaConstructorScreen(name="antedit"))
        sm.add_widget(SatelliteConstructorScreen(name="satedit"))
        return sm

    def _update_bg_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    @property
    def antennas_names_with_add(self):
        names = list(self.antennas_names)
        if 'Добавить' in names:
            names.remove('Добавить')
        return ['Добавить'] + names

    @property
    def satellites_names_with_add(self):
        names = list(self.satellites_names)
        if "Добавить" in names:
            names.remove("Добавить")
        return ["Добавить"] + names



CalcApp().run()