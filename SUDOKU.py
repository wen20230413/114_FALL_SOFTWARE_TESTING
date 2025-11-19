# sudoku.py
# Main Sudoku generator and solver implementation
import copy
import random

class SudokuBoard:
    def __init__(self, grid):
        # Use deepcopy to ensure the original grid is not modified
        self.grid = copy.deepcopy(grid)
        self.size = 9

    def is_valid(self, row, col, num):
        # Check row
        for i in range(self.size):
            if self.grid[row][i] == num:
                return False

        # Check column
        for i in range(self.size):
            if self.grid[i][col] == num:
                return False

        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        
        return True

    def find_empty(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)  # row, col
        return None

    def solve(self, randomize=False):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        numbers = list(range(1, self.size + 1))
        if randomize:
            random.shuffle(numbers)

        for num in numbers:
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if self.solve(randomize):
                    return True
                self.grid[row][col] = 0  # Backtrack
        return False
    
    def has_unique_solution(self):
        """
        Check if the Sudoku puzzle has a unique solution.
        Returns True if the puzzle has exactly one solution, False otherwise.
        """
        solution_count = 0

        def count_solutions():
            nonlocal solution_count
            find = self.find_empty()
            if not find:
                solution_count += 1
                return

            row, col = find
            for num in range(1, self.size + 1):
                if self.is_valid(row, col, num):
                    self.grid[row][col] = num
                    count_solutions()
                    self.grid[row][col] = 0  # Backtrack

                    # Stop early if more than one solution is found
                    if solution_count > 1:
                        return

        count_solutions()
        return solution_count == 1

    def score_difficulty(self):
        """
        使用人類求解技巧評估難度 (Human-Logic Difficulty Rating)
        Returns 'Easy', 'Medium', or 'Hard'.
        
        Uses DifficultyEngine with human-like solving technique hierarchy:
        - Easy (score ~15): Naked Singles, Hidden Singles
        - Medium (score 65-80): Naked Pairs, Pointing Pairs
        - Hard (score 120+): X-Wing
        
        This method simulates how a human would solve the puzzle,
        not the computational complexity of backtracking algorithms.
        """
        from difficulty_engine import DifficultyEngine
        engine = DifficultyEngine()
        difficulty, score, techniques = engine.rate_puzzle(self)
        return difficulty


def generate(difficulty):
    # 1. Create a full, random solution
    empty_grid = [[0] * 9 for _ in range(9)]
    solution_board = SudokuBoard(empty_grid)
    solution_board.solve(randomize=True)  # Use the randomized solver

    # 2. Create a puzzle by removing cells
    puzzle_board = SudokuBoard(solution_board.grid)
    
    cells_to_remove = difficulty
    while cells_to_remove > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        if puzzle_board.grid[row][col] != 0:
            puzzle_board.grid[row][col] = 0
            cells_to_remove -= 1
            
    return puzzle_board, solution_board