"""
Montecarlo Game Simulation

This package simulates a montecarlo dice roll game.

There are three classes in the package, Die, Game and Analyzer.

Basic Flow:
    * Create a numpy array(s) of text or numerical symbols.
    * Create a list of Die objects by passing the symbols.
    * Pass this list to a Game object
    * 'play' using the Game object to run the simulation.
    * Pass the Game object to an Analyzer
    * Inspect several aspects of the outcome.

Some notes:
* You can also create 'weighed' dice by using the Game's update_weight function.
* The faces for a set of Die should be the same, however, you can use any
       combination for a set of die.  For example:
           - ['1', '2','3', '4', '5', '6'] # a standard die
           - ['a', 'b', 'c', .... 'z']     # crabble like play
           - ['ace-hearts', 'two-hearts', ... 'king-spades'] # a deck of cards

For more details please see the documentaion for each class and the README.md

"""
from montecarlo.montecarlo import Die, Game, Analyzer
