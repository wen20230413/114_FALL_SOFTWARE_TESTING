#!/usr/bin/env python3
"""
Sudoku GUI using tkinter
Integrates with existing difficulty rating system
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import threading
import time
from SUDOKU import SudokuBoard, generate
from difficulty_engine import DifficultyEngine
from puzzle_cache import PuzzleCache


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver with Difficulty Rating")
        
        # Initialize difficulty engine and puzzle cache
        self.engine = DifficultyEngine()
        self.puzzle_cache = PuzzleCache()
        
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
        
        # Initialize progress tracking
        self.cache_build_in_progress = False
        
        # Initialize undo/redo system
        self.move_history = []
        self.undo_stack = []
        self.redo_stack = []
        
        # 延遲緩存檢查，讓GUI先啟動
        self.root.after(100, self.check_and_build_cache_delayed)
        
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
        
        # Hint button
        tk.Button(
            button_frame,
            text="💡 Hint",
            command=self.show_hint,
            font=("Arial", 12),
            bg="#9C27B0",
            fg="white",
            padx=20,
            pady=5
        ).pack(side="left", padx=5)
        
        # Second row of buttons
        button_frame2 = tk.Frame(main_frame, bg=self.BG_COLOR)
        button_frame2.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Undo button
        self.undo_button = tk.Button(
            button_frame2,
            text="↶ Undo",
            command=self.undo_move,
            font=("Arial", 10),
            bg="#607D8B",
            fg="white",
            padx=15,
            pady=3,
            state="disabled"
        )
        self.undo_button.pack(side="left", padx=5)
        
        # Redo button
        self.redo_button = tk.Button(
            button_frame2,
            text="↷ Redo", 
            command=self.redo_move,
            font=("Arial", 10),
            bg="#607D8B",
            fg="white",
            padx=15,
            pady=3,
            state="disabled"
        )
        self.redo_button.pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="Cache Status",
            command=self.show_cache_status,
            font=("Arial", 10),
            bg="#607D8B",
            fg="white",
            padx=15,
            pady=5
        ).pack(side="left", padx=5)
        
        # Status frame for cache progress
        self.status_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        self.status_frame.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Progress bar for cache building (initially hidden)
        self.progress_frame = tk.Frame(self.status_frame, bg=self.BG_COLOR)
        self.progress_label = tk.Label(self.progress_frame, text="", 
                                     font=("Arial", 9), bg=self.BG_COLOR)
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, 
                                          mode='determinate', 
                                          length=200)
        self.progress_bar.pack(pady=2)
        
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
        Uses cache system for faster generation, especially for Hard puzzles
        """
        target_difficulty = self.selected_difficulty.get()  # "Easy", "Medium", or "Hard"
        
        print(f"\n🎯 Getting {target_difficulty} puzzle...")
        
        # 1. 首先嘗試從緩存獲取
        cached_puzzle = self.puzzle_cache.get_puzzle(target_difficulty)
        
        if cached_puzzle:
            # 使用緩存的題目
            self.puzzle_board, self.solution_board = cached_puzzle
            print(f"✅ Using cached {target_difficulty} puzzle")
            
            # 在背景中生成新的題目補充緩存
            threading.Thread(
                target=self.replenish_cache_background, 
                args=(target_difficulty,), 
                daemon=True
            ).start()
            
        else:
            # 緩存中沒有，需要即時生成
            print(f"⚠️ No cached {target_difficulty} puzzle available, generating now...")
            self.puzzle_board, self.solution_board = self.generate_puzzle_immediate(target_difficulty)
        
        # 驗證並添加到緩存（如果是即時生成的）
        if not cached_puzzle:
            difficulty_rating, score, techniques = self.engine.rate_puzzle(self.puzzle_board)
            if difficulty_rating == target_difficulty:
                # 添加到緩存
                self.puzzle_cache.add_puzzle(target_difficulty, self.puzzle_board, self.solution_board)
        
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
        
        # Clear undo/redo history for new puzzle
        self.clear_undo_history()
        
        # Update display
        self.update_board()
    
    def generate_puzzle_immediate(self, target_difficulty):
        """
        即時生成題目（當緩存為空時使用）
        針對Hard題目使用更優化的策略
        """
        if target_difficulty == "Hard":
            # Hard題目使用智能策略，較少嘗試次數但更高成功率
            max_attempts = 15
            print("  🧠 Using smart generation for Hard puzzle...")
            
            for attempt in range(max_attempts):
                try:
                    puzzle, solution = self.puzzle_cache.generate_hard_puzzle_smart()
                    difficulty_rating, score, techniques = self.engine.rate_puzzle(puzzle)
                    
                    if difficulty_rating == "Hard":
                        print(f"  ✅ Generated Hard puzzle on attempt {attempt+1} (score: {score})")
                        return puzzle, solution
                    elif attempt % 3 == 0:
                        print(f"  🔄 Attempt {attempt+1}: Got {difficulty_rating} (score: {score})")
                        
                except Exception as e:
                    print(f"  ⚠️ Generation error on attempt {attempt+1}: {e}")
            
            # 如果智能策略失敗，使用常規方法
            print("  🔄 Smart generation failed, using fallback method...")
            return self.generate_puzzle_fallback(target_difficulty)
        
        else:
            # Easy/Medium 使用常規方法
            return self.generate_puzzle_fallback(target_difficulty)
    
    def generate_puzzle_fallback(self, target_difficulty):
        """
        回退生成方法（常規的重試機制）
        """
        empty_cells_range = {
            "Easy": (30, 40),
            "Medium": (40, 50),
            "Hard": (50, 58)
        }
        
        max_attempts = 20 if target_difficulty == "Hard" else 15
        best_puzzle = None
        best_solution = None
        
        for attempt in range(max_attempts):
            min_cells, max_cells = empty_cells_range[target_difficulty]
            empty_cells = random.randint(min_cells, max_cells)
            
            puzzle, solution = generate(empty_cells, max_attempts=10)
            difficulty_rating, score, techniques = self.engine.rate_puzzle(puzzle)
            
            if difficulty_rating == target_difficulty:
                print(f"  ✅ Found {target_difficulty} puzzle on attempt {attempt+1}")
                return puzzle, solution
            else:
                # 保留最佳嘗試
                if best_puzzle is None:
                    best_puzzle = puzzle
                    best_solution = solution
                
                if (attempt + 1) % 5 == 0:
                    print(f"  🔄 Attempt {attempt+1}: Got {difficulty_rating} (score: {score})")
        
        # 使用最佳嘗試
        print(f"  ⚠️ Using closest match after {max_attempts} attempts")
        return best_puzzle or puzzle, best_solution or solution
    
    def replenish_cache_background(self, difficulty):
        """
        在背景中補充緩存
        """
        def background_task():
            try:
                # 檢查緩存狀態
                status = self.puzzle_cache.get_cache_status()
                current = status[difficulty]["current"]
                target = status[difficulty]["target"]
                
                if current < target:
                    needed = min(3, target - current)  # 一次最多補充3個
                    print(f"🔄 Background: Replenishing {needed} {difficulty} puzzles...")
                    self.puzzle_cache.generate_puzzles_for_cache(difficulty, needed)
                    print(f"✅ Background: Cache replenished for {difficulty}")
                    
            except Exception as e:
                print(f"⚠️ Background cache replenishment error: {e}")
        
        # 短暫延遲後開始，避免影響用戶體驗
        time.sleep(1)
        background_task()
    
    def check_and_build_cache_delayed(self):
        """延遲檢查並建立緩存，確保GUI先啟動"""
        def progress_callback(progress, message):
            """進度回調函數"""
            self.root.after(0, lambda: self.update_progress_ui(progress, message))
        
        def build_cache_thread():
            """在背景線程中建立緩存"""
            try:
                self.cache_build_in_progress = True
                
                # 檢查是否需要建立緩存
                needs_cache = False
                for difficulty, target_count in self.puzzle_cache.target_counts.items():
                    current_count = len(self.puzzle_cache.cache.get(difficulty, []))
                    if current_count < target_count:
                        needs_cache = True
                        break
                
                if needs_cache:
                    self.root.after(0, self.show_progress_bar)
                    self.puzzle_cache.ensure_cache(progress_callback)
                    self.root.after(0, self.hide_progress_bar)
                
            except Exception as e:
                self.root.after(0, lambda: self.hide_progress_bar())
                print(f"Error building cache: {e}")
            finally:
                self.cache_build_in_progress = False
        
        # 在背景線程中檢查和建立緩存
        thread = threading.Thread(target=build_cache_thread, daemon=True)
        thread.start()
    
    def show_progress_bar(self):
        """顯示進度條"""
        if not hasattr(self, 'progress_frame'):
            return
        self.progress_frame.pack(pady=5)
    
    def hide_progress_bar(self):
        """隱藏進度條"""
        if not hasattr(self, 'progress_frame'):
            return
        self.progress_frame.pack_forget()
        self.progress_label.config(text="")
        self.progress_bar['value'] = 0
    
    def update_progress_ui(self, progress, message):
        """更新進度條UI"""
        if not hasattr(self, 'progress_bar'):
            return
        self.progress_bar['value'] = progress
        self.progress_label.config(text=message)
        self.root.update_idletasks()
    
    def show_cache_status(self):
        """顯示緩存狀態"""
        status = self.puzzle_cache.get_cache_status()
        
        message = "📦 Puzzle Cache Status:\n\n"
        for difficulty, info in status.items():
            current = info["current"]
            target = info["target"]
            percentage = (current / target * 100) if target > 0 else 0
            
            status_emoji = "✅" if current >= target else "⚠️" if current > 0 else "❌"
            message += f"{status_emoji} {difficulty}: {current}/{target} ({percentage:.0f}%)\n"
        
        message += f"\n💡 Hard puzzles are pre-generated for faster loading!"
        message += f"\n🔄 Cache is automatically replenished in background."
        
        messagebox.showinfo("Puzzle Cache Status", message)
    
    def show_hint(self):
        """提供解題提示"""
        if not hasattr(self, 'puzzle_board') or self.puzzle_board is None:
            messagebox.showwarning("提示", "請先生成一個數獨題目！")
            return
            
        if not hasattr(self, 'solution_board') or self.solution_board is None:
            messagebox.showwarning("提示", "沒有可用的解答！")
            return
        
        # 找到用戶沒有填寫的空格
        empty_cells = []
        user_errors = []
        
        for i in range(9):
            for j in range(9):
                if self.original_puzzle[i][j] == 0:  # 原題目中的空格
                    current_value = self.cells[i][j].cget("text")
                    if current_value == "" or current_value == " ":
                        # 用戶還沒填寫
                        empty_cells.append((i, j))
                    elif current_value.isdigit() and int(current_value) != self.solution_board.grid[i][j]:
                        # 用戶填寫錯誤
                        user_errors.append((i, j))
        
        # 優先提示錯誤
        if user_errors:
            row, col = user_errors[0]
            correct_value = self.solution_board.grid[row][col]
            current_value = self.cells[row][col].cget("text")
            
            # 高亮錯誤格子
            self.cells[row][col].config(bg="#FFCDD2")  # 淺紅色
            self.root.after(2000, lambda: self.cells[row][col].config(bg=self.CELL_BG))  # 2秒後恢復
            
            messagebox.showinfo("提示", 
                              f"位置 ({row+1},{col+1}) 的數字不正確！\n" +
                              f"您填寫的是 {current_value}，正確答案是 {correct_value}")
            return
        
        # 沒有錯誤，提供下一步提示
        if empty_cells:
            # 選擇一個空格給出答案
            row, col = empty_cells[0]
            correct_value = self.solution_board.grid[row][col]
            
            # 高亮提示格子
            self.cells[row][col].config(bg="#E8F5E8")  # 淺綠色
            self.root.after(3000, lambda: self.cells[row][col].config(bg=self.CELL_BG))  # 3秒後恢復
            
            # 詢問用戶是否要直接填入答案
            result = messagebox.askyesno("提示", 
                                       f"位置 ({row+1},{col+1}) 的正確答案是 {correct_value}\n\n" +
                                       "是否要自動填入這個答案？")
            
            if result:
                self.cells[row][col].config(text=str(correct_value), fg=self.SOLUTION_COLOR)
                self.cells[row][col].hint_filled = True  # 標記為提示填寫
        else:
            messagebox.showinfo("提示", "恭喜！您已經完成了這個數獨！🎉")
    
    def record_move(self, row, col, old_value, new_value):
        """記錄一個移動以供撤銷/重做"""
        move = {
            'row': row,
            'col': col, 
            'old_value': old_value,
            'new_value': new_value
        }
        self.undo_stack.append(move)
        # 清空重做堆疊，因為新的移動使重做無效
        self.redo_stack.clear()
        self.update_undo_redo_buttons()
    
    def undo_move(self):
        """撤銷上一個移動"""
        if not self.undo_stack:
            return
            
        move = self.undo_stack.pop()
        
        # 恢復舊值
        self.puzzle_board.grid[move['row']][move['col']] = move['old_value']
        
        # 將移動添加到重做堆疊
        self.redo_stack.append(move)
        
        self.update_board()
        self.update_undo_redo_buttons()
    
    def redo_move(self):
        """重做上一個撤銷的移動"""
        if not self.redo_stack:
            return
            
        move = self.redo_stack.pop()
        
        # 恢復新值
        self.puzzle_board.grid[move['row']][move['col']] = move['new_value']
        
        # 將移動添加到撤銷堆疊
        self.undo_stack.append(move)
        
        self.update_board()
        self.update_undo_redo_buttons()
    
    def update_undo_redo_buttons(self):
        """更新撤銷/重做按鈕的狀態"""
        # 更新撤銷按鈕
        if self.undo_stack:
            self.undo_button.config(state="normal")
        else:
            self.undo_button.config(state="disabled")
        
        # 更新重做按鈕
        if self.redo_stack:
            self.redo_button.config(state="normal")
        else:
            self.redo_button.config(state="disabled")
    
    def clear_undo_history(self):
        """清空撤銷歷史（在生成新題目時調用）"""
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.update_undo_redo_buttons()
    
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
        """Handle keyboard input with proper error handling"""
        if self.selected_cell is None:
            return
        
        # Skip non-character events (like Alt, Ctrl, etc.)
        if not hasattr(event, 'char') or not hasattr(event, 'keysym'):
            return
            
        row, col = self.selected_cell
        
        # Check if this is a fixed cell from original puzzle
        if self.original_puzzle[row][col] != 0:
            return  # Can't modify fixed cells
        
        try:
            # Handle number keys
            if event.char in "123456789":
                num = int(event.char)
                old_value = self.puzzle_board.grid[row][col]
                if old_value != num:  # Only record if value actually changes
                    self.record_move(row, col, old_value, num)
                    self.puzzle_board.grid[row][col] = num
                    self.update_board()
            
            # Handle delete/backspace/0
            elif event.keysym in ["Delete", "BackSpace"] or event.char == "0":
                old_value = self.puzzle_board.grid[row][col]
                if old_value != 0:  # Only record if value actually changes
                    self.record_move(row, col, old_value, 0)
                    self.puzzle_board.grid[row][col] = 0
                    self.update_board()
                
        except (ValueError, AttributeError) as e:
            # Silently ignore invalid input
            pass
        
        # Handle keyboard shortcuts
        if event.state & 0x4:  # Ctrl is pressed
            if event.keysym == 'z':  # Ctrl+Z
                self.undo_move()
                return
            elif event.keysym == 'y':  # Ctrl+Y
                self.redo_move() 
                return
        
        # Handle arrow keys (outside try block for navigation)
        if event.keysym == "Up" and row > 0:
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
