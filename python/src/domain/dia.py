from datetime import datetime, timedelta

from src.cross_cutting import get_config, Config
from src.cross_cutting.utils import now_as_timedelta
from src.enums import ESTADO_DESCRICAO, EstadoDia

from .hora import Hora
from .lista_hora import ListaHora


class Dia:

    def __init__(self, from_dict: dict = None, dia: datetime = None):
        self._marcas = ListaHora()
        self._hoje: datetime = datetime.today() if not isinstance(dia, datetime) else dia
        self._htrab: timedelta = timedelta()
        self._hint: timedelta = timedelta()
        self._config: Config = get_config()
        self._horas_por_dia = timedelta(hours=self._config.HORAS_POR_DIA)

        if from_dict:
            self.from_dict(from_dict)

    @property
    def hoje(self) -> datetime:
        return self._hoje

    @property
    def horas_trabalhadas(self) -> timedelta:
        return self._htrab

    @property
    def horas_trabalhadas_ate_agora(self) -> timedelta:
        if self.estado is EstadoDia.NAO_TERMINADO \
                or self.estado is EstadoDia.INICIADO:
            ht = now_as_timedelta()
            ultima_marca = self._marcas[-1].timedelta
            ht = ht - ultima_marca
            ht = ht + self.horas_trabalhadas
            return ht

    @property
    def horas_intervalo(self) -> timedelta:
        return self._hint

    @property
    def tempo_atual_intervalo(self) -> timedelta:
        if self.estado is EstadoDia.INTERVALO_INICIADO:
            return timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime) - self._marcas[-1].timedelta()

        return timedelta()

    @property
    def tempo_estimado_retorno_intervalo(self) -> timedelta:
        if self.estado is EstadoDia.INTERVALO_INICIADO:
            return self._marcas[-1] + timedelta(hours=1)

    @property
    def estado(self) -> EstadoDia:
        n_marcas = len(self._marcas)
        if n_marcas == 0:
            return EstadoDia.NAO_INICIADO
        if n_marcas == 1:
            return EstadoDia.INICIADO

        if self.horas_intervalo.total_seconds() > 0:
            if len(self._marcas) % 2 == 0:
                if self.horas_trabalhadas <= self.self._horas_por_dia:
                    return EstadoDia.TERMINADO
                else:
                    return EstadoDia.TERMINADO_HORA_EXTRA
            return EstadoDia.INICIADO_COM_INTERVALO
        elif len(self._marcas) > 2 and len(self._marcas) % 2 == 1:
            return EstadoDia.INTERVALO_INICIADO

        return EstadoDia.NAO_TERMINADO

    @property
    def hora_magica(self) -> Hora:
        estado = self.estado
        if estado.value < EstadoDia.INICIADO_COM_INTERVALO.value:
            return Hora()

        ind_ultima_entrada = len(self._marcas) - \
            (1 if estado is EstadoDia.INICIADO_COM_INTERVALO else 2)

        ultima_entrada = self._marcas[ind_ultima_entrada]

        if estado is EstadoDia.INICIADO_COM_INTERVALO:
            hora_magica = ultima_entrada.timedelta + \
                self._horas_por_dia - self.horas_trabalhadas
        else:
            hora_magica = ultima_entrada.timedelta + \
                self.horas_trabalhadas - self._horas_por_dia

        return Hora.from_timedelta(hora_magica)

    @property
    def descricao(self) -> str:
        return ''.join([
            ESTADO_DESCRICAO[self.estado],
            ' '+str(self._marcas),
            '' if self.horas_trabalhadas.total_seconds() <= 0 else ' Trabalhadas: ' +
            str(self.horas_trabalhadas),
            '' if self.horas_intervalo.total_seconds() <= 0 else ' Intervalo: ' +
            str(self.horas_intervalo),
            '' if self.horas_atividades.total_seconds() <= 0 else ' Atividades: ' +
            str(self.horas_atividades),
            '' if not(1 < self.estado.value <
                      8) else ' Hora Mágica: '+str(self.hora_magica)
        ])

    @property
    def marcas(self) -> ListaHora: return self._marcas

    def marcar(self, hora: Hora):
        if self._marcas.add(hora):
            self.update_valores()
            return True

    def desmarcar(self, hora: Hora):
        if self._marcas.remove(hora):
            self.update_valores()
            return True

    def update_valores(self):
        self.update_horas_trabalhadas()
        self.update_intervalos()

    def update_horas_trabalhadas(self):
        if len(self._marcas) == 0:
            self._htrab = timedelta()
            return

        ht = timedelta()
        for i, h in enumerate(self._marcas):
            if i % 2 == 0:
                ult_hora = h
            else:
                ht += h.timedelta - ult_hora.timedelta

        self._htrab = ht

    def update_horas_atividades(self):
        if len(self._atividades) == 0:
            self._hatv = timedelta()
            return

        ha = timedelta()
        for atividade in self._atividades:
            ha += atividade.duracao.timedelta

        self._hatv = ha

    def update_intervalos(self):
        if len(self._marcas) == 0:
            self._hint = timedelta()
            return

        hi = timedelta()
        ult_hora: Hora = None
        for i, h in enumerate(self._marcas):
            if i % 2 == 0 and i > 0:
                hi += h.timedelta - ult_hora.timedelta
            elif i % 2 == 1:
                ult_hora = h

        self._hint = hi

    def to_dict(self):
        return {
            'dia': self._hoje.strftime('%Y-%m-%d'),
            'horas': [str(marca) for marca in self._marcas],
        }

    def from_dict(self, from_dict: dict):
        self._hoje = datetime.strptime(from_dict['dia'], '%Y-%m-%d')
        self._marcas.clear()
        for hora in from_dict['horas']:
            self.marcar(Hora.from_string(hora))
