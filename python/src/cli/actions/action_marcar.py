from src.domain.repositorio import Repositorio
from src.domain import Hora
from datetime import date


def do_marcar(args):
    repositorio = Repositorio()
    if not repositorio.is_ok:
        return

    try:
        hora = Hora.from_string(args.hora)
        dia = args.dia or date.today()
    except Exception as exc:
        print("ERRO: {0}".format(str(exc)))
        return

    repositorio.add(dia, hora)
    print(args)
