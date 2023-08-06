def play_tic_tac_toe():
    # Initialize the game board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'

    # Function to print the game board
    def print_board():
        for row in board:
            print('|'.join(row))
            print('-' * 5)

    # Function to check if a player has won
    def check_win(player):
        # Check rows
        for row in board:
            if row.count(player) == 3:
                return True

        # Check columns
        for col in range(3):
            if board[0][col] == player and board[1][col] == player and board[2][col] == player:
                return True

        # Check diagonals
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            return True
        if board[0][2] == player and board[1][1] == player and board[2][0] == player:
            return True

        return False

    # Function to check if the game is a draw
    def check_draw():
        for row in board:
            if ' ' in row:
                return False
        return True

    # Main game loop
    while True:
        print_board()

        # Get the current player's move
        while True:
            row = int(input("Enter the row (0-2): "))
            col = int(input("Enter the column (0-2): "))

            if board[row][col] == ' ':
                board[row][col] = current_player
                break
            else:
                print("Invalid move. Try again.")

        # Check if the current player has won
        if check_win(current_player):
            print_board()
            print(f"Player {current_player} wins!")
            break

        # Check if the game is a draw
        if check_draw():
            print_board()
            print("It's a draw!")
            break

        # Switch to the other player
        current_player = 'O' if current_player == 'X' else 'X'

