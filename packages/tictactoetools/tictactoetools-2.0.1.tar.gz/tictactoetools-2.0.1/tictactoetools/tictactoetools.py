import json
from datetime import datetime
from .tictac_exceptions import FullBoardError
from dataclasses import dataclass
import os
import mysql.connector


class Board:
    __BLANK_SPACE = " "

    def __init__(self, size: int = 3, num_consecutive_to_win: int = None) -> None:
        if size <= 0 or num_consecutive_to_win and num_consecutive_to_win <= 0:
            raise ValueError("Board cannot have negative dimensions.")

        self.__size = size
        self.__num_consecutive_to_win = min(num_consecutive_to_win, size) if num_consecutive_to_win else size
        self.__board = [[self.__BLANK_SPACE for i in range(size)] for i in range(size)]

    def display(self) -> None:
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
        return self.__check_rows_for_win() or self.__check_columns_for_win() or self.__check_diagonals_for_win()

    def __check_rows_for_win(self) -> bool:
        for row in self.__board:
            for i in range(self.__size - self.__num_consecutive_to_win + 1):
                if row[i] != self.__BLANK_SPACE and len(
                        set([row[i + k] for k in range(self.__num_consecutive_to_win)])) == 1:
                    return True
        return False

    def __check_columns_for_win(self) -> bool:
        for i in range(self.__size - self.__num_consecutive_to_win + 1):
            for j in range(self.__size):
                if self.__board[i][j] != self.__BLANK_SPACE and len(
                        set([self.__board[i + k][j] for k in range(self.__num_consecutive_to_win)])) == 1:
                    return True

        return False

    def __check_diagonals_for_win(self) -> bool:
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
        for row in self.__board:
            for cell in row:
                if cell == self.__BLANK_SPACE:
                    return False

        return True

    def mark(self, row: int, col: int, symbol: str) -> None:
        if row > self.__size or col > self.__size:
            raise ValueError("Row or column number outside of board size.")

        if self.is_full():
            raise FullBoardError()

        self.__board[row - 1][col - 1] = symbol

    def is_empty_space(self, row: int, col: int) -> bool:
        return self.__board[row - 1][col - 1] == self.__BLANK_SPACE

    def clear(self) -> None:
        self.__board = [[self.__BLANK_SPACE for i in range(self.__size)] for i in range(self.__size)]

    def _as_json(self):
        return {
            "board": self.__board,
            "size": self.__size,
            "num_consecutive_to_win": self.__num_consecutive_to_win
        }

    @property
    def size(self) -> int:
        return self.__size


@dataclass
class Match:
    p1: str
    p2: str
    start_time: datetime
    end_time: datetime
    board: Board
    winner: str


def play() -> None:
    match = new_match()
    log_match(match)
    while wants_rematch():
        match = new_match(p1=match.p1, p2=match.p2)
        log_match(match)


def new_match(*, p1: str = None, p2: str = None) -> Match:
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
    row = prompt_board_value("Row: ", lim=board.size)
    col = prompt_board_value("Column: ", lim=board.size)
    while not board.is_empty_space(row, col):
        print(f"Space at row {row}, column {col} is not empty!")
        row = prompt_board_value("Row: ", lim=board.size)
        col = prompt_board_value("Column: ", lim=board.size)

    board.mark(row, col, symbol)


def prompt_board_value(prompt: str, *, lim: int = 100) -> int:
    val = int(input(prompt))
    while val <= 0 or val > lim:
        print("Invalid value!")
        val = int(input(prompt))

    return val


def prompt_username(player_num: int) -> str:
    # usernames are in all uppercase and have no trailing or leading whitespace
    username = input(f"Player {player_num} name: ").strip().upper()
    while len(username) > 15 or len(username) < 5:
        print("Username must be between 5 and 15 characters!")
        username = input(f"Player {player_num} name: ").strip().upper()

    return username


def wants_rematch() -> bool:
    resp = input("Rematch (y/n): ").lower().strip()
    while resp not in {"y", "n"}:
        print("Please type y (yes) or n (no).")
        resp = input("Rematch (y/n): ").lower().strip()

    return resp == "y"


