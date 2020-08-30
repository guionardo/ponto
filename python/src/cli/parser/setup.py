import argparse
import datetime

from src import __description__, __tool_name__, __version__
from src.cli.actions import do_desmarcar, do_hoje, do_marcar


def setup_marcar(subparser: argparse.ArgumentParser):
    marcar = subparser.add_parser("marcar")
    marcar.add_argument("hora", help="Hora hh:mm")
    marcar.add_argument('-d', '--dia', help="Dia dd/mm/aaaa",
                        default=datetime.date.today())
    marcar.set_defaults(func=do_marcar)


def setup_desmarcar(subparser: argparse.ArgumentParser):
    desmarcar = subparser.add_parser("desmarcar")
    desmarcar.add_argument('hora', help="Hora hh:mm")
    desmarcar.set_defaults(func=do_desmarcar)


def setup_hoje(subparser: argparse.ArgumentParser):
    hoje = subparser.add_parser('hoje')
    _hoje = datetime.date.today().strftime('%d/%m/%Y')

    hoje.add_argument('-d', '--dia', help="Dia dd/mm/aaaa",
                      default=_hoje)
    hoje.set_defaults(func=do_hoje)


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=__tool_name__,
                                     description=__description__)

    parser.add_argument('--version', action='version',
                        version='%(prog)s '+__version__)

    subparser = parser.add_subparsers()
    setup_marcar(subparser)
    setup_desmarcar(subparser)
    setup_hoje(subparser)

    return parser
