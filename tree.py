class Node:
    def __init__(self, moves, eval_):
        self.moves = moves
        self.eval = eval_
        self.player = (-1) ** len(moves)
        self.children = []
        self.best_child = None

    def __repr__(self):
        return f'Node({self.moves}, {round(self.eval, 5)})'


def get_end_nodes(board, depth=4):
    boards = [board]
    child_boards = []
    end_nodes = []
    for i in range(depth):
        for b in boards:
            for x in range(b.w):
                try:
                    c = b.play(x, copy=True)
                    if i == depth-1:
                        n = Node(c.moves, c.eval)
                        end_nodes.append(n)
                    else:
                        child_boards.append(c)
                except:
                    pass
        boards = child_boards.copy()
        child_boards.clear()
    return end_nodes


def build_tree(end_nodes, depth=4):
    children = end_nodes
    parents = {}
    for _ in range(depth):
        for c in children:
            p_moves = c.moves[:-1]
            parent = parents.get(p_moves)
            if parent:
                if parent.player == 1 and c.eval > parent.eval: # max
                    parent.eval = c.eval
                    parent.best_child = c
                elif parent.player == -1 and c.eval < parent.eval: # min
                    parent.eval = c.eval
                    parent.best_child = c
            else:
                parent = Node(p_moves, c.eval)
                parent.best_child = c
                parents[p_moves] = parent
            parent.children.append(c)
        children = list(parents.values())
        parents.clear()
    return children[0]


def alphabeta(board, alpha=-1, beta=1, moves='', depth=4, player=None): # alpha: lowest score maximizing player is assured, beta: highest score min player is assured
    if not player:
        player = board.player
    if len(moves) == depth: # end node
        try:
            board = board.play_moves(moves, copy=True)
            return moves[-1], board.eval
        except Exception as e:
            pass
    else:
        move = None
        best_eval = player * -1
        for x in range(board.w):
            r = alphabeta(board, alpha, beta, moves+str(x), depth, player*-1)
            if not r:
                continue
            eval_ = r[1]
            if player == 1:
                if eval_ > best_eval:
                    best_eval = eval_
                    move = x
                if best_eval > beta:
                    break
                alpha = max(alpha, best_eval)
            else:
                if eval_ < best_eval:
                    best_eval = eval_
                    move = x
                if best_eval < alpha:
                    break
                beta = min(beta, best_eval)
        if move:
            return move, best_eval


if __name__ == '__main__':
    import time
    from board import Board
    depth = 5
    b = Board()

    s = time.time()
    end_nodes = get_end_nodes(b, depth)
    root = build_tree(end_nodes, depth)
    move = int(root.best_child.moves[-1])
    t = time.time() - s

    p = root
    for _ in range(depth):
        print(f'Player: {p.player}')
        print(p.children)
        c = p.best_child
        print(f'Best: {c}s')
        p = c
        print()
    print(f'Time: {round(t, 5)}')
    print()

    s = time.time()
    move, eval_ = alphabeta(b, depth=depth)
    print(f'Alphabeta: {move, round(eval_, 5)}')
    t = time.time() - s
    print(f'Time: {round(t, 5)}s')
