import sys
sys.path.append('.')
import random
import unittest
import numpy as np
import pandas as pd
from montecarlo.montecarlo import Die, Game, Analyzer


class AnalyzerTestSuite(unittest.TestCase):
    def setUp(self):
        faces = np.array(['heads', 'tails'], dtype='object')
        self.dice = [Die(faces), Die(faces)]
        self.game = Game(self.dice)
        self.game.play(1000)
        self.analyzer = Analyzer(self.game)


    def test_initializer(self):
        self.assertIsInstance(self.analyzer.game, Game, "Analyzer's game variable should be of type Game")

    def test_jackpot(self):
        num_jackpots = self.analyzer.jackpot() 
        self.assertIsInstance(num_jackpots, int, "Analyzer jackpot should return an int")
        self.assertAlmostEqual(num_jackpots/1000, 0.5, None, "With two coins, prob of jackpit is 1/2", 0.1)

    def test_face_counts(self):
        df = self.analyzer.face_counts()
        self.assertIsInstance(df, pd.DataFrame, "Analyzer face_counts should return a pandas dataframe")
        self.assertAlmostEqual(int(df['tails'].sum()/1000), 0.9, None, "With two coins, prob of jackpit is 1/2", 0.1)

    def test_combo_count(self):
        df = self.analyzer.combo_count()
        self.assertIsInstance(df, pd.DataFrame)
        print(df.loc[('heads', 'tails')])
        self.assertAlmostEqual(df.loc[('heads', 'tails')]['count'].sum()/1000, 0.5, None, "With two coins, prob of jackpit is 1/2", 0.05)


    def test_perm_count(self):
        df = self.analyzer.permutation_count()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertAlmostEqual(df.loc['tailstails']['count'].sum()/1000, 0.25, None, "With two coins, prob of jackpit is 1/2", 0.05)



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
    
    def test_play_length(self):
        results = self.game.play(5)
        self.assertEqual(len(results), 5)

    def test_show(self):
        df = self.game.play(1)
        self.assertIsInstance(df, pd.DataFrame)


class DieTestSuite(unittest.TestCase):
    def setUp(self):
        face_list = ['heads', 'tails']
        faces = np.array(face_list, dtype='object')
        self.die = Die(faces)

    def test_load_faces(self):
        self.assertTrue('heads' in self.die.die['faces'].values)
        self.assertTrue('tails' in self.die.die['faces'].values)
        weights = self.die.die['weights'].to_list()
        self.assertEqual(weights.count(1.0), 2)


    def test_get_state(self):
        die_table = self.die.get_state()

        assert isinstance(die_table, pd.DataFrame)


    def test_bad_face_update_weight(self):
        with self.assertRaises(IndexError) as context:
            self.die.update_weight('edge', 2)

        self.assertTrue("The face edge does not exist in the die" in str(context.exception))


    def test_bad_weight_update_weight(self):
        with self.assertRaises(TypeError) as context:
            self.die.update_weight('heads', 'double')

        self.assertTrue("Expected np.long for weight but got <class 'str'>" in str(context.exception))


    def test_roll_fair(self):
        result_faces = self.die.roll(1000)
        fraction_heads = result_faces.count('heads')/1000

        self.assertAlmostEqual(fraction_heads, 0.5, None, "With 1:1 we should se about 50% heads", 0.05)


    def test_roll_loaded(self):
        self.die.update_weight('heads', 2)
        result_faces = self.die.roll(1000)
        fraction_heads = result_faces.count('heads')/1000

        self.assertAlmostEqual(fraction_heads, 0.66, None, "With 1:2 we should se about 66% heads", 0.05)

if __name__=="__main__":
    unittest.main(verbosity=3)
