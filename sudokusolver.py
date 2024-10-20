import random
import time
import os

# Initialize a 9x9 Sudoku grid with all 0s
grid = [[0 for _ in range(9)] for _ in range(9)]
edit = [[True for _ in range(9)] for _ in range(9)]

# Save the grid and the edit status to a file
def save(path):
    with open(path, 'w') as savegrid:
        for i in range(9):
            for j in range(9):
                savegrid.write(f"{grid[i][j]} {int(edit[i][j])} ")
            savegrid.write("\n")

# Load the grid and the edit status from a file
def load(path):
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        return False

    with open(path, 'r') as loadgrid:
        for i in range(9):
            row = loadgrid.readline().strip().split()
            for j in range(9):
                grid[i][j] = int(row[2 * j])
                edit[i][j] = bool(int(row[2 * j + 1]))
    return True

# Check if the grid is completely filled
def checkwin():
    for row in grid:
        if 0 in row:
            return False
    return True

# Print the grid in a simple text format
def print_grid():
    print("  0   1   2   3   4   5   6   7   8")
    for i in range(9):
        print("_____________________________________")
        for j in range(9):
            if grid[i][j] == 0:
                print("|   ", end="")
            else:
                if edit[i][j]:
                    print(f"| {grid[i][j]} ", end="")
                else:
                    print(f"| {grid[i][j]} ", end="")
        print(f"| {i}")
    print("_____________________________________")

# Check if the number is valid in the current row, column, and 3x3 subgrid
def isvalid(row, col, num):
    if grid[row][col] != 0:
        return False

    # Check row and column
    if num in grid[row]:
        return False
    if num in [grid[r][col] for r in range(9)]:
        return False

    # Check 3x3 subgrid
    start_row, start_col = row - row % 3, col - col % 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    return True

# Fill the board with random numbers
def generaterandomnumber():
    for _ in range(20):
        while True:
            i, j, n = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
            if isvalid(i, j, n):
                grid[i][j] = n
                edit[i][j] = False
                break
    print_grid()

# Main function to fill the board
def fiLLboard(path):
    while not checkwin():
        save(path)
        x = int(input("Enter row number from 0 to 8 (-1 to save and exit): "))
        if x == -1:
            print("Game saved and exited.")
            break
        y = int(input("Enter column number from 0 to 8: "))
        m = int(input("Enter number between 1 and 9: "))

        if 0 <= x < 9 and 0 <= y < 9 and 1 <= m <= 9:
            if isvalid(x, y, m) and edit[x][y]:
                grid[x][y] = m
                print_grid()
            else:
                print("Invalid move. Try again.")
        else:
            print("Invalid input. Try again.")
    if checkwin():
        print("Congratulations, you win!")

# Select a file path for saving the game
def select_path():
    choice = int(input("Enter 1 for slot 1, 2 for slot 2, or 3 for slot 3: "))
    while choice not in [1, 2, 3]:
        choice = int(input("Invalid choice. Enter 1, 2, or 3: "))
    return f"save/slot{choice}.txt"

def main():
    if not os.path.exists('save'):
        os.makedirs('save')

    print("Welcome to Sudoku!")
    print("Enter 1 to load a game, 2 to start a new game.")
    choice = int(input("Enter your choice: "))
    while choice not in [1, 2]:
        choice = int(input("Invalid choice. Enter 1 to load or 2 to start a new game: "))

    path = select_path()

    if choice == 1:
        if load(path):
            print_grid()
            fiLLboard(path)
        else:
            print("No saved file found.")
    elif choice == 2:
        generaterandomnumber()
        fiLLboard(path)

if __name__ == "__main__":
    main()
