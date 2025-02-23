import pygame
import time

# Initialize pygame
pygame.init()

# Constants for display
WIDTH, HEIGHT = 450, 450  # Window size
CELL_SIZE = WIDTH // 9
LINE_COLOR = (0, 0, 0)  # Black grid lines
BG_COLOR = (255, 255, 255)  # White background
FONT = pygame.font.Font(None, 40)  # Font for numbers

# Colors
HIGHLIGHT_COLOR = (200, 255, 200)  # Light green (for current cell)
TEXT_COLOR = (0, 0, 0)  # Black numbers
BACKTRACK_COLOR = (255, 200, 200)  # Light red (for backtracking)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")


def draw_board(board, current_cell=None, backtracking=False):
    """ Draws the Sudoku board with numbers. """
    screen.fill(BG_COLOR)

    # Draw grid lines
    for i in range(10):
        line_width = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_width)
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), line_width)

    # Draw numbers
    for row in range(9):
        for col in range(9):
            num = board[row][col]
            if num != ".":
                color = TEXT_COLOR
                if current_cell == (row, col):
                    color = HIGHLIGHT_COLOR if not backtracking else BACKTRACK_COLOR
                text = FONT.render(num, True, color)
                screen.blit(text, (col * CELL_SIZE + 15, row * CELL_SIZE + 10))

    pygame.display.update()
    time.sleep(0.05)  # Slow down to visualize solving


class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.rows = [set() for _ in range(9)]
        self.cols = [set() for _ in range(9)]
        self.boxes = [set() for _ in range(9)]
        self.empty_cells = []

        # Pre-fill sets and track empty cells
        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":
                    self.empty_cells.append((i, j))
                else:
                    num = board[i][j]
                    self.rows[i].add(num)
                    self.cols[j].add(num)
                    self.boxes[(i//3) * 3 + (j//3)].add(num)

    def solve(self, index=0):
        """ Backtracking Sudoku Solver with graphical updates. """
        if index == len(self.empty_cells):
            return True  # Solved!

        row, col = self.empty_cells[index]
        box_idx = (row // 3) * 3 + (col // 3)

        for num in "123456789":
            if num not in self.rows[row] and num not in self.cols[col] and num not in self.boxes[box_idx]:
                # Place number and update sets
                self.board[row][col] = num
                self.rows[row].add(num)
                self.cols[col].add(num)
                self.boxes[box_idx].add(num)

                # Draw the board with updates
                draw_board(self.board, (row, col))

                if self.solve(index + 1):
                    return True  # If solved, return

                # Undo move (backtracking)
                self.board[row][col] = "."
                self.rows[row].remove(num)
                self.cols[col].remove(num)
                self.boxes[box_idx].remove(num)

                # Draw backtracking
                draw_board(self.board, (row, col), backtracking=True)

        return False  # Trigger backtracking


# Example Sudoku board (input)
board = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"]
]

# Run Pygame loop and solve Sudoku
solver = SudokuSolver(board)
solver.solve()

# Keep window open
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
