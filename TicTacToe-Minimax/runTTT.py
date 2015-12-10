from TTT import TicTacToe, Alpha_Beta_Search, checkend
from TTTGui import TTTGui

class Controller:
    def __init__(self): # need to have self else you're not instantiating the object.
        self.game = TicTacToe(3, 'X', 3)  # Third param is cut off limit
        self.player = 'O'

        self.GUI = TTTGui(self, 3)  # 3 by 3

    def aiTurn(self):
        print("Old state: ", self.game.state)
        Alpha_Beta_Search(self.game)
        print("New state: ", self.game.state)

    def updateModel(self, x, y, callback):
        self.game.state[x][y] = 'x' if self.player == 'X' else 'o'
        # resolves a possible AlphaBetaSearch bug
        oldState = self.game.state
        self.game = TicTacToe(3, 'X', 3)
        self.game.state = oldState
        # put the old state back into the game before running AI turn
        self.aiTurn()

        # Optional boolean causes checkend to return winning coordinates (in a tuple)
        status = checkend(self.game.state, True)
        print("Current winning situation : ", status)
        if status[0]: #
            callback(self.game.state, status[1])
        else:
            callback(self.game.state)

    def restart(self, callback):
        self.game = TicTacToe(3, 'X', 6)
        self.game.state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        callback(self.game.state)


if __name__ == '__main__':
    # load GUI
    controller = Controller() # must have () to create the object, else just class.

    controller.GUI.start()

    # runApp()
