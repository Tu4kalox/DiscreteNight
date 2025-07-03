import  math
from pyproj import Transformer

class Transmitter(object):
    def __init__(self, outputOfTransmitter, lossInTransmitter, AntennaDiameter, focusOfAntenna, antennaTypeCoefficient, frequency, pos1, pos2, pos3, isGround):
        # 
        # Конструктор класса антенной системы
        
        # Параметры:
        #     outputOfTransmitter: мощность передатчика (Вт)
        #     lossInTransmitter: потери в передатчике (дБ)
        #     AntennaDiameter: диаметр антенны (м)
        #     focusOfAntenna: фокусное расстояние антенны (м)
        #     antennaTypeCoefficient: КПД антенны (0..1)
        #     frequency: рабочая частота (Гц)
        #     pos1, pos2, pos3: координаты позиции (с.ш. в.д./з.д., уровень моря, или в геоцентр x, y, z)
        # 
        self.waveLength = 299792458 / float(frequency)
        self.outputOfTransmitter = float(outputOfTransmitter)
        self.lossInTransmitter = float(lossInTransmitter)
        self.antennaDiameter = float(AntennaDiameter)
        self.focusOfAntenna = float(focusOfAntenna)
        self.antennaTypeCoefficient = float(antennaTypeCoefficient)
        self.pos1 = float(pos1)
        self.pos2 = float(pos2)
        self.pos3 = float(pos3)
        self.IsGround = bool(isGround)
        self._transformer = Transformer.from_crs("EPSG:4326", "EPSG:4978") #Инициализация преобразователя из библиотеки EPSG - обозначения систем
        self._geoid_transformer = Transformer.from_crs("EPSG:4326+5773", "EPSG:4326") #Тут высота над уровнем моря в высоту над эллипсоидом + аномалия высоты 5773 - модель геоида
        #self.IsGround = bool(IsGround) # True - если объект на земле, False - если это спутник
        
        # Вычисляем производные параметры
        self.areaOfSurface = self.calculate_area_of_surface()
        self.coefficientOfDirectedAction = self.calculate_COD()
    
    def calculate_area_of_surface(self):
        # Вычисляет площадь поверхности параболической антенны
        D = self.antennaDiameter
        f = self.focusOfAntenna
        try:
            term1 = (f + D**2/(16*f))**1.5
            term2 = f**1.5
            return (8 * math.pi * math.sqrt(f) / 3) * (term1 - term2)
        except ZeroDivisionError:
            return 2*math.pi*(D/2)**2
    
    def calculate_COD(self):
        # Вычисляет коэффициент направленного действия (КНД)
        # G = alpha * (4*Pi*S/lambda^2)
        return self.antennaTypeCoefficient * (4 * math.pi * self.areaOfSurface) / (self.waveLength**2)
    
    @staticmethod
    def convert_to_decibel(value):
        # Конвертирует линейное значение в децибелы
        return 10 * math.log10(float(value)) if float(value) > 0 else -math.inf
    
    def get_ecef_coordinates(self):
        if self.IsGround:
            result = self._geoid_transformer.transform(self.pos1, self.pos2, self.pos3)
            h_ellipsoid = result[2] #Высота над эллипсоидом из кортежа 
            return self._transformer.transform(self.pos1, self.pos2, h_ellipsoid)
        return (self.pos1, self.pos2, self.pos3)
    def Calculate_distance_to(self, other):
        self_coords = self.get_ecef_coordinates()
        other_coords = other.get_ecef_coordinates()
        return math.sqrt(sum((a-b)**2 for a, b in zip(self_coords, other_coords))) #zip для красоты, тут он попарно вычисляет квадрат разности координат

    def Calculate_signal_noise_ratio(self, other_ant, l2, l3, l4, l5, rate_of_transm, temperature): 
        Knd_earth = self.convert_to_decibel(self.coefficientOfDirectedAction)
        Knd_space = self.convert_to_decibel(other_ant.coefficientOfDirectedAction)
        Sat_distance = self.Calculate_distance_to(other_ant)
        l1= self.convert_to_decibel(16*(3.1415**2)*Sat_distance**2/(self.waveLength**2))
        EIRP_self = self.outputOfTransmitter + Knd_earth - self.lossInTransmitter
        Accepted_isotropic_power = EIRP_self - l1 - float(l2) - float(l3)
        Power_of_recived_signal = Accepted_isotropic_power + Knd_space - float(l4)
        temperature_decibel = self.convert_to_decibel(float(temperature))
        Spectral_velocity_of_noice = -228.6 + temperature_decibel
        Signal_noise_ratio = Power_of_recived_signal - Spectral_velocity_of_noice - float(rate_of_transm) - float(l5)
        return Signal_noise_ratio



    
    

    
            





