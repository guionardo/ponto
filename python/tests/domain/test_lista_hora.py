import unittest
from src.domain import ListaHora, Hora
from datetime import timedelta


class TestListaHora(unittest.TestCase):

    def test_lista_hora(self):
        h1 = Hora(0, 0)
        h2 = Hora(12, 34)
        lista = ListaHora()
        lista.append(h2)
        lista.append(h1)
        lista.append(h1)
        print(str(lista))
        self.assertEqual(len(lista), 2)

        lista = ListaHora(["00:00", h2, timedelta(hours=10, minutes=5)])
        print(str(lista))
        self.assertEqual(len(lista), 3)

    def test_excecoes(self):
        with self.assertRaises(Exception):
            ListaHora([0])

        with self.assertRaises(Exception):
            lista = ListaHora()
            lista.append(None)
