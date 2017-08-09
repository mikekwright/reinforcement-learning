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

