from src.exceptions import ListaHoraException
from datetime import timedelta
from .hora import Hora


class ListaHora(list):

    def __init__(self, *args, **kwargs):
        if args:
            for i, item in enumerate(args[0]):
                if isinstance(item, str):
                    item = Hora.from_string(item)
                elif isinstance(item, timedelta):
                    item = Hora.from_timedelta(item)
                elif not isinstance(item, Hora):
                    raise TypeError(
                        "Expected str, timedelta or Hora type. Received '"+str(item.__class__)+"'")
                args[0][i] = item
        super().__init__(*args, **kwargs)
        self._sort()

    def _sort(self):
        self.sort(key=lambda item: hash(item))

    def append(self, item: Hora):
        if not isinstance(item, Hora):
            raise TypeError(
                "Expected type Hora for item. Received '"+str(item.__class__)+"'")
        if self.index(item) > -1:
            return
        super().append(item)
        self._sort()

    def index(self, item: Hora, start=0, stop=99999):
        for i, h in enumerate(self):
            if (start <= i <= stop) and h == item:
                return i
        return -1

    def __str__(self):
        return str([str(h) for h in self])
