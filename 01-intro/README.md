The Reinforcement Learning Problem
==================================

This is a simple solution that I implemented while going over chapter 1 in the book
Reinforcement Learning.  It basically just goes over a very simple example of using
tic-tac-toe to see how values change and attempts to answers the questions that are
posed at the end of the chapter.  

## Tic Tac Toe

So tic-tac-toe is a pretty simple game overall.  Originally this solution was setup
in order to use OpenAI gym, however tic-tac-toe is not one of their supported
environments (from what I can see on the website).  

### How to play

If you want to just play a quick game of Tic-Tac-Toe against a Random player you can
do so by running this command.  

        python main.py play_game

If you want to play as the second player you can do so by adding the `--p2` command  

        python main.py play_game --p2

### How to train

If you want to go through a training to see the how well it works you can do so
by running this command.  

        python main.py train 10000

The above command will run a train/test that totals to 10000 games.  In this case
player one is a random player and player two is the ai player.  Once this is complete
you should see the output to know how well it played.  

        # This is a sample run of 10000 games (only displays test games which are 10%)
        AI player results - Wins: 907, Draws: 41, Loss: 52
        Total win percentage 90.7

You can also see the values the model created by looking at the generated file  

        less ai-results.json

If you want to run the system where the ai trains against itself, you can do so
with this command.  

        python main.py train 10000 -p1 ai -p2 ai

## Answers to Questions

### Exercise 1.1

Self-Play Suppose, instead of playing against a random opponent, the reinforcement learning
algorithm described above played against itself, with both sides learning. What do you think
would happen in this case? Would it learn a di↵erent policy for selecting moves?  


### Exercise 1.2

Symmetries Many tic-tac-toe positions appear di↵erent but are really the same because of
symmetries. How might we amend the learning process described above to take advantage of this?
In what ways would this change improve the learning process? Now think again. Suppose the
opponent did not take advantage of symmetries. In that case, should we? Is it true, then,
that symmetrically equivalent positions should necessarily have the same value?   

### Exercise 1.3

Greedy Play Suppose the reinforcement learning player was greedy, that is, it always played
the move that brought it to the position that it rated the best. Might it learn to play better,
or worse, than a nongreedy player? What problems might occur?   

### Exercise 1.4

Learning from Exploration Suppose learning updates occurred after all moves, including
exploratory moves. If the step-size parameter is appropriately reduced over time (but not the
tendency to explore), then the state values would converge to a set of probabilities. What are
the two sets of probabilities computed when we do, and when we do not, learn from exploratory
moves? Assuming that we do continue to make exploratory moves, which set of probabilities might
be better to learn? Which would result in more wins?  

### Exercise 1.5

Other Improvements Can you think of other ways to improve the reinforcement learning player?
Can you think of any better way to solve the tic-tac- toe problem as posed?   
