import sys
sys.path.append('.')
import unittest
import numpy as np
import pandas as pd
from app.die import Die

class DieTestSuite(unittest.TestCase):
    def setUp(self):
        face_list = ['heads', 'tails']
        faces = np.array(face_list, dtype='object')
        self.die = Die(faces)

    def test_load_faces(self):
        self.assertTrue('heads' in self.die.die['faces'].values)
        self.assertTrue('tails' in self.die.die['faces'].values)
        # TODO: check the weights are both there and are 1.0

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

if __name__=="__main__":
    unittest.main(verbosity=3)
