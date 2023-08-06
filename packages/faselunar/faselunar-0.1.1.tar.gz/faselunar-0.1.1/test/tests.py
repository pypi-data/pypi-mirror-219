import unittest
from faseLunar.faselunar import FaseLunar


class FaseLunarTestCase(unittest.TestCase):

    def setUp(self):
        self.f = FaseLunar(19, 5, 1995)

    def test_fase_lunar(self):

        self.f.calcular_fase()

    def test_luz(self):
        self.f.obtener_luz()

    def test_emoji(self):
        self.f.emoji_luna()

if __name__ == '__main__':
    unittest.main()