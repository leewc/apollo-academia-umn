from TTT import TicTacToe, Alpha_Beta_Search
from TTTGui import TTTGui

class Controller:
    def __init__(self): # need to have self else you're not instantiating the object.
        self.game = TicTacToe(3, 'X', 3)
        self.game.state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player = 'X'

        self.GUI = TTTGui(self, 3)  # 3 by 3

    def aiTurn(self):
        print("Old state: ", self.game.state)
        Alpha_Beta_Search(self.game)
        print("New state: ", self.game.state)

    def updateModel(self, x, y):
        print("Model update fired.  ",x, y)
        self.game.state[x][y] = 'x' if self.player == 'X' else 'o'
        self.aiTurn()


if __name__ == '__main__':
    # load GUI
    controller = Controller() # must have () to create the object, else just class.

    controller.GUI.start()

    # runApp()
