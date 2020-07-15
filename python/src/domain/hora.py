from datetime import timedelta


class Hora:
    """
    """

    def __init__(self, hora: int = 0, minuto: int = 0):
        if not (isinstance(hora, int) and (0 <= hora < 24)):
            raise ValueError("Hora inválida: {0}".format(hora))
        if not (isinstance(minuto, int) and (0 <= minuto < 60)):
            raise ValueError("Minuto inválido: {0}".format(minuto))

        self._hora = hora
        self._minuto = minuto

    @property
    def hora(self):
        return self._hora

    @property
    def minuto(self):
        return self._minuto

    @property
    def timedelta(self) -> timedelta:
        return timedelta(hours=self._hora, minutes=self._minuto)

    @classmethod
    def from_string(cls, string: str):
        string = (''.join([x for x in string if x.isnumeric()])).rjust(4, '0')
        hora = int(string[0:2])
        minuto = int(string[2:4])
        return cls(hora, minuto)

    @classmethod
    def from_timedelta(cls, td: timedelta):
        horas = td.seconds // 3600
        minutos = (td.seconds - horas * 3600)//60

        return cls(horas, minutos)

    def __str__(self):
        return "{0:02d}:{1:02d}".format(self._hora, self._minuto)

    def __repr__(self):
        return "Hora({0},{1})".format(self._hora, self._minuto)

    def __hash__(self):
        return self._hora*1000+self._minuto

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __gt__(self, other):
        return hash(self) > hash(other)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                hash(self) == hash(other))
