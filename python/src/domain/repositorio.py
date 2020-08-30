import json
import os
from datetime import date

from src.cross_cutting.config import Config
from src.domain import Hora, ListaHora


class Repositorio:

    def __init__(self, dia: date = date.today()):
        config = Config()
        self._is_ok = False
        if not os.path.isdir(config.REPOSITORIO):
            try:
                os.makedirs(config.REPOSITORIO)
            except Exception as exc:
                print("ERRO NO REPOSITÓRIO: {0}".format(str(exc)))
                return
        self._is_ok = os.path.isdir(config.REPOSITORIO)
        if not self._is_ok:
            return
        self._dias = {}
        self._lista = ListaHora()
        self._file = os.path.join(
            config.REPOSITORIO, dia.strftime('repo_%Y%m.json'))
        self.load()

    @property
    def is_ok(self):
        return self._is_ok

    def load(self):
        self._lista.clear()
        if os.path.isfile(self._file):
            with open(self._file) as f:
                lista = f.read()
            self.from_json(lista)

    def save(self):
        with open(self._file, 'w') as f:
            f.write(self.to_json())

    def add(self, dia: date, hora: Hora):
        dia = self._get_dia(dia)
        dia.append(hora)
        self.save()

    def remove(self, dia: date, hora: Hora):
        dia = self._get_dia(dia)
        dia.remove(hora)
        self.save()

    def _get_dia(self, dia: date) -> ListaHora:
        str_dia = dia.strftime('%Y%m%d')
        if str_dia not in self._dias:
            self._dias[str_dia] = {'marcas': ListaHora()}

        return self._dias[str_dia]['marcas']

    def to_json(self):
        return json.dumps(self._dias, default=str)

    def from_json(self, arg):
        obj = json.loads(arg)
        self._dias.clear()
        for str_dia in obj:
            self._dias[str_dia] = {"marcas": ListaHora()}
            for hora in str_dia.get('marcas', []):
                self._dias[str_dia]['marcas'].append(Hora.from_string(hora))
