import time

from TTT import TicTacToe, Alpha_Beta_Search, Random_Pick, checkend
from TTTGui import TTTGui

class Controller:
    def __init__(self): # need to have self else you're not instantiating the object.
        self.cut_off_limit = 9
        self.aiStartFirst = True
        self.use_alphaBetaPruning = True

        self.game = TicTacToe(3, 'X', self.cut_off_limit)  # Third param is cut off limit
        self.player = 'O'

        self.GUI = TTTGui(self, 3)  # 3 by 3

    def aiTurn(self):
        print("Old state: ", self.game.state)
        if self.use_alphaBetaPruning:
            t = time.process_time()
            Alpha_Beta_Search(self.game)
            print("Elapsed time for AlphaBetaSearch: ", t - time.process_time())
        else:
            Random_Pick(self.game)
        print("New state: ", self.game.state)

    def updateModel(self, x, y, callback):
        self.game.state[x][y] = 'x' if self.player == 'X' else 'o'
        # resolves a possible AlphaBetaSearch bug
        oldState = self.game.state
        self.game = TicTacToe(3, 'X', self.cut_off_limit)
        self.game.state = oldState
        # put the old state back into the game before running AI turn
        self.aiTurn()

        # Optional boolean causes checkend to return winning coordinates (in a tuple)
        status = checkend(self.game.state, True)
        print("Current winning situation : ", status)
        if status[0]:
            callback(self.game.state, status[1])
        else:
            callback(self.game.state)

    def restart(self, callback):
        self.game = TicTacToe(3, 'X', 6)
        self.game.state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.aiStartFirst = not self.aiStartFirst
        if self.aiStartFirst:
            print("AI will start first.")
            self.aiTurn()
        else:
            print("You go first.")
        callback(self.game.state)


if __name__ == '__main__':
    # load GUI
    controller = Controller() # must have () to create the object, else just class.
    if controller.use_alphaBetaPruning:
        print("AI will use Alpha Beta Pruning.")
    else:
        print("AI will use Random Selection.")
    if controller.aiStartFirst:
        print("AI will start first.")
        controller.aiTurn()
    else:
        print("You go first.")
    controller.GUI.start(controller.game.state)

    # runApp()
