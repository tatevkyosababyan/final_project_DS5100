import unittest
import pandas
import numpy as np
from montecarlo import Die as d
from montecarlo import Game as g
from montecarlo import Analyzer as a

class DieTestSuite(unittest.TestCase):
    def test_1_change(self):
        test_Die = d([1,2,3,4,5])
        test_Die.change(3,7)
        test = (test_Die._df[test_Die._df['Faces']==3].Weights.values[0]==1)
        message = "The weight value was not changed"
        self.assertFalse(test, message)
    
    def test_2_roll(self):
        test_Die = d([1,2,3,4,5])
        roll_output = (len(test_Die.roll(4))==4)
        message = "Number of rolls is incorrect"
        self.assertTrue(roll_output,  message)
    
    def test_3_show(self):
        test_Die = d([1,2,3,4,5])
        show_output_type = (type(test_Die.show())== pandas.core.frame.DataFrame)
        message = "The output is not a dataframe"
        self.assertTrue(show_output_type, message)


class GameTestSuite(unittest.TestCase):
    def test1_play(self):
        die1 = d([1,2,3,4,5])
        die2 = d([1,2,3,4,5])
        game = [die1, die2]
        test_game = g(game)
        test_game.play(4)
        play_output_length = (len(test_game._result)==4)
        message = "Number of rolls is incorrect"
        self.assertTrue(play_output_length,  message)

    def test2_show(self):
        die1 = d([1,2,3,4,5])
        die2 = d([1,2,3,4,5])
        game = [die1, die2]
        test_game = g(game)
        show_output_type = (type(test_game.show())== pandas.core.frame.DataFrame and type(test_game.show('narrow'))== pandas.core.series.Series) 
        message = "The output is not a dataframe"
        self.assertTrue(show_output_type, message)

class AnalyzerTestSuite(unittest.TestCase):
    def test1_jackpot(self):
        die1 = d([1,1,1])
        die2 = d([1,1,1])
        game = [die1, die2]
        test_game = g(game)
        test_game.play(2)
        test_a = a(test_game)
        jackpot_output = (test_a.jackpot() == 2)
        message = "Number of jackpots is incorrect"
        self.assertTrue(jackpot_output,  message)


    def test2_combo(self):
        die1 = d([1,1,1])
        die2 = d([1,1,1])
        game = [die1, die2]
        test_game = g(game)
        test_game.play(2)
        test_a = a(test_game)
        combo_output = (len(test_a.combo()) == 1)
        message = "Number of combinations is incorrect"
        self.assertTrue(combo_output,  message)

    def test3_faces_count_per_roll(self):
        die1 = d([1,2,3])
        die2 = d([1,2,3])
        game = [die1, die2]
        test_game = g(game)
        test_game.play(2)
        test_game.show().loc[3,[1,2,3]] = [1,2,3]
        test_a = a(test_game)
        test_faces = test_a.face_counts_per_roll()
        res = (False in (test_faces.loc[3].values == 0))
        message = "Number of faces count per roll is incorrect"
        self.assertTrue(res,  message)
















if __name__ == '__main__': 

    unittest.main(verbosity=3) 