import sys
sys.path.append(',')
from app.die import Die
import pandas as pd
import numpy as np


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
         


