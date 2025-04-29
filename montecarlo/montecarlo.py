"""
Montecarlo module

Contains the main classes to play the montecarlo simulation

Die        Simulated die/card-deck
Game       Simulates rolling the die and capturing results
Analyzer   Provides analytics on the results of a game object

Please see the help strings for the classes/methods for more details
"""
import pandas as pd
import numpy as np

class Analyzer:
    """
    Inspect a played Game object and extract results

    Initializer arguments:
        game           Game object which has been played

    METHODS            RETURNS
    jackpot            int, A count of times the die all returned the same face
    face_counts        dataframe, Counts of how many times each face came up in the rolls
    combo_count        dataframe, Counts of how many combinations (non-ordered) came up
    permuation_count   dataframe, Counts of how many combinations, ordered, came up.

    For more details please see the help() on each of the methods
    """
    def __init__(self, game):
        """
        Extracts measurements from a played game for analysis

        INPUT:
            game        Game, a Game object that has been been played
        """
        if not isinstance(game, Game):
            raise ValueError("game should be of type Game")
        self.game = game
        self.df = self.game.show()

    def jackpot(self):
        """
        Calculate how many rolls of the dies in a Game object hit a jackpot.

        A jackpot is defined as a roll where all the die came up with the same face.

        INPUT:
            None
        RETURNS:
            int, the number of jackpots found in all the rolls.
        """
        return int((self.df.nunique(axis=1) == 1).sum())


    def face_counts(self):
        """
        Calculate how many times a face came up during the play

        INPUT:
            None
        RETURNS:
           pd.DataFrame, with
        """
        df_counts = self.df.apply(pd.Series.value_counts, axis=1)
        df_counts = df_counts.fillna(0)
        df_counts.index.name = 'roll'
        return df_counts

    def combo_count(self):
        """
        Calculate the different combinations from a game of dice

        A combination is order independent, so ABC is the same as BCA, CAB etc.

        INPUT:
            None
        RETURNS:
            pd.DataFrame  containing a multi index for the face values and column with
                              the counts
        """
        df_combo = self.df.apply(lambda x: tuple(sorted(x)), axis=1)
        df_count = df_combo.value_counts().to_frame(name='count')
        df_count.index = pd.MultiIndex.from_tuples(df_count.index)
        return df_count

    def permutation_count(self):
        """
        Calculate the different combinations from a game of dice

        A permutation is order dependent, so ABC is NOT the same as BCA, CAB etc.
            Each order dependent combination has it's own count

        Permutations are stored as a strung together set of values.  For example,
        a set of resulting faces ['W', 'O', 'R', 'D'] is reported as permutation 'WORD' 

        INPUT:
            None
        RETURNS:
            pd.DataFrame  containing a multi index for the permutations and column with the counts
        """
        df_perms = self.df.apply(lambda x: "".join(list(x)), axis=1)
        df_perms = df_perms.value_counts().to_frame()
        df_perms.index.name = 'perm'
        return df_perms


class Game:
    """
    Simulates game play by 'rolling' a set of dice

    There are two main methods:
        play     Rolls the set of dice a given number of times and stores all the results
                    in a pandas dataframe

        show     Returns the pandas dataframe with the current state of play
    """
    def __init__(self, dice):
        """
        INPUT:
            dice     list<Die>, a list of dice all configured with the same face values
        """
        assert isinstance(dice, list)
        assert isinstance(dice[0], Die)
        self.dice = dice
        self._rolls = None

    def play(self, nroll):
        """
        Iterates through the list of dice and 'rolls' them a given number of N times.

        INPUT:
            nroll    int, the number of times to roll the set of dice
        RETURNS:
            pd.DataFrame    Contains one row per roll, where each roll has the roll number
                                and the resulting faces per roll
        """
        assert isinstance(nroll, int)
        results = {}
        for idx, die in enumerate(self.dice):
            results[idx] = die.roll(nroll)

        self._rolls = pd.DataFrame(results)
        return self._rolls


    def show(self, display='wide'):
        """
        Returns the internal state of results from a roll in either plain format or
            a wide format (stacked)

        INPUT:
            display    string, 'wide' for standard format, 'narrow' for stacked
        RETURNS:
            pd.DataFrame    The dataframe in the format specfied
        """
        if display not in ['narrow', 'wide']:
            raise ValueError(f"Unrecognized display format {display}")

        if display == 'wide':
            return self._rolls.copy()

        tmp_frame = self._rolls.stack().to_frame(name='results')
        tmp_frame.index.names = ['roll', 'die']
        return tmp_frame


class Die:
    """
    Stores a set of faces and weights representing a die, deck of cards or other
        'rollable'.  Rollable meaning that one face will be 'up' after one roll.
        The initial state is for all faces to have a default weight of 1.
        Weights can be updated to make a particular face 'heavier' by altering it's weight.
        Thereafter when a die is rolled, the weighed face has a higher chance of coming 'up'

    Note that when a die is rolled it's internal structure is not altered.  It simply
        returns a list of faces that came up.  It's internal state, (faces, weights)
        remains the same.
    """
    def __init__(self, faces):
        """
        Intanciates a die from a given set of faces representing a die

        INPUT:
            faces    np.array, a numpy array containing strings or numbers for the die faces
                        e.g. faces = np.array(['heads', 'tails'], dtype='object')

        NOTE: The face values must be unique.  I.e. ['heads', 'heads', tails'] rould result
                   in an exception thrown when creating a die

        """
        assert isinstance(faces, np.ndarray)
        assert len(faces) == len(np.unique(faces)), "faces array must be unique"
        self.weights = np.array([1.0]*len(faces), dtype=int)
        self.die = pd.DataFrame({
            'faces': faces,
            'weights': self.weights
            })


    def update_weight(self, side, weight):
        """
        Modify the default weights (1.0) of a face

        INPUTS:
            side     string, the face to be modified
            weight   float,  the new weight to be associated with the face
        """
        if side not in self.die['faces'].values:
            raise IndexError(f"The face {side} does not exist in the die")


        if not isinstance(weight, int):
            raise TypeError(f"Expected np.long for weight but got {type(weight)}")

        self.die.loc[self.die.faces == side, 'weights'] = weight


    def roll(self, ntimes=1):
        """
        'Roll' the dice specified number of times (default 1)

        INPUTS:
            ntimes   int, the number of times to roll the die
        RETURNS:
            list, a list contining the face result for each time the die was rolled
        """
        return np.random.choice(
                self.die['faces'],
                size=ntimes,
                replace=True,
                p=self.die['weights'] / self.die['weights'].sum()
                ).tolist()


    def get_state(self):
        """
        Access the internal state of the die stored in a pd.DataFrame
        
        INPUTS:
            None

        RETURNS:
            pd.DataFrame   self.die, the internal dataframe holding the face values and weights            
        """
        return self.die
