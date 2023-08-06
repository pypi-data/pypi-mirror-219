""" This module provides the functions and classes used for making Tic-Tac_toe games and storing them in the user database. """

import json
from datetime import datetime
from .tictac_exceptions import FullBoardError
from dataclasses import dataclass
import mysql.connector


class Board:
    """
    Contains all the information that a Tic-Tac-Toe board has as well as functions for operating on the internal board.
    """

    __BLANK_SPACE = " "

    def __init__(self, size: int = 3, num_consecutive_to_win: int = None):
        """
        Initializes a Board object.

        :param size: The size (dimension) of the board (default: 3).
        :param num_consecutive_to_win: The number of consecutive symbols required to win (default: size).
        :raises ValueError: If the size or num_consecutive_to_win is not positive.
        """

        if size <= 0 or num_consecutive_to_win is not None and num_consecutive_to_win <= 0:
            raise ValueError("Board cannot have a dimension that is not positive.")

        self.__size = size
        self.__num_consecutive_to_win = min(num_consecutive_to_win, size) if num_consecutive_to_win else size
        self.__board = [[self.__BLANK_SPACE for i in range(size)] for i in range(size)]

    def display(self) -> None:
        """
        Displays the current state of the board and the row and column numbers starting at 1 from the top left.
        """

        board_str = "  "

        # top numbers
        for i in range(self.__size):
            board_str += f"   {i + 1}    "
        board_str += "\n"

        # for each group of 3 rows
        for i in range(self.__size):
            # print a row
            for j in range(3):
                # if middle row
                if j == 1:
                    # row with X's and O's
                    for k in range(self.__size):
                        if k == 0:
                            board_str += f"{i + 1} "
                        board_str += f"   {self.__board[i][k]}   {'|' if k != self.__size - 1 else ''}"
                    board_str += "\n"

                else:
                    # print blank row
                    for k in range(self.__size - 1):
                        if k == 0:
                            board_str += "  "
                        board_str += "       |"
                    board_str += "\n"

            if i != self.__size - 1:
                # print separating row
                for j in range(self.__size):
                    if j == 0:
                        board_str += "  "
                    board_str += f"-------{'|' if j != self.__size - 1 else ''}"
                board_str += "\n"

        print(board_str, end="")

    def has_winner(self) -> bool:
        """
        Checks if there is a winner on the board.

        :return: True if a player has won, False otherwise.
        """

        return self.__check_rows_for_win() or self.__check_columns_for_win() or self.__check_diagonals_for_win()

    def __check_rows_for_win(self) -> bool:
        """
        Checks the if any of the rows contain a winner or not.

        :return: True if there is a winner in the rows, False otherwise.
        """
        for row in self.__board:
            for i in range(self.__size - self.__num_consecutive_to_win + 1):
                if row[i] != self.__BLANK_SPACE and len(
                        set([row[i + k] for k in range(self.__num_consecutive_to_win)])) == 1:
                    return True
        return False

    def __check_columns_for_win(self) -> bool:
        """
        Checks the if any of the columns contain a winner or not.

        :return: True if there is a winner in the columns, False otherwise.
        """

        for i in range(self.__size - self.__num_consecutive_to_win + 1):
            for j in range(self.__size):
                if self.__board[i][j] != self.__BLANK_SPACE and len(
                        set([self.__board[i + k][j] for k in range(self.__num_consecutive_to_win)])) == 1:
                    return True

        return False

    def __check_diagonals_for_win(self) -> bool:
        """
        Checks the if any of the diagonals contain a winner or not.

        :return: True if there is a winner in the diagonals, False otherwise.
        """

        # check left to right diagonals
        for i in range(self.__size - self.__num_consecutive_to_win + 1):
            for j in range(self.__size - self.__num_consecutive_to_win + 1):
                if self.__board[i][j] != self.__BLANK_SPACE and len(
                        set([self.__board[i + k][j + k] for k in range(self.__num_consecutive_to_win)])) == 1:
                    return True

        # check right to left diagonals
        for i in range(self.__num_consecutive_to_win - 1, self.__size):
            for j in range(self.__size - self.__num_consecutive_to_win + 1):
                if self.__board[i][j] != self.__BLANK_SPACE and len(
                        set([self.__board[i - k][j + k] for k in range(self.__num_consecutive_to_win)])) == 1:
                    return True

        return False

    def is_full(self) -> bool:
        """
        Checks if the board is completely filled.

        :return: True if the board is full, False otherwise.
        """

        for row in self.__board:
            for cell in row:
                if cell == self.__BLANK_SPACE:
                    return False

        return True

    def mark(self, row: int, col: int, symbol: str) -> None:
        """
        Marks a cell on the board with the given symbol.

        :param row: The row number of the cell.
        :param col: The column number of the cell.
        :param symbol: The symbol to mark in the cell.
        :raises FullBoardError: If the board is already full.
        :raises ValueError: If row or col are greater than the size of the board.
        """

        if row > self.__size or col > self.__size:
            raise ValueError("Row or column number outside of board size.")

        if self.is_full():
            raise FullBoardError()

        self.__board[row - 1][col - 1] = symbol

    def is_empty_space(self, row: int, col: int) -> bool:
        """
        Checks if a cell on the board is empty (just a space in quotes " ").

        :param row: The row number of the cell.
        :param col: The column number of the cell.
        :return: True if the cell is empty, False otherwise.
        """

        return self.__board[row - 1][col - 1] == self.__BLANK_SPACE

    def clear(self) -> None:
        """
        Clears the board by setting all cells to blank spaces.
        """

        self.__board = [[self.__BLANK_SPACE for i in range(self.__size)] for i in range(self.__size)]

    def _as_json(self):
        """
        Returns the board state as a JSON-compatible dictionary.

        Not meant to be used outside this module. The JSON data can be retrieved from the board column of the matches
        table in the database. This is used to put that data there.

        :return: The board state as a dictionary.
        """

        return {
            "board": self.__board,
            "size": self.__size,
            "num_consecutive_to_win": self.__num_consecutive_to_win
        }

    @property
    def size(self) -> int:
        """
        Returns the size (dimension) of the board.

        :return: The size of the board.
        """

        return self.__size


