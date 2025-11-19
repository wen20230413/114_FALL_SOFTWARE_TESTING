# difficulty_engine.py
# Difficulty rating engine that simulates human solving logic

import copy
from solving_techniques import SudokuTechniques

class DifficultyEngine:
    """
    難度評分引擎
    
    根據求解過程中需要使用的技巧來評估題目難度。
    模擬人類解題過程，而非計算機回溯演算法。
    """
    
    # 技巧階層與分數對應表
    # 參考來源: Sudoku Solving Techniques Hierarchy (SE Rating)
    # Easy: 10-15, Medium: 50-90, Hard: 120+, Expert: 160+
    TECHNIQUE_SCORES = {
        'naked_single': 15,      # Easy - Direct observation
        'hidden_single': 15,     # Easy - Single candidate in unit
        'naked_pair': 65,        # Medium - Candidate pattern in 2 cells
        'hidden_pair': 70,       # Medium - (Not implemented yet)
        'pointing_pair': 80,     # Medium - Box-line reduction
        'x_wing': 120,           # Hard - 2x2 rectangular pattern
        'swordfish': 160,        # Hard - 3x3 pattern
        'xy_wing': 180,          # Expert - Pivot pattern with bi-value cells
    }
    
    def rate_puzzle(self, board):
        """
        評估題目難度
        
        Args:
            board: SudokuBoard 實例
        
        Returns:
            tuple: (difficulty, max_score, techniques_used)
                - difficulty: 'Easy', 'Medium', 或 'Hard'
                - max_score: 最高技巧分數
                - techniques_used: 使用過的技巧列表
        """
        # 創建工作副本
        working_board = copy.deepcopy(board)
        techniques_used = []
        max_score = 0
        
        # 模擬人類求解過程
        iteration = 0
        max_iterations = 1000  # 防止無窮迴圈
        
        while not self._is_solved(working_board) and iteration < max_iterations:
            iteration += 1
            tech = SudokuTechniques(working_board)
            applied = False
            
            # 1. 嘗試 Naked Singles（最簡單）
            if singles := tech.find_naked_singles():
                for row, col, num in singles:
                    working_board.grid[row][col] = num
                techniques_used.append('naked_single')
                max_score = max(max_score, self.TECHNIQUE_SCORES['naked_single'])
                applied = True
                continue
            
            # 2. 嘗試 Hidden Singles
            if hidden := tech.find_hidden_singles():
                for row, col, num in hidden:
                    working_board.grid[row][col] = num
                techniques_used.append('hidden_single')
                max_score = max(max_score, self.TECHNIQUE_SCORES['hidden_single'])
                applied = True
                continue
            
            # 3. 嘗試 Naked Pairs（Medium 難度）
            if pairs := tech.find_naked_pairs():
                eliminated = tech.apply_naked_pairs(pairs)
                if eliminated > 0:
                    techniques_used.append('naked_pair')
                    max_score = max(max_score, self.TECHNIQUE_SCORES['naked_pair'])
                    applied = True
                    continue
            
            # 4. 嘗試 Pointing Pairs（Medium 難度）
            if pointing := tech.find_pointing_pairs():
                eliminated = tech.apply_pointing_pairs(pointing)
                if eliminated > 0:
                    techniques_used.append('pointing_pair')
                    max_score = max(max_score, self.TECHNIQUE_SCORES['pointing_pair'])
                    applied = True
                    continue
            
            # 5. 嘗試 X-Wing（Hard 難度）
            if x_wing := tech.find_x_wing():
                eliminated = tech.apply_x_wing(x_wing)
                if eliminated > 0:
                    techniques_used.append('x_wing')
                    max_score = max(max_score, self.TECHNIQUE_SCORES['x_wing'])
                    applied = True
                    continue
            
            # 6. 嘗試 Swordfish（Hard 難度，比 X-Wing 更難）
            if swordfish := tech.find_swordfish():
                eliminated = tech.apply_swordfish(swordfish)
                if eliminated > 0:
                    techniques_used.append('swordfish')
                    max_score = max(max_score, self.TECHNIQUE_SCORES['swordfish'])
                    applied = True
                    continue
            
            # 7. 嘗試 XY-Wing（Expert 難度）
            if xy_wing := tech.find_xy_wing():
                eliminated = tech.apply_xy_wing(xy_wing)
                if eliminated > 0:
                    techniques_used.append('xy_wing')
                    max_score = max(max_score, self.TECHNIQUE_SCORES['xy_wing'])
                    applied = True
                    continue
            
            # 如果沒有任何技巧可用，需要更高階技巧
            if not applied:
                # 題目需要 Expert 級技巧（Swordfish, XY-Wing, AIC 等）
                # 超出目前實作範圍,標記為需要專家技巧
                max_score = max(max_score, 200)
                techniques_used.append('requires_expert_technique')
                break  # 停止評估,因為超出實作技巧範圍
        
        # 根據最高分數分類
        if max_score <= 15:
            difficulty = 'Easy'
        elif max_score <= 90:
            difficulty = 'Medium'
        else:
            difficulty = 'Hard'
        
        return difficulty, max_score, techniques_used
    
    def _is_solved(self, board):
        """檢查棋盤是否已解決"""
        for row in board.grid:
            if 0 in row:
                return False
        return True
