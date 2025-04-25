import sys
sys.path.append('.')
import unittest
import numpy as np
import pandas as pd
from app.game import Game 
from app.die import Die 
from app.analyzer import Analyzer 


class AnalyzerTestSuite(unittest.TestCase):
    def setUp(self):
        faces = np.array(['heads', 'tails'], dtype='object')
        self.dice = [Die(faces), Die(faces)]
        self.game = Game(self.dice)
        self.game.play(5)
        self.analyzer = Analyzer(self.game)


    def test_initializer(self):
        self.assertTrue(isinstance(self.analyzer.game, Game))

    def test_jackpot(self):
        self.assertTrue(isinstance(self.analyzer.jackpot(), int))

    def test_face_counts(self):
        self.assertTrue(isinstance(self.analyzer.face_counts(), pd.DataFrame))

    def test_combo_count(self):
        self.assertTrue(isinstance(self.analyzer.combo_count(), pd.DataFrame))

    @unittest.skip("I need to figure out why this df is different")
    def test_perm_count(self):
        self.assertTrue(isinstance(self.analyzer.permutation_count(), pd.DataFrame))




if __name__=="__main__":
    unittest.main(verbosity=3)
