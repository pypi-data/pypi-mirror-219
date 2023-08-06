class FullBoardError(Exception):
    def __init__(self, message="Cannot mark a full board."):
        super(message)
