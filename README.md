# Tetris-NeuroEvolution-AI
Tetris clone with Neuro-Evolution of Augmented Typologies Artificial Intelligence as the player<br>
<a href="http://arcade.academy/index.html">Built using Python Arcade Module</a><br>
<a href="http://arcade.academy/examples/tetris.html#tetris">Tetris Code Used</a>
<a href="https://neat-python.readthedocs.io/en/latest/neat_overview.html">NEAT-Python</a>
<a href="https://github.com/ikergarcia1996/NeuroEvolution-Flappy-Bird/blob/master/Jupyter%20Notebook/Flappy.ipynb">Flappy Bird NEAT code used as an example of how to set up the training</a>

Execute Train.py the run.py to see the best AI play the game<br>
Executing Tetris.py will load up a human playable version at a reasonable speed<br>
Use the left and right arrow keys to move horizontally and up and down to rotate<br>
<br>
Training and selection is done in a simulation of tetris that updates much faster than the game loop allows to<br>
The python arcade module does not seem to run along side the neat module, so instead, a pickled<br>
player that meets the specified fitness requirement is loaded to play in the run file<br>
<br>
The AI don't do too great a job at playing tetris, even with the selection process<br>
The highest score after about 3 million simulations was 2 and I only saw the reloaded legends do it once per game at most<br>
The fitness calculation takes into account how much a row was filled if there is more<br>
than one peice in it, which leads to AI that just put two peices per row being selected for<br>
Results weren't better when the fitness function accounted only for row clears<br>
Basically all the AI failed under those conditions<br>
It seems this may be too complicated for the small populations and low amount of generations my machine can handle<br>
<br>
Playing with the "TetrisNEAT" file will change how the topologies are generated and change over time<br>
See the NEAT python documentation for specifics<br>