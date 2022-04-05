# Player Template
# IMPORTANT: 	This module must have a function called play
# 				that receives a game and return a tuple of
# 				two integers who represent a valid move on
# 				the game.

from __future__ import annotations
from typing import Set, Tuple
from game_logic import *
from minimax import minimax
from dataclasses import dataclass

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
    # Code Here
    # Random player implementation (just delete it)

    return minimax(game, player, 3, heuristic, moves)


def moves(game, player):
    for x in range(game.size):
        for y in range(game.size):
            if game[x, y] == EMPTY:
                yield (x, y)


def heuristic(game: Game, player: str) -> int:
    hval = most_sparsed(game, player)
    return max(0, hval)


def most_sparsed(game: Game, player: str):
    global_borders = Borders(*[(-1, -1) for _ in range(4)])
    get_bigger = (
        lambda border1, border2: border1.bigger_vertical_border(border2)
        if player == WHITE
        else border1.bigger_horizontal_border(border2)
    )
    visited = set()
    empty_area = set()
    for x in range(game.size):
        for y in range(game.size):
            if game[x, y] == player and (x, y) not in visited:
                visited.add((x, y))
                borders = Borders(*[(x, y) for _ in range(4)])
                dfs(game, player, (x, y), visited, empty_area, borders)
                global_borders = (
                    get_bigger(global_borders, borders)
                    if global_borders.valid
                    else borders
                )

    # print("######")
    # print(player)
    # if player == WHITE:
    # print(global_borders)
    # print(game)

    area_covered = (
        global_borders.bottom[1] - global_borders.top[1]
        if player == WHITE
        else global_borders.right[0] - global_borders.left[0]
    )

    return area_covered * 100 - len(empty_area)


def dfs(
    game: Game,
    player: str,
    current: Position,
    visited: Set[Position],
    empty_area: Set[Position],
    borders: Borders,
) -> None:
    for ady in game.neighbour(*current):
        if game[ady] in {player, EMPTY}:
            empty_area.add(ady)
        if ady in visited:
            continue
        visited.add(ady)
        borders.update_borders(ady)
        dfs(game, player, ady, visited, empty_area, borders)


@dataclass
class Borders:
    left: Position
    right: Position
    top: Position
    bottom: Position

    @property
    def valid(self):
        return (
            self.left[0] != -1
            and self.right[0] != -1
            and self.top[1] != -1
            and self.bottom[1] != -1
        )

    def update_borders(self, position: Position):
        if position[0] < self.left[0]:
            self.left = position
        if position[0] > self.right[0]:
            self.right = position
        if position[1] < self.top[1]:
            self.top = position
        if position[1] > self.bottom[1]:
            self.bottom = position

    def bigger_border(self, other_border: Borders):
        if self.left[0] < other_border.left[0]:
            return self
        if self.right[0] > other_border.right[0]:
            return self
        if self.top[1] < other_border.top[1]:
            return self
        if self.bottom[1] > other_border.bottom[1]:
            return self
        return other_border

    def bigger_horizontal_border(self, other_border: Borders):
        self_size = self.right[0] - self.left[0]
        other_size = other_border.right[0] - other_border.left[0]
        if self_size >= other_size:
            return self
        return other_border

    def bigger_vertical_border(self, other_border: Borders):
        self_size = self.bottom[1] - self.top[1]
        other_size = other_border.bottom[1] - other_border.top[1]
        if self_size >= other_size:
            return self
        return other_border

    def __str__(self) -> str:
        return f"{self.left} {self.right} {self.top} {self.bottom}"
