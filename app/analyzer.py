import sys
sys.path.append('.')
from app.die import Die
from app.game import Game
import pandas as pd
import numpy as np


from itertools import combinations

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
        df_perms = self.df.apply(lambda x: "_".join(list(x)), axis=1)
        df_perms.value_counts().to_frame()
        return df_perms
