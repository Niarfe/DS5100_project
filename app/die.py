import numpy as np
import pandas as pd


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



