from board import Board
from tree import Node, get_end_nodes, build_tree, alphabeta

if __name__ == '__main__':
    depth = 6
    player = 1
    b = Board()
    while not b.gameover:
        print(b)
        if b.player == player:
            move = int(input('Move: '))
        else:
            # end_nodes = get_end_nodes(b, depth)
            # root = build_tree(end_nodes, depth)
            # move = int(root.best_child.moves[-1])
            move, _ = alphabeta(b)
            print(_)
        b.play(move)
    print('Game over')
    print(b)
    print('Winner:', b.winner)
