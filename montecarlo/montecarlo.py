import pandas as pd
import numpy as np

class Analyzer:
    def __init__(self, game):
        if not isinstance(game, Game):
            raise ValueError("game should be of type Game")
        self.game = game
        self.df = self.game.show()

    def jackpot(self):
        return int((self.df.nunique(axis=1) == 1).sum())


    def face_counts(self):
        df_counts = self.df.apply(pd.Series.value_counts, axis=1)
        df_counts = df_counts.fillna(0)
        df_counts.index.name = 'roll'
        return df_counts 

    def combo_count(self):
        df_combo = self.df.apply(lambda x: tuple(sorted(x)), axis=1)
        df_count = df_combo.value_counts().to_frame(name='count')
        df_count.index = pd.MultiIndex.from_tuples(df_count.index)
        return df_count 

    def permutation_count(self):
        df_perms = self.df.apply(lambda x: "".join(list(x)), axis=1)
        df_perms.value_counts().to_frame()
        return df_perms


class Game:
    def __init__(self, dice):
        # TODO: optional check that they are all die and have same faces
        assert isinstance(dice, list)
        assert isinstance(dice[0], Die)
        self.dice = dice
        self._rolls = None 

    def play(self, nroll):
        assert isinstance(nroll, int)
        results = {}
        for idx, die in enumerate(self.dice):
            results[idx] = die.roll(nroll)

        self._rolls = pd.DataFrame(results)
        return self._rolls


    def show(self, display='wide'):
        if display not in ['narrow', 'wide']:
            raise ValueError(f"Unrecognized display format {display}")

        if display == 'wide':
            return self._rolls.copy()
        elif display == 'narrow':
            tmp_frame = self._rolls.stack().to_frame(name='results')
            tmp_frame.index.names = ['roll', 'die']
            return tmp_frame
         

class Die:
    def __init__(self, faces):
        assert isinstance(faces, np.ndarray)
        assert len(faces) == len(np.unique(faces)), "faces array must be unique"
        self.weights = np.array([1.0]*len(faces), dtype=int)
        self.die = pd.DataFrame({
            'faces': faces,
            'weights': self.weights
            })


    def update_weight(self, side, weight):
        if side not in self.die['faces'].values:
            raise IndexError(f"The face {side} does not exist in the die")


        if not isinstance(weight, int):
            raise TypeError(f"Expected np.long for weight but got {type(weight)}")

        self.die.loc[self.die.faces == side, 'weights'] = weight


    def roll(self, ntimes=1):
        return [self.die.sample()['faces'].iloc[0] for roll in range(ntimes)]



    def get_state(self):
        return self.die



