# puzzle_cache.py
# 預生成困難題目緩存系統

import json
import os
import random
import time
from SUDOKU import generate, SudokuBoard
from difficulty_engine import DifficultyEngine

try:
    from preset_puzzles import get_random_preset_puzzle, get_preset_count
    PRESET_AVAILABLE = True
except ImportError:
    PRESET_AVAILABLE = False
    print("⚠️ 預設題目庫不可用，將使用動態生成")

class PuzzleCache:
    """
    數獨題目緩存管理器
    預生成並緩存不同難度的題目，提高用戶體驗
    """
    
    def __init__(self, cache_file="puzzle_cache.json"):
        self.cache_file = cache_file
        self.engine = DifficultyEngine()
        self.cache = self.load_cache()
        
        # 每個難度級別的緩存目標數量 (減少以加快啟動，因為有預設題目支援)
        self.target_counts = {
            "Easy": 10,      # 減少 Easy 題目緩存
            "Medium": 5,     # 大幅減少 Medium 題目緩存
            "Hard": 3        # 大幅減少 Hard 題目緩存
        }
        
        # 如果有預設題目，進一步減少緩存需求
        if PRESET_AVAILABLE:
            print(f"📋 預設題目可用，減少緩存需求以加快啟動")
            self.target_counts = {
                "Easy": 5,      # Easy: 5個緩存 + 3個預設 = 8個可用
                "Medium": 3,    # Medium: 3個緩存 + 3個預設 = 6個可用  
                "Hard": 2       # Hard: 2個緩存 + 3個預設 = 5個可用
            }
        
        # 不在初始化時立即建立緩存，改為延遲建立
        # self.ensure_cache()  # 移除這行以加快啟動速度
    
    def load_cache(self):
        """從文件載入緩存"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return {"Easy": [], "Medium": [], "Hard": []}
    
    def save_cache(self):
        """保存緩存到文件"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)
    
    def get_puzzle(self, difficulty):
        """
        獲取指定難度的題目
        
        Args:
            difficulty: "Easy", "Medium", or "Hard"
        
        Returns:
            tuple: (puzzle_grid, solution_grid) or None if not available
        """
        if difficulty in self.cache and self.cache[difficulty]:
            # 從緩存中隨機選擇一個題目
            puzzle_data = random.choice(self.cache[difficulty])
            puzzle_grid = puzzle_data["puzzle"]
            solution_grid = puzzle_data["solution"]
            
            # 創建SudokuBoard對象
            puzzle_board = SudokuBoard([row[:] for row in puzzle_grid])
            solution_board = SudokuBoard([row[:] for row in solution_grid])
            
            # 從緩存中移除使用過的題目（避免重複）
            self.cache[difficulty].remove(puzzle_data)
            self.save_cache()
            
            return puzzle_board, solution_board
        
        # 如果沒有緩存，優先使用預設題目
        if PRESET_AVAILABLE:
            preset_puzzle = get_random_preset_puzzle(difficulty)
            if preset_puzzle:
                print(f"📋 Using preset {difficulty} puzzle...")
                puzzle_board = SudokuBoard([row[:] for row in preset_puzzle["puzzle"]])
                solution_board = SudokuBoard([row[:] for row in preset_puzzle["solution"]])
                
                return puzzle_board, solution_board
        
        # 如果沒有預設題目，快速生成一個題目以保持響應性
        print(f"⚡ No {difficulty} cache/preset available, quick generation...")
        return self._generate_single_puzzle_quick(difficulty)
    
    def _generate_single_puzzle_quick(self, difficulty):
        """快速生成單個題目，用於緩存為空時的即時響應"""
        from SUDOKU import generate
        
        try:
            if difficulty == "Hard":
                # Hard題目使用較少嘗試次數來保持響應性
                return generate(random.randint(52, 58), max_attempts=5)
            elif difficulty == "Medium":
                return generate(random.randint(42, 50), max_attempts=3)
            else:  # Easy
                return generate(random.randint(32, 40), max_attempts=2)
        except Exception as e:
            print(f"⚠️ Quick generation failed: {e}, using simple fallback...")
            # 簡單的後備方案
            return generate(40, max_attempts=2)
    
    def add_puzzle(self, difficulty, puzzle_board, solution_board):
        """
        添加題目到緩存
        
        Args:
            difficulty: 題目難度
            puzzle_board: SudokuBoard 題目
            solution_board: SudokuBoard 解答
        """
        puzzle_data = {
            "puzzle": puzzle_board.grid,
            "solution": solution_board.grid,
            "timestamp": time.time()
        }
        
        if difficulty not in self.cache:
            self.cache[difficulty] = []
        
        self.cache[difficulty].append(puzzle_data)
        
        # 限制緩存大小，保留最新的題目
        max_cache_size = self.target_counts.get(difficulty, 15) * 2
        if len(self.cache[difficulty]) > max_cache_size:
            # 按時間戳排序，保留較新的
            self.cache[difficulty].sort(key=lambda x: x["timestamp"], reverse=True)
            self.cache[difficulty] = self.cache[difficulty][:max_cache_size]
        
        self.save_cache()
    
    def ensure_cache(self, progress_callback=None):
        """確保每個難度都有足夠的緩存題目"""
        total_needed = 0
        for difficulty, target_count in self.target_counts.items():
            current_count = len(self.cache.get(difficulty, []))
            if current_count < target_count:
                total_needed += target_count - current_count
        
        if total_needed == 0:
            if progress_callback:
                progress_callback(100, "緩存已完整")
            return
            
        completed = 0
        for difficulty, target_count in self.target_counts.items():
            current_count = len(self.cache.get(difficulty, []))
            
            if current_count < target_count:
                needed = target_count - current_count
                print(f"🔄 Generating {needed} {difficulty} puzzles for cache...")
                
                def sub_progress(sub_completed, sub_total, message=""):
                    nonlocal completed
                    overall_progress = int(((completed + sub_completed) / total_needed) * 100)
                    if progress_callback:
                        progress_callback(overall_progress, f"生成 {difficulty} 題目: {sub_completed}/{sub_total}")
                
                self.generate_puzzles_for_cache(difficulty, needed, sub_progress)
                completed += needed
    
    def generate_puzzles_for_cache(self, difficulty, count, progress_callback=None):
        """
        為緩存生成指定數量的題目
        
        Args:
            difficulty: 目標難度
            count: 需要生成的數量
            progress_callback: 進度回調函數 (completed, total, message)
        """
        generated = 0
        max_attempts_per_puzzle = 100 if difficulty == "Hard" else 50
        
        # Hard題目使用更智能的策略
        if difficulty == "Hard":
            empty_cells_range = (52, 60)  # 更多空格通常更困難
        elif difficulty == "Medium":
            empty_cells_range = (42, 50)
        else:  # Easy
            empty_cells_range = (32, 40)
        
        total_attempts = 0
        
        while generated < count and total_attempts < count * max_attempts_per_puzzle:
            try:
                # 使用漸進式策略生成Hard題目
                if difficulty == "Hard":
                    puzzle, solution = self.generate_hard_puzzle_smart()
                else:
                    # 一般生成方法
                    min_cells, max_cells = empty_cells_range
                    empty_cells = random.randint(min_cells, max_cells)
                    puzzle, solution = generate(empty_cells, max_attempts=20)
                
                # 驗證難度
                rated_difficulty, score, techniques = self.engine.rate_puzzle(puzzle)
                
                if rated_difficulty == difficulty:
                    self.add_puzzle(difficulty, puzzle, solution)
                    generated += 1
                    print(f"  ✅ Generated {difficulty} puzzle {generated}/{count} (score: {score})")
                    
                    # 更新進度
                    if progress_callback:
                        progress_callback(generated, count, f"已生成 {generated}/{count} 個 {difficulty} 題目")
                
                total_attempts += 1
                
                # 每50次嘗試顯示進度
                if total_attempts % 50 == 0:
                    print(f"  🔄 Progress: {generated}/{count} generated, {total_attempts} attempts")
                    
            except Exception as e:
                print(f"  ⚠️ Error generating {difficulty} puzzle: {e}")
                total_attempts += 1
        
        if generated < count:
            print(f"  ⚠️ Only generated {generated}/{count} {difficulty} puzzles")
    
    def generate_hard_puzzle_smart(self):
        """
        智能生成Hard難度題目的策略
        使用多階段挖洞法，更容易產生需要高級技巧的題目
        """
        max_attempts = 50
        
        for attempt in range(max_attempts):
            # 1. 生成完整解答
            empty_grid = [[0] * 9 for _ in range(9)]
            solution = SudokuBoard(empty_grid)
            solution.solve(randomize=True)
            
            # 2. 多階段挖洞策略
            puzzle = SudokuBoard(solution.grid)
            
            # 階段1: 移除一些隨機單元格 (35-40個)
            stage1_removals = random.randint(35, 40)
            self.remove_cells_random(puzzle, stage1_removals)
            
            # 階段2: 針對性移除可能產生高級模式的位置 (10-15個)
            stage2_removals = random.randint(10, 15)
            self.remove_cells_strategic(puzzle, stage2_removals)
            
            # 3. 驗證唯一解
            if puzzle.has_unique_solution():
                return puzzle, solution
        
        # 如果智能策略失敗，回退到常規方法
        return generate(random.randint(52, 58), max_attempts=20)
    
    def remove_cells_random(self, puzzle, count):
        """隨機移除指定數量的格子"""
        positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(positions)
        
        removed = 0
        for row, col in positions:
            if removed >= count:
                break
            if puzzle.grid[row][col] != 0:
                puzzle.grid[row][col] = 0
                removed += 1
    
    def remove_cells_strategic(self, puzzle, count):
        """
        策略性移除格子，優先選擇可能產生高級模式的位置
        如：行列交叉點、宮邊界位置等
        """
        # 優先位置：宮邊界和中心位置
        strategic_positions = []
        
        # 宮邊界位置 (更可能形成 pointing pairs, X-wing 等)
        for box_row in range(3):
            for box_col in range(3):
                base_r, base_c = box_row * 3, box_col * 3
                # 邊界位置
                strategic_positions.extend([
                    (base_r, base_c), (base_r, base_c + 2),
                    (base_r + 2, base_c), (base_r + 2, base_c + 2),
                    (base_r + 1, base_c), (base_r + 1, base_c + 2),
                    (base_r, base_c + 1), (base_r + 2, base_c + 1)
                ])
        
        # 隨機化順序
        random.shuffle(strategic_positions)
        
        removed = 0
        for row, col in strategic_positions:
            if removed >= count:
                break
            if puzzle.grid[row][col] != 0:
                puzzle.grid[row][col] = 0
                removed += 1
        
        # 如果還沒移除夠，用隨機位置補足
        if removed < count:
            remaining = count - removed
            self.remove_cells_random(puzzle, remaining)
    
    def get_cache_status(self):
        """獲取緩存狀態"""
        status = {}
        for difficulty in ["Easy", "Medium", "Hard"]:
            count = len(self.cache.get(difficulty, []))
            target = self.target_counts[difficulty]
            status[difficulty] = {"current": count, "target": target}
        return status
    
    def clear_cache(self, difficulty=None):
        """清空緩存"""
        if difficulty:
            self.cache[difficulty] = []
        else:
            self.cache = {"Easy": [], "Medium": [], "Hard": []}
        self.save_cache()
