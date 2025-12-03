#!/usr/bin/env python3
"""
Sudoku GUI using tkinter
Integrates with existing difficulty rating system
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
from SUDOKU import SudokuBoard, generate
from difficulty_engine import DifficultyEngine


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver with Difficulty Rating")
        
        # Initialize difficulty engine
        self.engine = DifficultyEngine()
        
        # Game state
        self.puzzle_board = None
        self.solution_board = None
        self.original_puzzle = None  # Store original puzzle to distinguish fixed cells
        self.user_progress = None  # Store user's solving progress
        self.selected_cell = None
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.selected_difficulty = tk.StringVar(value="Easy")  # Default difficulty = Easy (by complexity)
        self.solution_shown = False  # Track if solution is currently shown
        self.show_errors = False  # Track if errors should be highlighted
        
        # Colors
        self.BG_COLOR = "#F0F0F0"
        self.CELL_BG = "white"
        self.FIXED_COLOR = "#333333"
        self.USER_COLOR = "#0066CC"
        self.SOLUTION_COLOR = "#2E7D32"  # Green for solution cells
        self.SELECTED_COLOR = "#BBDEFB"
        self.RELATED_COLOR = "#E3F2FD"  # Light blue for same row/col/box
        self.ERROR_COLOR = "#FFCDD2"
        
        self.setup_ui()
        self.generate_new_puzzle()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        main_frame.pack(padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Sudoku Solver", 
            font=("Arial", 20, "bold"),
            bg=self.BG_COLOR
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Board frame
        board_frame = tk.Frame(main_frame, bg="black")
        board_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Create 9x9 grid of cells
        for i in range(9):
            for j in range(9):
                cell_frame = tk.Frame(
                    board_frame,
                    bg="black",
                    width=50,
                    height=50
                )
                cell_frame.grid(
                    row=i, 
                    column=j, 
                    padx=(2 if j % 3 == 0 else 1, 2 if j == 8 else 1),
                    pady=(2 if i % 3 == 0 else 1, 2 if i == 8 else 1)
                )
                
                cell = tk.Label(
                    cell_frame,
                    text="",
                    font=("Arial", 18),
                    bg=self.CELL_BG,
                    width=3,
                    height=1
                )
                cell.pack(expand=True, fill="both")
                cell.bind("<Button-1>", lambda e, row=i, col=j: self.cell_clicked(row, col))
                
                self.cells[i][j] = cell
        
        # Info frame
        info_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        info_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Difficulty selection frame
        difficulty_selection_frame = tk.Frame(info_frame, bg=self.BG_COLOR)
        difficulty_selection_frame.pack(pady=5)
        
        tk.Label(
            difficulty_selection_frame,
            text="Select Difficulty:",
            font=("Arial", 11, "bold"),
            bg=self.BG_COLOR
        ).pack(side="left", padx=5)
        
        # Radio buttons for difficulty (based on solving complexity, not empty cells)
        difficulties = [("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")]
        for text, value in difficulties:
            tk.Radiobutton(
                difficulty_selection_frame,
                text=text,
                variable=self.selected_difficulty,
                value=value,
                font=("Arial", 10),
                bg=self.BG_COLOR,
                command=self.on_difficulty_change
            ).pack(side="left", padx=5)
        
        self.difficulty_label = tk.Label(
            info_frame,
            text="Puzzle Complexity: -",
            font=("Arial", 11),
            bg=self.BG_COLOR
        )
        self.difficulty_label.pack(pady=5)
        
        self.techniques_label = tk.Label(
            info_frame,
            text="",
            font=("Arial", 9),
            bg=self.BG_COLOR,
            wraplength=500,
            justify="left"
        )
        self.techniques_label.pack()
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        tk.Button(
            button_frame,
            text="New Puzzle",
            command=self.generate_new_puzzle,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="Check Solution",
            command=self.check_solution,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=5
        ).pack(side="left", padx=5)
        
        # Store reference to show solution button for text updates
        self.show_solution_button = tk.Button(
            button_frame,
            text="Show Solution",
            command=self.toggle_solution,
            font=("Arial", 12),
            bg="#FF9800",
            fg="white",
            width=15,  # Fixed width to prevent resizing
            padx=20,
            pady=5
        )
        self.show_solution_button.pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_user_inputs,
            font=("Arial", 12),
            bg="#F44336",
            fg="white",
            padx=20,
            pady=5
        ).pack(side="left", padx=5)
        
        # Bind keyboard events
        self.root.bind("<Key>", self.key_pressed)
    
    def on_difficulty_change(self):
        """Called when difficulty selection changes"""
        # Optionally auto-generate new puzzle when difficulty changes
        # Uncomment the next line if you want automatic regeneration
        # self.generate_new_puzzle()
        pass
    
    def generate_new_puzzle(self):
        """
        Generate a new Sudoku puzzle matching the selected difficulty level
        Uses DifficultyEngine to ensure the puzzle matches the target complexity
        """
        target_difficulty = self.selected_difficulty.get()  # "Easy", "Medium", or "Hard"
        
        print(f"\n🎯 Generating {target_difficulty} puzzle...")
        
        # Difficulty ranges for empty cells (starting estimates)
        empty_cells_range = {
            "Easy": (30, 40),
            "Medium": (40, 50),
            "Hard": (50, 58)
        }
        
        max_attempts = 30
        best_puzzle = None
        best_solution = None
        best_score = None
        
        for attempt in range(max_attempts):
            # Start with a random number of empty cells in the range
            min_cells, max_cells = empty_cells_range[target_difficulty]
            empty_cells = random.randint(min_cells, max_cells)
            
            # Generate puzzle
            puzzle, solution = generate(empty_cells)
            
            # Evaluate difficulty
            difficulty_rating, score, techniques = self.engine.rate_puzzle(puzzle)
            
            # Check if it matches target
            if difficulty_rating == target_difficulty:
                # Perfect match!
                self.puzzle_board = puzzle
                self.solution_board = solution
                best_score = score
                print(f"✅ Found {target_difficulty} puzzle on attempt {attempt+1}")
                break
            else:
                # Keep track of best attempt
                if best_puzzle is None:
                    best_puzzle = puzzle
                    best_solution = solution
                    best_score = score
                
                # Print progress every 5 attempts
                if (attempt + 1) % 5 == 0:
                    print(f"  Attempt {attempt+1}: Got {difficulty_rating} (score: {score}), retrying...")
        else:
            # If no perfect match found, use best attempt
            print(f"⚠️  Using closest match after {max_attempts} attempts")
            self.puzzle_board = best_puzzle
            self.solution_board = best_solution
        
        # Store original puzzle for comparison
        self.original_puzzle = [row[:] for row in self.puzzle_board.grid]
        
        # Reset solution shown state
        self.solution_shown = False
        self.user_progress = None
        self.show_solution_button.config(text="Show Solution")
        
        # Reset error highlighting
        self.show_errors = False
        
        # Rate the puzzle difficulty
        difficulty_rating, score, techniques = self.engine.rate_puzzle(self.puzzle_board)
        
        # Count empty cells
        empty_count = sum(row.count(0) for row in self.puzzle_board.grid)
        
        # Print detailed info to terminal
        print("\n" + "="*60)
        print(f"🎮 New Puzzle Generated")
        print("="*60)
        print(f"Target Difficulty: {target_difficulty}")
        print(f"Evaluated Complexity: {difficulty_rating} (score: {score})")
        print(f"Empty cells: {empty_count}")
        
        # Format techniques (count occurrences)
        from collections import Counter
        tech_counter = Counter(techniques)
        print(f"\nTechniques used to solve:")
        for name, count in tech_counter.items():
            print(f"  • {name}: {count} times")
        print("="*60 + "\n")
        
        # Update info label - show only simple info on GUI
        self.difficulty_label.config(
            text=f"Difficulty: {difficulty_rating} (score: {score}) | {empty_count} empty cells"
        )
        
        # Hide techniques label (info now in terminal)
        self.techniques_label.config(text="")
        
        # Clear selection
        self.selected_cell = None
        
        # Update display
        self.update_board()
    
    def update_board(self):
        """Update the visual display of the board"""
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                value = self.puzzle_board.grid[i][j]
                
                if value != 0:
                    # Check if this is an original fixed cell
                    if self.original_puzzle[i][j] != 0:
                        # Original puzzle cell - dark gray
                        cell.config(
                            text=str(value),
                            fg=self.FIXED_COLOR,
                            font=("Arial", 18, "bold")
                        )
                    else:
                        # Cell filled by user or solution - check if it's from solution
                        cell.config(
                            text=str(value),
                            fg=self.SOLUTION_COLOR,  # Green for solution cells
                            font=("Arial", 18)
                        )
                else:
                    cell.config(text="", fg=self.USER_COLOR)
                
                # Set background color with priority system
                bg_color = self.CELL_BG  # Default white
                
                # Check if cell is in same row/col/box as selected cell
                if self.selected_cell is not None:
                    sel_row, sel_col = self.selected_cell
                    
                    # Check if in same row, column, or 3x3 box
                    same_row = (i == sel_row)
                    same_col = (j == sel_col)
                    same_box = (i // 3 == sel_row // 3 and j // 3 == sel_col // 3)
                    
                    if i == sel_row and j == sel_col:
                        # This is the selected cell
                        bg_color = self.SELECTED_COLOR
                    elif same_row or same_col or same_box:
                        # Related cell (same row/col/box)
                        bg_color = self.RELATED_COLOR
                
                # Override with error color if needed
                if self.show_errors and value != 0 and self.original_puzzle[i][j] == 0:
                    # User-filled cell - check if it's wrong
                    if value != self.solution_board.grid[i][j]:
                        bg_color = self.ERROR_COLOR  # Red for errors (highest priority)
                
                cell.config(bg=bg_color)
    
    def cell_clicked(self, row, col):
        """Handle cell click event"""
        self.selected_cell = (row, col)
        self.update_board()
    
    def key_pressed(self, event):
        """Handle keyboard input"""
        if self.selected_cell is None:
            return
        
        row, col = self.selected_cell
        
        # Check if this is a fixed cell from original puzzle
        if self.original_puzzle[row][col] != 0:
            return  # Can't modify fixed cells
        
        # Handle number keys
        if event.char in "123456789":
            num = int(event.char)
            self.puzzle_board.grid[row][col] = num
            self.update_board()
        
        # Handle delete/backspace
        elif event.keysym in ["Delete", "BackSpace", "0"]:
            self.puzzle_board.grid[row][col] = 0
            self.update_board()
        
        # Handle arrow keys
        elif event.keysym == "Up" and row > 0:
            self.selected_cell = (row - 1, col)
            self.update_board()
        elif event.keysym == "Down" and row < 8:
            self.selected_cell = (row + 1, col)
            self.update_board()
        elif event.keysym == "Left" and col > 0:
            self.selected_cell = (row, col - 1)
            self.update_board()
        elif event.keysym == "Right" and col < 8:
            self.selected_cell = (row, col + 1)
            self.update_board()
    
    def check_solution(self):
        """Check if the current solution is correct and highlight errors"""
        # Toggle error highlighting
        if self.show_errors:
            # Turn off error highlighting
            self.show_errors = False
            self.update_board()
        else:
            # Turn on error highlighting
            self.show_errors = True
            
            # Count errors and empty cells
            error_count = 0
            empty_count = 0
            
            for i in range(9):
                for j in range(9):
                    value = self.puzzle_board.grid[i][j]
                    if value == 0:
                        empty_count += 1
                    elif self.original_puzzle[i][j] == 0:  # User-filled cell
                        if value != self.solution_board.grid[i][j]:
                            error_count += 1
            
            self.update_board()
            
            # Update check button text or show status
            if error_count == 0 and empty_count == 0:
                # Puzzle solved correctly!
                messagebox.showinfo("Success!", "Congratulations! You solved the puzzle correctly!")
                self.show_errors = False
                self.update_board()
            # Note: We don't show messagebox for errors, just highlight them
    
    def toggle_solution(self):
        """Toggle between showing solution and user progress"""
        if not self.solution_shown:
            # Save current progress before showing solution
            self.user_progress = [row[:] for row in self.puzzle_board.grid]
            
            # Show solution
            self.puzzle_board.grid = [row[:] for row in self.solution_board.grid]
            self.solution_shown = True
            
            # Turn off error highlighting when showing solution
            self.show_errors = False
            
            # Update button text
            self.show_solution_button.config(text="Hide Solution")
            
            self.update_board()
        else:
            # Restore user progress
            self.puzzle_board.grid = [row[:] for row in self.user_progress]
            self.solution_shown = False
            
            # Update button text
            self.show_solution_button.config(text="Show Solution")
            
            self.update_board()
    
    def clear_user_inputs(self):
        """Clear all user inputs, keeping original puzzle"""
        # Reset to original puzzle state
        self.puzzle_board.grid = [row[:] for row in self.original_puzzle]
        
        # Reset solution shown flag
        self.solution_shown = False
        self.user_progress = None
        self.show_solution_button.config(text="Show Solution")
        
        # Reset error highlighting
        self.show_errors = False
        
        # Clear selection
        self.selected_cell = None
        
        # Update display
        self.update_board()


def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
