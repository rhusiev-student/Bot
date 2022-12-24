#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A bot to play the game
"""

from logging import DEBUG, debug, getLogger, info

getLogger().setLevel(DEBUG)
PLAYERS = {1: "O", 2: "X"}


def debug_info(text: str):
    """
    Output debug info coloured

    Parameters
    ----------
    text: str
        Text to output
    """
    info("\x1b[33;20m" + text + "\x1b[0m")


def parse_info_about_player():
    """
    This function parses the info about the player

    It can look like this:

    $$$ exec p2 : [./player1.py]

    Returns
    -------
    int
        Player number
    """
    line = input()
    debug(f"Info about the player: {line}")
    debug_info(f"The bot is player#{1 if 'p1 :' in line else 2}")
    return 1 if "p1 :" in line else 2


def parse_field_info() -> tuple[int, int]:
    """
    Get information about the field

    Returns
    -------
    tuple[int, int]
        Field size
    """
    line = input()
    debug(f"Description of the field: {line}")
    field_size = int(line.split()[-2]), int(line.split()[-1][:-1])
    debug_info(f"Field size: {field_size}")
    return field_size


def parse_field(field_height: int) -> list[str]:
    """
    Get information about the field

    Parameters
    ----------
    field_height: int
        Field height

    Returns
    -------
    list[str]
        Field
    """
    field = []
    debug_info("Field:")
    debug(input())
    for _ in range(field_height):
        line = input()
        debug(f"{line}")
        line = line[4:]
        field.append(line)
    return field


def parse_figure() -> tuple[int, int, list[tuple[int, int]]]:
    """
    Get a given figure

    Returns
    -------
    tuple[int, int, list[tuple[int, int]]]
        Figure
    """
    line = input()
    height = int(line.split()[1])
    width = int(line.split()[2][:-1])
    debug_info(f"Piece {height}x{width}:")
    figure = []
    for i in range(height):
        line = input()
        debug(f"{line}")
        for j, char in enumerate(line):
            if char == "*":
                figure.append((i, j))
    height = max([i[0] for i in figure]) + 1
    width = max([i[1] for i in figure]) + 1
    return height, width, figure


def step(player: int, switch: bool = False) -> tuple[tuple[int, int], float]:
    """
    Perform one step of the game.

    Parameters
    ----------
    player: int
        Represents whether we're the first or second player
    switch: bool
        Whether to switch the side, from which to search for moves

    Returns
    -------
    tuple[tuple[int, int], float]
        Move
        Number of attempts to made this time to make a move per field length
    """
    debug_info(f"Player {player} is playing")
    # Get the field size
    field_height, field_width = parse_field_info()
    # Get the field
    field = parse_field(field_height)
    # If we're the second player, we need to switch the field upside down
    # Because the second player is lower in the field and will be going down otherwise
    if player == 2 and not switch or player == 1 and switch:
        field_for_enumeration = field[::-1]
    else:
        field_for_enumeration = field
    if player == 2:
        field_for_enumeration = [row[::-1] for row in field_for_enumeration]
    figure_height, figure_width, figure = parse_figure()
    attempts = 0
    for i, line in enumerate(field_for_enumeration):
        if player == 2 and not switch or player == 1 and switch:
            i = field_height - i - 1
        for j, char in enumerate(line):
            if player == 2:
                j = field_width - j - 1
            if not char == PLAYERS[player]:
                continue
            x_place = i, j
            for star in figure:
                temp_move = x_place[0] - star[0], x_place[1] - star[1]
                attempts += 1
                is_good = True
                if temp_move[0] < 0 or temp_move[1] < 0:
                    is_good = False
                    continue
                if (
                    temp_move[0] + figure_height > field_height
                    or temp_move[1] + figure_width > field_width
                ):
                    is_good = False
                    continue
                for star1 in figure:
                    if (x_place[0] - star1[0], x_place[1] - star1[1]) == temp_move:
                        continue
                    if field[temp_move[0] + star1[0]][
                        temp_move[1] + star1[1]
                    ].lower() in [k.lower() for k in PLAYERS.values()]:
                        is_good = False
                if is_good:
                    debug_info(f"Move: {temp_move}")
                    return temp_move, attempts / field_height
    debug_info("Move: 0 0")
    return (0, 0), attempts / field_height


def play(player: int):
    """
    Main game loop

    Parameters
    ----------
    player: int
        First or second player is the bot playing
    """
    to_switch = 0
    attempts = 0.0
    while True:
        if to_switch >= 7 or attempts > 1.5:
            debug_info(f"Switching the side for player {player}")
            move, attempts = step(player, switch=True)
            to_switch = 0
        else:
            move, attempts = step(player, switch=False)
        to_switch += 1
        print(*move)


def main():
    """
    Main function
    """
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. The bot has lost")


if __name__ == "__main__":
    main()
