import datetime
import os
from pathlib import Path

from gs_config import ConfigClass, ConfigType, DefaultValue

DATE_FMT = '%d/%m/%Y'
CONFIG = None


class Config(ConfigClass):
    REPOSITORIO = ConfigType(env_name='PONTO_REPOSITORIO',
                             type=str,
                             default=os.path.join(str(Path.home()), '.repositorio_ponto'))
    HORAS_POR_DIA = ConfigType(env_name='PONTO_HORAS_POR_DIA',
                               type=float,
                               default=8.0,
                               validation=[4.0, 8.0, 8.8])

    HOJE: str = datetime.datetime.today().strftime(DATE_FMT)


def get_config() -> Config:
    global CONFIG
    if CONFIG:
        return CONFIG
    CONFIG = Config()
    
    return CONFIG
