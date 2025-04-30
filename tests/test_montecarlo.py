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
        """
        Given an initialized Analyzer object 
        When I check it's internal game variable and check what type of object it is
        Then I should find it is of type Game
        """
        self.assertIsInstance(self.analyzer.game, Game, "Analyzer's game variable should be of type Game")

    def test_jackpot(self):
        """
        Given an Analyzer object intialized with a played Game with two coins
          And the coins have equal weights
          And it has been played with 1000 rolls
        When I request the number of jackpots
        Then the jackpot function should return an int
          And I should find that the number of jackpots should be approximately 50%

        NOTE:  With two dice, there are four outcomes per roll, two of which give you the jackpot.
                   heads/heads and tails/tails.  So that's 2 out of 4, or 50%
        """
        num_jackpots = self.analyzer.jackpot() 
        self.assertIsInstance(num_jackpots, int, "Analyzer jackpot should return an int")
        self.assertAlmostEqual(num_jackpots/1000, 0.5, None, "With two coins, prob of jackpit is 1/2", 0.1)

    def test_face_counts(self):
        """
        Given an Analyzer object intialized with a played Game with two coins
          And the coins have equal weights
          And it has been played with 1000 rolls
        When I request the fact counts
          And take the sum of the tails
        Then the face_counts method should return a pd.DataFrame
          And the number of tails should be aproximately 50%
        """
        df = self.analyzer.face_counts()
        self.assertIsInstance(df, pd.DataFrame, "Analyzer face_counts should return a pandas dataframe")
        self.assertAlmostEqual(int(df['tails'].sum()/1000), 0.9, None, "Given fair dice, about half the faces should be tails", 0.2)

    def test_combo_count(self):
        """
        Given an Analyzer object intialized with a played Game with two coins
          And the coins have equal weights
          And it has been played with 1000 rolls
        When I request the combo counts
          And take the sum of the ('heads','tails') combination
        Then the combo_counts method should return a pd.DataFrame
          And the number of ('heads',, 'tails') should be aproximately 50%
        """
        df = self.analyzer.combo_count()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertAlmostEqual(df.loc[('heads', 'tails')]['count'].sum()/1000, 0.5, None, "With two coins combination 'heads', 'tails' is should be about 1/2", 0.05)

    def test_perm_count(self):
        """
        Given an Analyzer object intialized with a played Game with two coins
          And the coins have equal weights
          And it has been played with 1000 rolls
        When I request the permutation counts
          And take the sum of the 'tailstails' permutation 
        Then the perm_counts method should return a pd.DataFrame
          And the number of 'tailstails' should be aproximately 25%
        """
        df = self.analyzer.permutation_count()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertAlmostEqual(df.loc['tailstails']['count'].sum()/1000, 0.25, None, "With two coins the permutation shoudl be about 1/4 ", 0.05)



class GameTestSuite(unittest.TestCase):
    def setUp(self):
        faces = np.array(['heads', 'tails'], dtype='object')
        self.dice = [Die(faces), Die(faces)]
        self.game = Game(self.dice)

    def test_initializer(self):
        """
        Given an Game object intialized with two coins
        When I check the type of the dice
        Then the type should match 'list'
        """
        self.assertTrue(isinstance(self.game.dice, list))


    def test_play(self):
        """
        Given an Game object intialized with two coins
          And I roll it 5 times
        When I check the type of the results
        Then I should find the type of the result is a pd.DataFrame
        """
        results = self.game.play(5)
        self.assertTrue(isinstance(results, pd.DataFrame))
    
    def test_play_length(self):
        """
        Given an Game object intialized with two coins
          And I roll it 5 times
        When I check the type of the results
        Then I should find the length of the dataframe to be 5 
        """
        results = self.game.play(5)
        self.assertEqual(len(results), 5)

    def test_show(self):
        """
        Given an Game object intialized with two coins
        When I roll the die once
        Then I should find the result of the play to be of type pd.DataFrame
        """
        df = self.game.play(1)
        self.assertIsInstance(df, pd.DataFrame)


class DieTestSuite(unittest.TestCase):
    def setUp(self):
        face_list = ['heads', 'tails']
        faces = np.array(face_list, dtype='object')
        self.die = Die(faces)

    def test_load_faces(self):
        """
        Given a die initalized with a coin (two faces 'heads', 'tails')
        When I check for the face values and weights
        Then I should find
          one heads face
          one tails face
          two 1.0 weights
        """
        self.assertTrue('heads' in self.die.die['faces'].values)
        self.assertTrue('tails' in self.die.die['faces'].values)
        weights = self.die.die['weights'].to_list()
        self.assertEqual(weights.count(1.0), 2)


    def test_get_state(self):
        """
        Given a die initalized with a coin (two faces 'heads', 'tails')
        When I call the get_state method 
        Then I should find that the type returned is a pd.DataFrame 
        """
        die_table = self.die.get_state()

        assert isinstance(die_table, pd.DataFrame)


    def test_bad_face_update_weight(self):
        """
        Given a die initalized with a coin (two faces 'heads', 'tails')
        When I update one of the weights with a non-existing face 
        Then I should find the method returns an IndexError
          And a message indicting the face was not fund
        """
        with self.assertRaises(IndexError) as context:
            self.die.update_weight('edge', 2)

        self.assertTrue("The face edge does not exist in the die" in str(context.exception))


    def test_bad_weight_update_weight(self):
        """
        Given a die initalized with a coin (two faces 'heads', 'tails')
        When I update one of the weights with a non-valid weight (not a number type) 
        Then I should find the method returns a TypeError
          And gives a message stating it got the wrong type for weight
        """
        with self.assertRaises(TypeError) as context:
            self.die.update_weight('heads', 'double')

        self.assertTrue("Expected np.long for weight but got <class 'str'>" in str(context.exception))


    def test_roll_fair(self):
        """
        Given a die initalized with a coin (two faces 'heads', 'tails')
        When I roll the die 1000 times
          And I check the fraction of times heads comes up
        Then I should find the fraction to be approximately 50%
        """
        result_faces = self.die.roll(1000)
        fraction_heads = result_faces.count('heads')/1000

        self.assertAlmostEqual(fraction_heads, 0.5, None, "With 1:1 we should se about 50% heads", 0.05)


    def test_roll_loaded(self):
        """
        Given a die initalized with a coin (two faces 'heads', 'tails')
          And I set one of the dice to a weight of 2 (default 1)
        When I roll the dice 1000 times
          And I check the fraction of times heads comes up
        Then I should find the fraction to be approximately 66%
        """
        self.die.update_weight('heads', 2)
        result_faces = self.die.roll(1000)
        fraction_heads = result_faces.count('heads')/1000

        self.assertAlmostEqual(fraction_heads, 0.66, None, "With 1:2 we should se about 66% heads", 0.05)

if __name__=="__main__":
    unittest.main(verbosity=3)