@dataclass
class Match:
    """
    Dataclass that stores the data of a match.

    p1 for player1 username, p2 for player2 username, start_time as a datetime, end_time as a datetime, the Board object
    that the match was played on, and the winner username.
    """

    p1: str
    p2: str
    start_time: datetime
    end_time: datetime
    board: Board
    winner: str


class _DBConnection:
    def __init__(self) -> None:
        """
        Initializes a _DBConnection object.

        db as the connection to the database and cur as the cursor for that connection. Supports context manager
        protocol by using __enter__ to just return the current instance and __exit to close db and cur.
        """

        self.db = mysql.connector.connect(
            host='sql9.freesqldatabase.com',
            user='sql9632131',
            password='iWCMKp7Q8R',
            database='sql9632131'
        )
        self.cur = self.db.cursor()

    def __enter__(self):
        """
        Enter method for using a with as statement.

        :return: Current instance of _DBConnection
        """

        return self

    def __exit__(self, exc_type: BaseException, exc_val: BaseException, exc_tb) -> None:
        """
        Close the db connection and cursor.

        :param exc_type: The type of the exception raised in the context, or None if no exception occurred.
        :type exc_type: type or None
        :param exc_val: The instance of the exception raised in the context, or None if no exception occurred.
        :type exc_val: BaseException or None
        :param exc_tb: The traceback associated with the exception raised in the context, or None if no exception occurred.
        :type exc_tb: traceback.TracebackType or None
        :return: Optionally return a value to indicate whether any exception has been handled or suppressed.
        :rtype: bool or None
        """

        self.db.close()
        self.cur.close()


def play() -> None:
    """
    Allows users to play a Tic-Tac-Toe match and log it in the database.

    This function is just an example of how all the utilities this package provides can be used in tandem to create a
    Tic-Tac-Toe game.
    """
    match = new_match()
    log_match(match)
    while wants_rematch():
        match = new_match(p1=match.p1, p2=match.p2)
        log_match(match)


