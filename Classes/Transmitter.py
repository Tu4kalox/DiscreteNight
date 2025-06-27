import  math
from pyproj import Transformer

class AntennaSystem(object):
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
        term = (1 + (4 * f**2) / D**2)**1.5
        return (math.pi * D**3 / (48 * f**2)) * (term - 1)
    
    def calculate_COD(self):
        # Вычисляет коэффициент направленного действия (КНД)
        # G = alpha * (4*Pi*S/lambda^2)
        return self.antennaTypeCoefficient * (4 * math.pi * self.areaOfSurface) / (self.waveLength**2)
    
    @staticmethod
    def convert_to_decibel(value):
        # Конвертирует линейное значение в децибелы
        return 10 * math.log10(value) if value > 0 else -math.inf
    
    def get_ecef_coordinates(self):
        if self.IsGround:
            result = self._geoid_transformer.transform(self.pos1, self.pos2, self.pos3)
            h_ellipsoid = result[2] #Высота над эллипсоидом из кортежа 
            return self._transformer.transform(self.pos1, self.pos2, h_ellipsoid)

    def Calculate_distance_to(self, other):
        self_coords = self.get_ecef_coordinates()
        other_coords = other.get_ecef_coordinates()
        return math.sqrt(sum((a-b)**2 for a, b in zip(self_coords, other_coords))) #zip для красоты, тут он попарно вычисляет квадрат разности координат


    
    

    
            





