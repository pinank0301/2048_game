import tkinter as tk
import random

# Constants
GRID_SIZE = 4
TILE_SIZE = 100
PADDING = 10
FONT = ("Helvetica", 30, "bold")
COLORS = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}

# Initialize grid
def initialize_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_random_tile(grid)
    add_random_tile(grid)
    return grid

# Add random tile to the grid
def add_random_tile(grid):
    empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        grid[r][c] = 2 if random.random() < 0.9 else 4

# Slide and merge a row
def slide_and_merge(row):
    non_zero = [num for num in row if num != 0]
    merged = []
    skip = False
    for i in range(len(non_zero)):
        if skip:
            skip = False
            continue
        if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
            merged.append(non_zero[i] * 2)
            skip = True
        else:
            merged.append(non_zero[i])
    return merged + [0] * (GRID_SIZE - len(merged))

# Slide the grid in a direction
def slide_grid(grid, direction):
    new_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    score = 0
    if direction in ("LEFT", "RIGHT"):
        for r in range(GRID_SIZE):
            row = grid[r]
            if direction == "RIGHT":
                row = row[::-1]
            new_row = slide_and_merge(row)
            if direction == "RIGHT":
                new_row = new_row[::-1]
            new_grid[r] = new_row
            score += sum(new_row)
    else:  # UP or DOWN
        for c in range(GRID_SIZE):
            col = [grid[r][c] for r in range(GRID_SIZE)]
            if direction == "DOWN":
                col = col[::-1]
            new_col = slide_and_merge(col)
            if direction == "DOWN":
                new_col = new_col[::-1]
            for r in range(GRID_SIZE):
                new_grid[r][c] = new_col[r]
                score += new_col[r]
    return new_grid, score

# Check if moves are possible
def can_move(grid):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0:
                return True
            if c + 1 < GRID_SIZE and grid[r][c] == grid[r][c + 1]:
                return True
            if r + 1 < GRID_SIZE and grid[r][c] == grid[r + 1][c]:
                return True
    return False

# GUI Class
class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.root.geometry(f"{GRID_SIZE * TILE_SIZE + PADDING * (GRID_SIZE + 1)}x{GRID_SIZE * TILE_SIZE + PADDING * (GRID_SIZE + 1) + 50}")
        self.root.configure(bg="#bbada0")
        self.score = 0
        self.grid = initialize_grid()
        self.frames = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.create_ui()
        self.update_ui()

    def create_ui(self):
        # Create a canvas for the grid
        self.canvas = tk.Canvas(self.root, bg="#bbada0", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # Create a restart button
        restart_button = tk.Button(self.root, text="Restart", command=self.restart_game, font=("Helvetica", 15), bg="#8f7a66", fg="white")
        restart_button.pack(pady=10)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x1 = PADDING + c * (TILE_SIZE + PADDING)
                y1 = PADDING + r * (TILE_SIZE + PADDING)
                x2 = x1 + TILE_SIZE
                y2 = y1 + TILE_SIZE
                self.frames[r][c] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLORS[0], outline="")

    def update_ui(self):
        self.canvas.delete("text")
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = self.grid[r][c]
                color = COLORS[value]
                self.canvas.itemconfig(self.frames[r][c], fill=color)
                if value != 0:
                    x1 = PADDING + c * (TILE_SIZE + PADDING) + TILE_SIZE // 2
                    y1 = PADDING + r * (TILE_SIZE + PADDING) + TILE_SIZE // 2
                    self.canvas.create_text(x1, y1, text=str(value), font=FONT, fill="white" if value > 4 else "black", tags="text")

    def move(self, direction):
        new_grid, gained_score = slide_grid(self.grid, direction)
        if new_grid != self.grid:
            self.grid = new_grid
            self.score += gained_score
            add_random_tile(self.grid)
            self.update_ui()
            if not can_move(self.grid):
                self.game_over()

    def restart_game(self):
        self.grid = initialize_grid()
        self.score = 0
        self.update_ui()

    def game_over(self):
        self.canvas.create_text(GRID_SIZE * TILE_SIZE // 2 + PADDING, GRID_SIZE * TILE_SIZE // 2 + PADDING, text="Game Over", font=("Helvetica", 40, "bold"), fill="red", tags="text")

# Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.bind("<Left>", lambda e: game.move("LEFT"))
    root.bind("<Right>", lambda e: game.move("RIGHT"))
    root.bind("<Up>", lambda e: game.move("UP"))
    root.bind("<Down>", lambda e: game.move("DOWN"))
    root.mainloop()