def new_match(*, p1: str = None, p2: str = None) -> Match:
    """
    Creates a new Tic-Tac-Toe match with user-specified parameters.

    This method essentially plays a game of Tic-Tac-Tow in order to retrieve all the data for a new Match object that is
    returned.

    :param p1: The username of player 1 (optional).
    :param p2: The username of player 2 (optional).
    :return: The Match object representing the new match.
    """

    p1 = p1 if p1 else prompt_username(player_num=1)
    p2 = p2 if p2 else prompt_username(player_num=2)

    size = prompt_board_value("Board size: ")
    num_consecutive_to_win = prompt_board_value("Number of consecutive symbols to win: ")
    board = Board(size, num_consecutive_to_win)

    st = datetime.now()

    turn_number = 1
    while not board.has_winner() and not board.is_full():
        board.display()

        if turn_number % 2 == 1:
            print(f"{p1}'s turn")
            player_move(board, "X")
        else:
            print(f"{p2}'s turn")
            player_move(board, "O")

        turn_number += 1

    winner = None if (board.is_full() and not board.has_winner()) else (p1 if turn_number % 2 == 0 else p2)

    if not winner:
        print("It's a tie!")
    elif winner == p1:
        print(f"{p1} wins!")
    else:
        print(f"{p2} wins!")

    end = datetime.now()

    return Match(p1=p1, p2=p2, start_time=st, end_time=end, board=board, winner=winner)


def player_move(board: Board, symbol: str) -> None:
    """
    Handles the player's move during a Tic-Tac-Toe match.

    If the row and col entered are already occupying a space on the board it will ask for new entries.

    :param board: The Board object representing the game board.
    :param symbol: The symbol of the current player (X or O).
    """

    row = prompt_board_value("Row: ", lim=board.size)
    col = prompt_board_value("Column: ", lim=board.size)
    while not board.is_empty_space(row, col):
        print(f"Space at row {row}, column {col} is not empty!")
        row = prompt_board_value("Row: ", lim=board.size)
        col = prompt_board_value("Column: ", lim=board.size)

    board.mark(row, col, symbol)


def prompt_board_value(prompt: str, *, lim: int = 100) -> int:
    """
    Prompts the user for a valid board value.

    Values cannot be negative or go over the limit. An explicit limit needs to be set if the board size is greater than
    100 (or just don't play a massive game of Tic-Tac-Toe).

    :param prompt: The prompt message to display.
    :param lim: The upper limit for the valid board value (default: 100).
    :return: The validated board value.
    """

    val = int(input(prompt))
    while val <= 0 or val > lim:
        print("Invalid value!")
        val = int(input(prompt))

    return val


def prompt_username(player_num: int) -> str:
    """
    Prompts the user for a valid username.

    This function will prompt another username if the given one is less than 5 characters or more than 15. While the
    database supports usernames under 5 characters, it does not for over 15. Usernames are converted to all uppercase
    and have no trailing or leading whitespace.

    :param player_num: The number of the player (1 or 2).
    :return: The validated username.
    """

    username = input(f"Player {player_num} name: ").strip().upper()
    while len(username) > 15 or len(username) < 5:
        print("Username must be between 5 and 15 characters!")
        username = input(f"Player {player_num} name: ").strip().upper()

    return username


def wants_rematch() -> bool:
    """
    Asks the user if they want a rematch.

    :return: True if the user wants a rematch, False otherwise.
    """

    resp = input("Rematch (y/n): ").lower().strip()
    while resp not in {"y", "n"}:
        print("Please type y (yes) or n (no).")
        resp = input("Rematch (y/n): ").lower().strip()

    return resp == "y"


def log_match(match: Match) -> None:
    """
    Logs a Tic-Tac-Toe match in the database.

    Puts match_id, player1_id, player2_id, start_time, end_time, board, and winner_id in the matches table of the
    database.

    :param match: The Match object representing the match data to log.
    """

    p1_id = get_player_id(match.p1)
    p2_id = get_player_id(match.p2)
    formatted_start_datetime = match.start_time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_end_datetime = match.end_time.strftime("%Y-%m-%d %H:%M:%S")
    board_data = match.board._as_json()
    winner_id = get_player_id(match.winner) if match.winner else None

    with _DBConnection() as conn:
        conn.cur.execute("""
        INSERT INTO matches (
            player1_id,
            player2_id,
            start_time,
            end_time,
            board,
            winner_id
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """, (p1_id, p2_id, formatted_start_datetime, formatted_end_datetime, json.dumps(board_data), winner_id))
        conn.db.commit()


