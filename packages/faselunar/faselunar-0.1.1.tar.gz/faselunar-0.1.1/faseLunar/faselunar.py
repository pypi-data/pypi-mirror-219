import emoji

"""
clase fase lunar
"""
class FaseLunar:

    """
    constructor que recibe el dia, mes y año
    """
    def __init__(self, dia, mes, anio):
        """
        se valida cada parametro ingresado, de lo contrario arrojará error
        :param dia:
        :param mes:
        :param anio:
        """
        self.mes = self.validar_mes(mes)
        self.dia = self.validar_dia(dia)
        self.anio = self.validar_anio(anio)
        # valor para la descripcion del estado lunar
        self.descripciones = ["Nueva",
      "Lunula creciente",
      "Cuarto creciente",
      "Gibosa creciente",
      "Llena",
      "Gibosa Menguante",
      "Cuarto Menguante",
      "Lúnula Menguante"]
        # meses del año
        self.meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.dias_fase = 0
        self.estado = None
        self.estado_calc = False

    def es_bisiesto(self):
        """
        funcion que verifica si se trata de un año bisiesto
        entrada: ninguna
        salida: True o False si es que es bisiesto o no
        :return:
        """
        if self.anio % 400 == 0 or (self.anio % 100 != 0 and self.anio % 4 == 0):
            return True
        return False

    def set_mes(self, mes):
        """
        funcion que setea un nuevo mes
        :param mes:
        :return:
        """
        self.mes = self.validar_mes(mes)

    def set_anio(self, anio):
        """
        funcion que setea un nuevo año
        :param anio:
        :return:
        """
        self.anio = self.validar_anio(anio)

    def set_dia(self, dia):
        """
        funcion que setea un nuevo dia
        :param dia:
        :return:
        """
        self.dia = self.validar_dia(dia)

    def get_mes(self):
        """
        funcion que obtiene el mes
        :return: mes
        """
        return self.mes

    def get_anio(self):
        """
        funcion que obtiene el año
        :return: año
        """
        return self.anio

    def get_dia(self):
        """
        funcion que obtiene el dia
        :return: dia
        """
        return self.dia

    def validar_dia(self, dia):
        """
        funcion que valida el dia del mes en base al mes y año
        :param dia:
        :return: error en caso de que dia no se encuentre en el rango o dia correcto
        """
        meses = {1: 31, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        if not isinstance(dia, int):
            raise ValueError("Valor día debe ser entero")
        if self.mes == 2 and self.es_bisiesto(self.anio):
            if dia < 1 or dia>29:
                raise ValueError("Día debe estar entre 1 y 29")
        elif self.mes == 2 and not self.es_bisiesto(self.anio):
            if dia < 1 or dia>28:
                raise ValueError("Día debe estar entre 1 y 28")
        elif dia < 1 or dia > meses[self.mes]:
            raise ValueError(f"Día debe estar entre 1 y {meses[self.mes]}")
        return dia

    def validar_mes(self, mes):
        """
        funcion que valida el mes, que este sea correcto
        :param mes:
        :return: error si es que el mes no es valido y en caso contrario retorna el mes
        """
        if not isinstance(mes, int):
            raise ValueError("Valor mes debe ser entero")
        if mes < 1 or mes > 12:
            raise ValueError("Mes debe estar entre 1 y 12")
        return mes

    def validar_anio(self, anio):
        """
        funcion que valida el año ingresado
        :param anio:
        :return: error en caso de que el año no sea correcto o el año
        """
        if not isinstance(anio, int):
            raise ValueError("Valor año debe ser entero")
        if anio < 1:
            raise ValueError("Año debe ser mayor a 0")
        return anio

    def calcular_fase(self):
        """
        funcion que obtiene la fase de la luna en base al dia, mes y año
        :return: fase de la luna
        """
        siglos = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
        offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]

        dia = self.dia
        if dia == 31:
            dia = 1
        self.dias_fase = ((siglos[(self.anio + 1) % 19] + ((dia + offsets[self.mes - 1]) % 30) + (self.anio < 1900)) % 30)
        indice = int((self.dias_fase + 2) * 16 / 59.0)
        if indice > 7:
            indice = 7
        self.estado = self.descripciones[indice]
        self.estado_calc = True
        return self.estado

    def obtener_luz(self):
        """
        funcion que obtiene la luz de la fase lunar
        :return: luz en valor de porcentaje en tipo entero
        """
        if not self.estado_calc:
            raise ValueError("Debe calcular la fase de la luna en primer lugar")
        luz = int(2 * self.dias_fase * 100 / 29)
        if luz > 100:
            luz = abs(luz - 200)
        return luz

    def emoji_luna(self):
        """
        función que obtiene un emoji que representa el estado de la fase lunar
        :return: 30 veces el emoji de la fase lunar
        """
        if not self.estado_calc:
            raise ValueError("Debe calcular la fase de la luna en primer lugar")
        emojis = [':crescent_moon:', ':waxing_crescent_moon:', ':first_quarter_moon:',
                  ':waxing_gibbous_moon:', ':full_moon:', ':waning_gibbous_moon:',
                  ':last_quarter_moon:', '	:waning_crescent_moon:']
        print(emoji.emojize(emojis[self.descripciones.index(self.estado)])*30)

