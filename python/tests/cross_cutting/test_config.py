import unittest

from src.cross_cutting import Config


class TestConfig(unittest.TestCase):

    def test_config(self):
        config = Config()
        print(config.to_dict())
