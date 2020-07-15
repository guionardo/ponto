import unittest
from datetime import timedelta

from src.domain import Hora


class TestHora(unittest.TestCase):

    def test_hora(self):
        hora = Hora.from_string("12:34")
        self.assertEqual(hora.hora, 12)
        self.assertEqual(hora.minuto, 34)
        self.assertEqual(hora.timedelta, timedelta(hours=12, minutes=34))

        hora2 = Hora.from_timedelta(timedelta(hours=0, minutes=0))
        self.assertLess(hora2, hora)
        self.assertGreater(hora, hora2)

        self.assertEqual(str(hora2), '00:00')
        self.assertEqual(repr(hora2), 'Hora(0,0)')

        hora3 = Hora(0, 0)
        self.assertEqual(hora2, hora3)

    def test_excecoes(self):
        with self.assertRaises(Exception):
            Hora(25, 0)

        with self.assertRaises(Exception):
            Hora(0, 61)
