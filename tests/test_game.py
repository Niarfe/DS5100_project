import sys
sys.path.append('.')
import unittest
import numpy as np
import pandas as pd
from app.game import Game 
from app.die import Die 

class GameTestSuite(unittest.TestCase):
    def setUp(self):
        faces = np.array(['heads', 'tails'], dtype='object')
        self.dice = [Die(faces), Die(faces)]
        self.game = Game(self.dice)

    def test_initializer(self):
        self.assertTrue(isinstance(self.game.dice, list))


    def test_play(self):
        results = self.game.play(5)
        self.assertTrue(isinstance(results, pd.DataFrame))


if __name__=="__main__":
    unittest.main(verbosity=3)