def get_player_id(username: str) -> int:
    """
    Retrieves the player ID from the database based on the username.

    :param username: The username to retrieve the ID for.
    :return: The player ID.
    """

    if not username_exists(username):
        create_new_user(username)

    with _DBConnection() as conn:
        conn.cur.execute("""
            SELECT player_id
            FROM players
            WHERE username = %s
            """, (username,))
        row = conn.cur.fetchone()
        return row[0]


def username_exists(username: str) -> bool:
    """
    Checks if a username exists in the database.

    :param username: The username to check.
    :return: True if the username exists, False otherwise.
    """

    with _DBConnection() as conn:
        conn.cur.execute("""
        SELECT EXISTS(
            SELECT 1 FROM players WHERE username = %s
        ) AS username_exists
        """, (username,))
        exists = bool(conn.cur.fetchone()[0])
        return exists


def create_new_user(username: str) -> None:
    """
    Creates a new user in the database.

    Puts a player_id and username column in the players table.

    :param username: The username of the new user.
    """

    with _DBConnection() as conn:
        conn.cur.execute("""
        INSERT INTO players (username)
        VALUES (
            %s
        )
        """, (username,))
        conn.db.commit()


def get_player_stats(usernames: list[str] = None) -> list:
    """
    Retrieves player statistics from the database.

    The player statistics are the username, num_matches, and num_wins

    :param usernames: Optional list of usernames to filter the results (default: None).
    :return: A list of dictionaries containing player statistics.
    """

    data = []

    with _DBConnection() as conn:
        if not usernames:
            conn.cur.execute("""
            SELECT username, num_matches, num_wins
            FROM player_stats
            """)
        else:
            placeholders = ', '.join(['%s'] * len(usernames))
            conn.cur.execute(f"""
            SELECT username, num_matches, num_wins
            FROM player_stats
            WHERE username IN ({placeholders})
            """, usernames)
        rows = conn.cur.fetchall()
        for row in rows:
            username, num_matches, num_wins = row
            data.append({
                "username": username,
                "num_matches": num_matches,
                "num_wins": num_wins
            })
        return data


def get_match_stats(usernames: list[str] = None) -> list:
    """
    Retrieves match statistics from the database.

    The match statistics are player1 (username), player2 (username), start_time (datetime), end_time (datetime), board
    (result of the _as_json() function), and winner (username)

    :param usernames: Optional list of usernames to filter the results (default: None).
    :return: A list of dictionaries containing match statistics.
    """

    data = []

    with _DBConnection() as conn:
        if not usernames:
            conn.cur.execute("""
            SELECT p1.username, p2.username, m.start_time, m.end_time, m.board, w.username
            FROM matches m
            INNER JOIN players p1 ON m.player1_id = p1.player_id
            INNER JOIN players p2 ON m.player2_id = p2.player_id
            INNER JOIN players w ON m.winner_id = w.player_id
            """)
        else:
            placeholders = ', '.join(['%s'] * len(usernames))
            conn.cur.execute(f"""
            SELECT p1.username, p2.username, m.start_time, m.end_time, m.board, w.username
            FROM matches m
            INNER JOIN players p1 ON m.player1_id = p1.player_id
            INNER JOIN players p2 ON m.player2_id = p2.player_id
            INNER JOIN players w ON m.winner_id = w.player_id
            WHERE p1.username IN ({placeholders}) OR p2.username IN ({placeholders})
            """, usernames * 2)  # Duplicate the usernames to match the placeholders
        rows = conn.cur.fetchall()
        for row in rows:
            player1, player2, st, end, board, winner = row
            data.append({
                "player1": player1,
                "player2": player2,
                "start_time": st,
                "end_time": end,
                "board": board,
                "winner": winner
            })
        return data
