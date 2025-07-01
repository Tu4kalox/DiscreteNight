from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ListProperty


Builder.load_file('UI.kv')

AntsForOpt = []
Ants = open('antennas.txt')
for ant in Ants:


class MenuScreen(Screen): pass
class CalcScreen(Screen):
    def calculate(self):
        try:
            ant = list(map(float, self.ids.ant_input.text.split(';')))
            sat = list(map(float, self.ids.sat_input.text.split(';')))
            result = f"Расстояние между антенной и спутником рассчитать тяжело {ant[1]}"
            self.ids.result_label.text = result
        except:
            self.ids.result_label.text = "Ошибка: некорректный ввод"

class OptimizeScreen(Screen): 
    def optimize(self):


class CalcApp(App):
    def build(self):
        sm = ScreenManager()
        
        with sm.canvas.before:
            from kivy.graphics import Color, Rectangle2
            Color(0.07, 0.07, 0.07, 1) 
            self.bg_rect = Rectangle(size=sm.size, pos=sm.pos)

        sm.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(CalcScreen(name="calc"))
        sm.add_widget(OptimizeScreen(name="optimize"))
        return sm

    def _update_bg_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos



CalcApp().run()