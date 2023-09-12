import random

class CDominoPiece:
    def __init__(self, side1, side2):
        self.side1 = side1
        self.side2 = side2

    def __str__(self):
        return f"[{self.side1}|{self.side2}]"

class CDominoes:
    def __init__(self):
        self.pieces = []

    def initialize(self):
        for i in range(7):
            for j in range(i, 7):
                self.pieces.append(CDominoPiece(i, j))

    def shuffle(self):
        random.shuffle(self.pieces)  # Shuffle the pieces randomly

    def draw_piece(self):
        if self.pieces:
            return self.pieces.pop()
        else:
            return None

class CTable:
    def __init__(self):
        self.displayed_pieces = []

    def add_piece(self, piece, end=None):
        if end == "head":
            self.displayed_pieces.insert(0, piece)
        elif end == "tail":
            self.displayed_pieces.append(piece)

    def get_head(self):
        if self.displayed_pieces:
            return self.displayed_pieces[0]
        else:
            return None

    def get_tail(self):
        if self.displayed_pieces:
            return self.displayed_pieces[-1]
        else:
            return None

    def __str__(self):
        return "Table: " + " ".join(map(str, self.displayed_pieces))

class CPlayer:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_piece(self, dominoes):
        piece = dominoes.draw_piece()
        if piece:
            self.hand.append(piece)
            return piece
        else:
            return None

    def play_piece(self, table, piece):
        if piece in self.hand:
            self.hand.remove(piece)
            head = table.get_head()
            tail = table.get_tail()

            if head is None or piece.side1 == head.side1 or piece.side2 == head.side1:
                table.add_piece(piece, "head")
            elif tail is None or piece.side1 == tail.side2 or piece.side2 == tail.side2:
                table.add_piece(piece, "tail")

    def has_matching_piece(self, table):
        head = table.get_head()
        tail = table.get_tail()

        if head is None or tail is None:
            return False

        for piece in self.hand:
            if piece.side1 == head.side1 or piece.side1 == tail.side1 or piece.side2 == head.side1 or piece.side2 == tail.side1:
                return True

        return False

    def take_turn(self, table, dominoes):
        head = table.get_head()
        tail = table.get_tail()
        matching_piece = None

        for piece in self.hand:
            if head is not None and (piece.side1 == head.side1 or piece.side2 == head.side1):
                matching_piece = piece
                break
            elif tail is not None and (piece.side1 == tail.side2 or piece.side2 == tail.side2):
                matching_piece = piece
                break

        if matching_piece:
            self.play_piece(table, matching_piece)
        else:
            drawn_piece = dominoes.draw_piece()

            if drawn_piece:
                self.hand.append(drawn_piece)

                if head is None or (drawn_piece.side1 == head.side1 or drawn_piece.side2 == head.side1):
                    self.play_piece(table, drawn_piece)
                elif tail is None or (drawn_piece.side1 == tail.side2 or drawn_piece.side2 == tail.side2):
                    self.play_piece(table, drawn_piece)

    def __str__(self):
        return f"{self.name}'s Hand: " + " ".join(map(str, self.hand))

# ASCII art representations of domino pieces
domino_art = {
    (0, 0): ["┌───┐", "│   │", "│   │", "│   │", "└───┘"],
    (0, 1): ["┌───┐", "│   │", "│ ┃ │", "│   │", "└───┘"],
    # ... (ASCII art representations for other pieces)
}

def display_table(table):
    # Display the table with ASCII art representations of pieces
    table_pieces = [domino_art.get((piece.side1, piece.side2), ["       "]*5) for piece in table.displayed_pieces]
    for i in range(5):
        print("  ".join(row[i] for row in table_pieces))
    print("\n")

if __name__ == "__main__":
    dominoes = CDominoes()
    dominoes.initialize()  # Initialize the set of 28 pieces
    dominoes.shuffle()  # Shuffle the pieces randomly

    table = CTable()
    player1 = CPlayer("Player 1")
    player2 = CPlayer("Player 2")

    # Give 10 random pieces to each player
    for _ in range(10):
        player1.draw_piece(dominoes)
        player2.draw_piece(dominoes)

    # Determine the first player using random.uniform distribution
    starting_player = random.choice([player1, player2])
    print(f"The starting player is: {starting_player.name}\n")

    # Game loop with the starting player going first
    current_player = starting_player
    winner = None  # Initialize the winner variable

    while True:
        print(f"{current_player.name}'s Turn:")
        current_player.take_turn(table, dominoes)
        display_table(table)

        # Check if the current player has won
        if not current_player.hand:
            winner = current_player
            break

        # Check if there are no more pieces left and neither player can make a move
        if not dominoes.pieces and not player1.has_matching_piece(table) and not player2.has_matching_piece(table):
            break

        # Switch to the other player for the next turn
        if current_player == player1:
            current_player = player2
        else:
            current_player = player1

    # Display the final result
    if winner:
        print(f"{winner.name} is the winner! They have no more pieces in their hand.")
    else:
        print("It's a draw! The game has ended.")

    # Display the pieces left with the second player (player1 if player2 is the winner)
    second_player = player1 if winner == player2 else player2
    print(f"{second_player.name} has {len(second_player.hand)} pieces left:")
    for piece in second_player.hand:
        print(domino_art.get((piece.side1, piece.side2), ["       "]*5))
