from enum import Enum


class EstadoDia(Enum):
    NAO_INICIADO = 0
    INICIADO = 1
    INICIADO_COM_INTERVALO = 2
    INTERVALO_INICIADO = 4
    NAO_TERMINADO = 8
    TERMINADO = 16
    TERMINADO_HORA_EXTRA = 32


ESTADO_DESCRICAO = {
    EstadoDia.NAO_INICIADO: 'Não iniciado',
    EstadoDia.INICIADO: 'Iniciado',
    EstadoDia.INICIADO_COM_INTERVALO: 'Iniciado + Intervalo',
    EstadoDia.INTERVALO_INICIADO: 'Intervalo iniciado',
    EstadoDia.NAO_TERMINADO: 'Não terminado',
    EstadoDia.TERMINADO: 'Terminado',
    EstadoDia.TERMINADO_HORA_EXTRA: 'Terminado (HE)'
}
