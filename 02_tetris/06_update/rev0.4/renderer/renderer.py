class Renderer():
    def __init__(self):
        pass

    def draw(self, board):
    # def draw_board(self, board):
        '''Draw the board on the console.

        Display empty cells as "□"
        and blocks as "■".

        Args:
            board (list):
                Board data to draw.

        Returns:
            None
        '''
        # print("[proc] draw_board")
        for row in board:
            line = ""

            for cell in row:
                if cell == 0:
                    line += "□"
                else:
                    line += "■"
            print(line)
