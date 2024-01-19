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
                if parent.player == 1 and c.eval > parent.eval:# max
                    parent.eval = c.eval
                    parent.best_child = c
                elif parent.player == -1 and c.eval < parent.eval:
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


if __name__ == '__main__':
    from board import Board
    depth = 4
    b = Board()
    end_nodes = get_end_nodes(b, depth)
    root = build_tree(end_nodes, depth)
    p = root
    for _ in range(depth):
        print(f'Player: {p.player}')
        print(p.children)
        c = p.best_child
        print(f'Best: {c}')
        p = c
        print()