def log_match(match: Match) -> None:
    p1_id = get_player_id(match.p1)
    p2_id = get_player_id(match.p2)
    formatted_start_datetime = match.start_time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_end_datetime = match.end_time.strftime("%Y-%m-%d %H:%M:%S")
    board_data = match.board._as_json()
    winner_id = get_player_id(match.winner) if match.winner else None

    with mysql.connector.connect(
        host='sql9.freesqldatabase.com',
        user='sql9632131',
        password='iWCMKp7Q8R',
        database='sql9632131'
    ) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
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
            conn.commit()
        finally:
            cursor.close()


def get_player_id(username: str) -> int:
    if not username_exists(username):
        create_new_user(username)

    with mysql.connector.connect(
        host='sql9.freesqldatabase.com',
        user='sql9632131',
        password='iWCMKp7Q8R',
        database='sql9632131'
    ) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT player_id
                FROM players
                WHERE username = %s
                """, (username,))
            row = cursor.fetchone()
            # Consume and discard any remaining unread results
            cursor.fetchall()
            return row[0]
        finally:
            cursor.close()


def username_exists(username: str) -> bool:
    with mysql.connector.connect(
            host='sql9.freesqldatabase.com',
            user='sql9632131',
            password='iWCMKp7Q8R',
            database='sql9632131'
    ) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT EXISTS(
                SELECT 1 FROM players WHERE username = %s
            ) AS username_exists
            """, (username,))
            exists = bool(cursor.fetchone()[0])
            # Consume and discard any remaining unread results
            cursor.fetchall()
            return exists
        finally:
            cursor.close()


def create_new_user(username: str) -> None:
    with mysql.connector.connect(
            host='sql9.freesqldatabase.com',
            user='sql9632131',
            password='iWCMKp7Q8R',
            database='sql9632131'
    ) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO players (username)
            VALUES (
                %s
            )
            """, (username,))
            conn.commit()
        finally:
            cursor.close()


def get_player_stats(usernames: list[str] = None) -> list:
    data = []

    with mysql.connector.connect(
            host='sql9.freesqldatabase.com',
            user='sql9632131',
            password='iWCMKp7Q8R',
            database='sql9632131'
    ) as conn:
        cursor = conn.cursor()

        try:
            if not usernames:
                cursor.execute("""
                SELECT username, num_matches, num_wins
                FROM player_stats
                """)
            else:
                placeholders = ', '.join(['%s'] * len(usernames))
                cursor.execute(f"""
                SELECT username, num_matches, num_wins
                FROM player_stats
                WHERE username IN ({placeholders})
                """, usernames)
            rows = cursor.fetchall()
            for row in rows:
                username, num_matches, num_wins = row
                data.append({
                    "username": username,
                    "num_matches": num_matches,
                    "num_wins": num_wins
                })
            return data
        finally:
            cursor.close()


def get_match_stats(usernames: list[str] = None) -> list:
    data = []

    with mysql.connector.connect(
            host='sql9.freesqldatabase.com',
            user='sql9632131',
            password='iWCMKp7Q8R',
            database='sql9632131'
    ) as conn:
        cursor = conn.cursor()

        try:
            if not usernames:
                cursor.execute("""
                SELECT p1.username, p2.username, m.start_time, m.end_time, m.board, w.username
                FROM matches m
                INNER JOIN players p1 ON m.player1_id = p1.player_id
                INNER JOIN players p2 ON m.player2_id = p2.player_id
                INNER JOIN players w ON m.winner_id = w.player_id
                """)
            else:
                placeholders = ', '.join(['%s'] * len(usernames))
                cursor.execute(f"""
                SELECT p1.username, p2.username, m.start_time, m.end_time, m.board, w.username
                FROM matches m
                INNER JOIN players p1 ON m.player1_id = p1.player_id
                INNER JOIN players p2 ON m.player2_id = p2.player_id
                INNER JOIN players w ON m.winner_id = w.player_id
                WHERE p1.username IN ({placeholders}) OR p2.username IN ({placeholders})
                """, usernames * 2)  # Duplicate the usernames to match the placeholders
            rows = cursor.fetchall()
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
        finally:
            cursor.close()
