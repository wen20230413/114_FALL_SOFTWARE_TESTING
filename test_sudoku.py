# test_sudoku.py
from SUDOKU import SudokuBoard, generate

def test_is_valid():
    initial_grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    board = SudokuBoard(initial_grid)

    # Test valid placement (placing 4 at (0, 2))
    assert board.is_valid(0, 2, 4) is True, "is_valid(0, 2, 4) should be True"

    # Test row conflict (placing 5 at (0, 2))
    assert board.is_valid(0, 2, 5) is False, "is_valid(0, 2, 5) should be False due to row conflict"

    # Test column conflict (placing 8 at (0, 2))
    assert board.is_valid(0, 2, 8) is False, "is_valid(0, 2, 8) should be False due to column conflict"

    # Test 3x3 box conflict (placing 9 at (1, 1))
    assert board.is_valid(1, 1, 9) is False, "is_valid(1, 1, 9) should be False due to box conflict"


def test_solve():
    puzzle_grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0], 
        [6, 0, 0, 1, 9, 5, 0, 0, 0], 
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3], 
        [4, 0, 0, 8, 0, 3, 0, 0, 1], 
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0], 
        [0, 0, 0, 4, 1, 9, 0, 0, 5], 
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    solution_grid = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2], 
        [6, 7, 2, 1, 9, 5, 3, 4, 8], 
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3], 
        [4, 2, 6, 8, 5, 3, 7, 9, 1], 
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4], 
        [2, 8, 7, 4, 1, 9, 6, 3, 5], 
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]
    
    puzzle = SudokuBoard(puzzle_grid)
    assert puzzle.solve() is True, "Solver should return True for a solvable puzzle"
    assert puzzle.grid == solution_grid, "The solved puzzle does not match the expected solution"


def test_generate():
    difficulty = 45  # Number of cells to remove
    puzzle_board, solution_board = generate(difficulty)

    # 1. Validate the number of empty cells
    empty_cells = sum(row.count(0) for row in puzzle_board.grid)
    assert empty_cells == difficulty, f"Puzzle should have {difficulty} empty cells, but has {empty_cells}"

    # 2. Validate that the puzzle is solvable
    puzzle_copy = SudokuBoard(puzzle_board.grid)
    assert puzzle_copy.solve() is True, "Generated puzzle must be solvable"
    
    # 3. Validate that the provided solution is valid and complete
    def is_complete_valid_solution(board):
        # Check if board is completely filled
        for row in board.grid:
            if 0 in row:
                return False
        
        # Check if all rules are satisfied
        for row in range(9):
            for col in range(9):
                num = board.grid[row][col]
                # Temporarily remove the number and check if it's valid placement
                board.grid[row][col] = 0
                is_valid = board.is_valid(row, col, num)
                board.grid[row][col] = num  # Put it back
                if not is_valid:
                    return False
        return True
    
    assert is_complete_valid_solution(solution_board), "Provided solution must be valid and complete"

def test_has_unique_solution():
    """Test that has_unique_solution correctly identifies puzzles with unique or multiple solutions"""
    
    # Test case 1: Puzzle with a unique solution
    unique_puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    board = SudokuBoard(unique_puzzle)
    assert board.has_unique_solution() is True, "The puzzle should have a unique solution"

    # Test case 2: Empty puzzle (multiple solutions)
    multiple_solution_puzzle = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    board = SudokuBoard(multiple_solution_puzzle)
    assert board.has_unique_solution() is False, "Empty puzzle should have multiple solutions"
    
    # Test case 3: Puzzle with only one empty cell (unique solution)
    one_empty_puzzle = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 0]
    ]
    board = SudokuBoard(one_empty_puzzle)
    assert board.has_unique_solution() is True, "Puzzle with one empty cell should have unique solution"
