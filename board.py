import copy
import numpy as np


class Board:
    def __init__(self, h=6, w=7):
        self.h = h
        self.w = w
        self.board = np.zeros((h, w), dtype=np.int8)
        self.player = 1
        self.moves = ''

    def __repr__(self):
        b = self.board.__str__()
        return f'\n{b}\nPlayer: {self.player}, Moves: {[int(i) for i in self.moves]}\n'

    def copy(self, deep=True):
        if deep:
            return copy.deepcopy(self)
        else:
            return copy.copy(self)

    def play(self, x, copy=False):
        if copy:
            board = self.copy()
        else:
            board = self

        y = board.h - 1
        while True:
            if not board.board[y, x]:
                board.board[y, x] = board.player
                board.player *= -1
                board.moves += str(x)
                break
            if not y:
                raise Exception('Invalid position')
            y -= 1
        if copy:
            return board

    def rows_of_n(self, n, player):
        rows = 0
        for y in range(self.h): # horizontal rows
            for x in range(self.w-n+1):
                if (self.board[y, x:x+n] == [player]*n).all():
                    rows += 1
        for y in range(self.h-n+1): # vertical rows
            for x in range(self.w):
                if (self.board[y:y+n, x] == [player]*n).all():
                    rows += 1
        for y in range(self.h-n+1): # diagonals
            for x in range(self.w-n+1):
                r = [self.board[y+i, x+i] for i in range(n)]
                if r == [player]*n:
                    rows += 1
        for y in range(self.h-n+1): # diagonals
            for x in range(n-1, self.w):
                r = [self.board[y+i, x-i] for i in range(n)]
                if r == [player]*n:
                    rows += 1
        return rows

    def pssbl_rows_of_n(self, n, player):
        rows = 0
        for y in range(self.h): # horizontal
            for x in range(self.w-n+1):
                if -player not in self.board[y, x:x+n]:
                    rows += 1
        for y in range(self.h-n+1): # vertical
            for x in range(self.w):
                if -player not in self.board[y:y+n, x]:
                    rows += 1
        for y in range(self.h-n+1): # diagonals
            for x in range(self.w-n+1):
                r = [self.board[y+i, x+i] for i in range(n)]
                if -player not in r:
                    rows += 1
        for y in range(self.h-n+1): # diagonals
            for x in range(n-1, self.w):
                r = [self.board[y+i, x-i] for i in range(n)]
                if -player not in r:
                    rows += 1
        return rows

    @property
    def eval(self):
        # + for 1, - for -1
        if self.rows_of_n(4, 1):
            return 1
        if self.rows_of_n(4, -1):
            return -1
        # if self._eval is not None:
        #     return self._eval
        return (self.pssbl_rows_of_n(4, 1)-self.pssbl_rows_of_n(4, -1)) / 69

    @property
    def gameover(self):
        return (self.eval == 1 or self.eval == -1 or len(self.moves) == self.h*self.w)

    @property
    def winner(self):
        assert self.gameover, 'game not over'
        if self.eval == 1 or self.eval == -1:
            return self.eval
        else:
            return 0

if __name__ == '__main__':
    b = Board()
    b.play(3)
    b.play(5)
    print(b)
    print(b.eval)