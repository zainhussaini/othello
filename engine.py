import numpy as np

class OthelloBoard:
  def __init__(self):
    board = [['.' for _ in range(8)] for _ in range(8)]
    board[3][3] = 'w'
    board[3][4] = 'b'
    board[4][3] = 'b'
    board[4][4] = 'w'
    self.board = board

    self.player = 'b'
    # print(f"{self.player}'s turn")

  def show(self):
    for i in range(8):
      print(' '.join(self.board[i]))
    print()

  def opposite_player(self):
    if self.player == 'b':
      return 'w'
    if self.player == 'w':
      return 'b'

  def __change_player(self):
    self.player = self.opposite_player()

  def check_moves_available(self):
    for x in range(8):
      for y in range(8):
        if self.board[x][y] == '.':
          # all 8 directions to look
          directions = [[-1, -1], [0, -1], [1, -1],
                        [-1, 0], [1, 0],
                        [-1, 1], [0, 1], [1, 1]]
          for (xd, yd) in directions:
            i = 1
            while True:
              # check bounds
              if x + i*xd < 0 or x + i*xd > 7 or y + i*yd < 0 or y + i*yd > 7:
                break

              # check for empty space
              if self.board[x + i*xd][y + i*yd] == '.':
                break

              # keep looking in direction
              if self.board[x + i*xd][y + i*yd] == self.opposite_player():
                i += 1
                continue

              # found end of search, fill in line
              if self.board[x + i*xd][y + i*yd] == self.player:
                if i == 1:
                  break

                return True
    return False

  def play(self, x, y):
    if self.board[x][y] != '.':
      # print("hey you can't put a piece there")
      return self.player

    # all 8 directions to look
    directions = [[-1, -1], [0, -1], [1, -1],
                  [-1, 0], [1, 0],
                  [-1, 1], [0, 1], [1, 1]]

    valid_move_made = False

    for (xd, yd) in directions:
      i = 1
      while True:
        # check bounds
        if x + i*xd < 0 or x + i*xd > 7 or y + i*yd < 0 or y + i*yd > 7:
          break

        # check for empty space
        if self.board[x + i*xd][y + i*yd] == '.':
          break

        # keep looking in direction
        if self.board[x + i*xd][y + i*yd] == self.opposite_player():
          i += 1
          continue

        # found end of search, fill in line
        if self.board[x + i*xd][y + i*yd] == self.player:
          if i == 1:
            break

          valid_move_made = True
          for j in range(0, i):
            self.board[x + j*xd][y + j*yd] = self.player
          break

    # Tell player that they didn't make a valid move and
    # they have to try again.
    if not valid_move_made:
      # print("invalid move attempted!")
      # print(f"{self.player}'s turn")
      return self.player

    # print(f"{self.player} made move")
    # self.show()
    self.__change_player()
    
    # Next player has moves available so they should go.
    if self.check_moves_available():
      return self.player
    
    # print(f"{self.player} has no moves available")
    self.__change_player()
    
    # Next player had no moves available so back to the past samurai jack.
    if self.check_moves_available():
      # print(f"{self.player}'s turn again")
      return self.player

    # No one has moves available, this is a truly happy moment.
    # print("GAME OVER!")
    return None

  def count_board(self):
    w_count = 0
    b_count = 0
    for x in range(8):
      for y in range(8):
        if self.board[x][y] == 'w':
          w_count += 1
        elif self.board[x][y] == 'b':
          b_count += 1
    # print(f"b score: {b_count}")
    # print(f"w score: {w_count}")
    if w_count > b_count:
      # print("WINNER IS w")
      return 'w'
    elif w_count < b_count:
      # print("WINNER IS b")
      return 'b'
    else:
      # print("IT'S A TIE")
      return 'tie'
      


if __name__ == "__main__":
  wins = {}
  for _ in range(1000):
    board = OthelloBoard()
    player = board.player

    # keep playing until you get None which means game ended.
    while player:
      x = np.random.randint(0, 8)
      y = np.random.randint(0, 8)
      player = board.play(x, y)
    
    winner = board.count_board()
    if winner in wins:
      wins[winner] += 1
    else:
      wins[winner] = 1

  print(wins)
