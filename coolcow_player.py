# Player Template
# IMPORTANT: 	This module must have a function called play
# 				that receives a game and return a tuple of
# 				two integers who represent a valid move on
# 				the game.

from __future__ import annotations
from typing import List, Set, Tuple
from game_logic import *
from coolcow_minimax import minimax
import heapq


# Type Synonims
Position = Tuple[int, int]

# game_logic
#
# 	EMPTY
# 	PLAYER[0]
# 	PLAYER[1]

# game
# 	-> current (W or B)
# 		It refers to the player who must play in
# 		this turn.
# 	-> indexing
# 		game[i,j] return the player who have played
# 		on position <i;j> (compare with PLAYER[0]
# 		and PLAYER[1]). EMPTY if none player have
# 		played there.
# 	-> neighbour
# 		creates an iterator that yields all
# 		coordinates <x;y> who are neighbour of
# 		current coordinates.
#
# 		for nx, ny in game.neighbour(x, y):
# 			print(nx, ny)


def play(game, player):
    depth = 3
    return minimax(game, player, depth, heuristic, moves)


def moves(game, player):
    for x in range(game.size):
        for y in range(game.size):
            if game[x, y] == EMPTY:
                yield (x, y)


def heuristic(game: Game, player: str) -> int:
    # h1 = most_sparsed(game, player)
    # h2 = block_adversary(game, player)
    h3 = shortest_path(game, player)
    return max(0, h3)


def shortest_path(game: Game, player: str) -> int:
    n = game.size
    white_starting_points = set((i, 0) for i in range(n) if game[i, 0] != BLACK)
    white_end_points = set((i, n - 1) for i in range(n) if game[i, n - 1] != BLACK)
    black_starting_points = set((0, i) for i in range(n) if game[0, i] != WHITE)
    black_end_points = set((n - 1, i) for i in range(n) if game[n - 1, i] != WHITE)

    shortest_white = ucs(game, WHITE, white_starting_points, white_end_points)
    shortest_black = ucs(game, BLACK, black_starting_points, black_end_points)

    hval = (
        shortest_black - shortest_white
        if player == WHITE
        else shortest_white - shortest_black
    )
    return hval


def ucs(
    game: Game,
    player: str,
    start_positions: Set[Position],
    end_positions: Set[Position],
) -> int:
    # Init Priority Queue
    pq: List[Tuple[int, Position]] = [
        (0 if game[st_pos] == player else 1, st_pos) for st_pos in start_positions
    ]
    heapq.heapify(pq)

    # Init visited
    visited = set(pq)

    while len(pq) > 0:
        cost, current = heapq.heappop(pq)
        if current in end_positions:
            return cost
        for ady in game.neighbour(*current):
            if ady in visited or game[ady] not in {EMPTY, player}:
                continue
            visited.add(ady)
            new_cost = cost + (1 if game[ady] == EMPTY else 0)
            heapq.heappush(pq, (new_cost, ady))

    return game.size ** 2
