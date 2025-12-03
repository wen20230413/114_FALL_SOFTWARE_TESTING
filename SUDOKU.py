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


def generate(difficulty, max_attempts=50):
    """
    Generate a Sudoku puzzle with mostly symmetric holes (帶隨機性的中心對稱挖洞)
    約 70-80% 對稱，增加自然感，並確保唯一解
    
    Args:
        difficulty: Number of cells to remove
        max_attempts: Maximum attempts to generate a valid puzzle with unique solution
    
    Returns:
        tuple: (puzzle_board, solution_board)
    """
    for attempt in range(max_attempts):
        # 1. Create a full, random solution
        empty_grid = [[0] * 9 for _ in range(9)]
        solution_board = SudokuBoard(empty_grid)
        solution_board.solve(randomize=True)  # Use the randomized solver

        # 2. Create a puzzle by removing cells with partial symmetry
        puzzle_board = SudokuBoard(solution_board.grid)
        
        # Decide how many cells to remove symmetrically vs randomly
        # 70-80% symmetric, 20-30% random
        symmetry_ratio = random.uniform(0.7, 0.8)
        symmetric_count = int(difficulty * symmetry_ratio)
        random_count = difficulty - symmetric_count
        
        # Make sure symmetric_count is even
        if symmetric_count % 2 == 1:
            symmetric_count -= 1
            random_count += 1
        
        pairs_to_remove = symmetric_count // 2
        
        # Create list of all possible cell positions
        available_cells = []
        for row in range(9):
            for col in range(9):
                available_cells.append((row, col))
        
        # Shuffle to randomize which cells to remove
        random.shuffle(available_cells)
        
        # Phase 1: Remove pairs symmetrically
        removed_count = 0
        for row, col in available_cells:
            if removed_count >= pairs_to_remove:
                break
            
            # Calculate symmetric position (center symmetry)
            sym_row = 8 - row
            sym_col = 8 - col
            
            # Skip if this would be the same cell (center)
            if row == sym_row and col == sym_col:
                continue
            
            # Only remove if both cells still have values
            if puzzle_board.grid[row][col] != 0 and puzzle_board.grid[sym_row][sym_col] != 0:
                puzzle_board.grid[row][col] = 0
                puzzle_board.grid[sym_row][sym_col] = 0
                removed_count += 1
        
        # Phase 2: Remove remaining cells randomly for natural variation
        cells_removed = sum(row.count(0) for row in puzzle_board.grid)
        attempts_random = 0
        max_attempts_random = random_count * 10  # Prevent infinite loop
        
        while cells_removed < difficulty and attempts_random < max_attempts_random:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            
            if puzzle_board.grid[row][col] != 0:
                puzzle_board.grid[row][col] = 0
                cells_removed += 1
            
            attempts_random += 1
        
        # 3. Verify unique solution
        if puzzle_board.has_unique_solution():
            # Success! Return this puzzle
            return puzzle_board, solution_board
        
        # If not unique, try again (loop continues)
        if attempt < max_attempts - 1:
            # Print progress for debugging (optional, can be removed)
            if attempt % 10 == 0 and attempt > 0:
                print(f"  Attempt {attempt+1}/{max_attempts}: Retrying to get unique solution...")
    
    # If we get here, we couldn't generate a unique solution puzzle
    # Return the last attempt anyway (rare case)
    print(f"Warning: Could not generate puzzle with unique solution after {max_attempts} attempts")
    return puzzle_board, solution_board