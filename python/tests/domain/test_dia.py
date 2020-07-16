import unittest

from src.domain import Dia


class TestDia(unittest.TestCase):

    def test_dia(self):
        dia = Dia()
        self.assertIsInstance(dia, Dia)
