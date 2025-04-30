# DS5100 Final Project: Montecarlo game simulation

This package is a montecarlo simulation on a dice roll game.
You create any number of dice with arbitrary 'faces' then simulate a numnber of rolls of the dice.
Then you can get some analyze the resulting game results to extract combination, permutations and counts.

# Installation
You can install this package with
```bash
pip install git+https://github.com/Niarfe/DS5100_project.git
```

Or simply put `git+https://github.com/Niarfe/DS5100_project.git` in your `requirements.txt` file.

# Using the package
The package provides three classes.  Here's a quick start example of flipping a coin
```python
from montecarlo.montecarlo import Die, Game, Analyzer
import numpy as np

# Create two coins
fair_coin = Die(np.array(['H','T'], dtype='object'))
unfair_coin = Die(np.array(['H','T'], dtype='object'))
# make one of these coins 'unfair'
unfair_coin.update_weight('T', 5)

# Create a game and roll them 1000 times
game_ff = Game([fair_coin, fair_coin])
game_ff.play(1000)

# Create an analyzer and pass it the game object
analyze_ff = Analyzer(game_ff)

# call jackpot and check how many jackpots out of 1000 happened
f_ff = analyze_ff.jackpot()
print(f"Frequency of fair coin jackpots is {f_ff} per 1000")
```

# API synopsis (for more detail use help() on the objects and methods)

`class Die`
* Constructor:  Pass in a python list of np.array with strings or numbers.
* `update_weight(face, weight)`: Change the default weight of a face to make the die 'unfair'
* `roll(ntimes)`: Roll a die `ntimes`.  Defaults to 1
* `get_state()`: retrieve the inner state of the die as a pd.DataFrame

`class Game`
* Constructor: Pass in a python list of np.arrays with faces.  i.e. `[ Die(np.array(['H','T'], dtype='object')),  Die(np.array(['H','T'], dtype='object'))]`
* `play(nrolls)`: Roll the games dice `nroll` times
* `show()`: Retrieve the results of the game as pd.DataFrame
     - pass in `display='wide'` for standard dataframe format
     - pass in `display='narrow'` for a stacked dataframe format

`class Analyzer`
* Constructor: Pass in a played game object
* `jackpot()`: returns an int.  The number of jackpots found.  Jackpot is all faces equal.
* `face_count()`: Returns a pd.DataFrame containing the faces listed with the number of times that face came up.
* `combo_count()`: Returns a pd.DataFrame with the combinations (non-order-dependent) and the number of times each came up
* `permutation_count()`: Returns a pd.Dataframe with the permutations (order-dependent) and the number of times that came up

