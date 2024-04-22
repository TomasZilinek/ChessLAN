class Figure:
    def __init__(self, color, number):
        self.special = 0  # for distinguishing rooks and the possibility to do En passant
        self.num_to_lett = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H"}
        self.black_types = ["BlackPawn", "BlackPawn", "BlackPawn", "BlackPawn", "BlackPawn", "BlackPawn", "BlackPawn",
                            "BlackPawn", "BlackRook", "BlackKnight", "BlackBishop", "BlackQueen", "BlackKing",
                            "BlackBishop", "BlackKnight", "BlackRook"]
        self.white_types = ["WhiteRook", "WhiteKnight", "WhiteBishop", "WhiteQueen", "WhiteKing", "WhiteBishop",
                            "WhiteKnight", "WhiteRook", "WhitePawn", "WhitePawn", "WhitePawn", "WhitePawn", "WhitePawn",
                            "WhitePawn", "WhitePawn", "WhitePawn"]
        self.name_and_value_list = {"Pawn": 1, "Rook": 5, "Knight": 3, "Bishop": 3, "Queen": 9, "King": 0}
        self.made_on_last_line = 0
        self.value = 0
        self.color = color
        self.position = 0
        self.name = ""
        self.number = number
        self.set_name_and_value(self.number, self.color)
        self.set_position(self.color, self.number)
        self.living_state = 1
        self.already_moved = 0

    def set_name_and_value(self, n, color):
        change = {"white": self.white_types, "black": self.black_types}
        self.name = change[color][n]
        self.value = self.name_and_value_list[self.name[5:]]
        if self.name[5:] == "Rook" and color == "black":
            if n == 15:
                self.special = "RightRook"
            else:
                self.special = "LeftRook"
        elif self.name[5:] == "Rook" and color == "white":
            if n == 7:
                self.special = "RightRook"
            else:
                self.special = "LeftRook"

    def set_position(self, color, n):
        change = {"white": 1, "black": 7}
        line = int(change[color] + (n - n % 8) / 8)
        letter = self.num_to_lett[int((change[color] - 1) * 8 + n - (line - 1) * 8 + 1)]
        self.position = str(letter) + str(line)
