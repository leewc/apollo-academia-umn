# Summary

We decided to implement the minimax and alpha-beta pruning algorithms for the simple Tic Tac Toe game. The project was decided in a fashion where the UI and the algorithms are in separate files and are separated in terms of purpose (Model-View-Controller).

Our game starts with the AI making the move first, upon restart, the human player will start first (turns are alternated between the AI and the player).

The Alpha-beta pruning algorithm is executed whenever the AI is required to make the ‘best move’, that minimizes losses, and maximizes wins. The algorithm is provided with the board state for evaluation.

We have also written an algorithm where the AI plays randomly by selecting empty boxes in the Tic Tac Toe game.

# Usage

Run the program by executing:

    python3 runTTT.py

**Tkinter must be installed for the GUI to execute.**

Installation of Tkinter for Python3 for Macs can be found at:
https://www.python.org/download/mac/tcltk/

Installation of Tkinter for Python3 for Debian:
    sudo apt-get install python3-tk

Note: Tkinter should be included in Windows installations of Python.
Note: The game was designed on a Linux machine, there may be differences in TKInter versions that cause no color on the X’s and O’s, or differently styled buttons.
