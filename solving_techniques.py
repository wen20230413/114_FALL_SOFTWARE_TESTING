# solving_techniques.py
# Human-like Sudoku solving techniques detector

import copy

class SudokuTechniques:
    """
    檢測和應用人類求解技巧
    
    支援的技巧：
    - Naked Singles: 某格只有一個候選數字
    - Hidden Singles: 某數字在某單元中只能在一個位置
    - Naked Pairs: 兩個格子有相同的兩個候選數字
    - Pointing Pairs: 某數字在宮內只出現在同一行/列
    """
    
    def __init__(self, board):
        """
        初始化技巧檢測器
        
        Args:
            board: SudokuBoard 實例
        """
        self.board = board
        self.grid = board.grid
        self.candidates = self._init_candidates()
    
    def _init_candidates(self):
        """
        為每個空格計算候選數字
        
        Returns:
            dict: {(row, col): set(candidates)}
        """
        candidates = {}
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    candidates[(row, col)] = self._get_candidates(row, col)
        return candidates
    
    def _get_candidates(self, row, col):
        """
        取得某格的所有候選數字
        
        Args:
            row: 行索引 (0-8)
            col: 列索引 (0-8)
        
        Returns:
            set: 可能的候選數字集合
        """
        if self.grid[row][col] != 0:
            return set()
        
        # 從 1-9 開始，排除不可能的數字
        possible = set(range(1, 10))
        
        # 排除同行的數字
        for c in range(9):
            if self.grid[row][c] != 0:
                possible.discard(self.grid[row][c])
        
        # 排除同列的數字
        for r in range(9):
            if self.grid[r][col] != 0:
                possible.discard(self.grid[r][col])
        
        # 排除同宮的數字
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if self.grid[r][c] != 0:
                    possible.discard(self.grid[r][c])
        
        return possible
    
    def find_naked_singles(self):
        """
        檢測 Naked Singles：某格只有一個候選數字
        
        這是最基本的求解技巧，當某個空格經過排除後只剩一個可能的數字時，
        該數字就是這個格子的答案。
        
        Returns:
            list: [(row, col, num), ...] 找到的 Naked Singles
        """
        results = []
        for (row, col), cands in self.candidates.items():
            if len(cands) == 1:
                num = list(cands)[0]
                results.append((row, col, num))
        return results
    
    def find_hidden_singles(self):
        """
        檢測 Hidden Singles：某數字在某單元中只能在一個位置
        
        在某個單元（行、列或宮）中，如果某個數字只能填在一個格子裡，
        即使該格子有多個候選數字，也可以確定該數字就是答案。
        
        Returns:
            list: [(row, col, num), ...] 找到的 Hidden Singles
        """
        results = []
        
        # 檢查每一行
        for row in range(9):
            results.extend(self._find_hidden_in_row(row))
        
        # 檢查每一列
        for col in range(9):
            results.extend(self._find_hidden_in_col(col))
        
        # 檢查每一宮
        for box_idx in range(9):
            results.extend(self._find_hidden_in_box(box_idx))
        
        # 去除重複項目（同一個格子可能在不同單元中被找到）
        return list(set(results))
    
    def _find_hidden_in_row(self, row):
        """在指定行中尋找 Hidden Singles"""
        results = []
        
        # 對每個數字 1-9
        for num in range(1, 10):
            # 如果這個數字已經在這一行中，跳過
            if num in self.grid[row]:
                continue
            
            # 找出這個數字可能出現的位置
            possible_positions = []
            for col in range(9):
                if (row, col) in self.candidates and num in self.candidates[(row, col)]:
                    possible_positions.append((row, col))
            
            # 如果只有一個位置可以放這個數字，那就是 Hidden Single
            if len(possible_positions) == 1:
                results.append((possible_positions[0][0], possible_positions[0][1], num))
        
        return results
    
    def _find_hidden_in_col(self, col):
        """在指定列中尋找 Hidden Singles"""
        results = []
        
        # 對每個數字 1-9
        for num in range(1, 10):
            # 如果這個數字已經在這一列中，跳過
            if num in [self.grid[r][col] for r in range(9)]:
                continue
            
            # 找出這個數字可能出現的位置
            possible_positions = []
            for row in range(9):
                if (row, col) in self.candidates and num in self.candidates[(row, col)]:
                    possible_positions.append((row, col))
            
            # 如果只有一個位置可以放這個數字，那就是 Hidden Single
            if len(possible_positions) == 1:
                results.append((possible_positions[0][0], possible_positions[0][1], num))
        
        return results
    
    def _find_hidden_in_box(self, box_idx):
        """在指定宮中尋找 Hidden Singles"""
        results = []
        
        # 計算宮的起始位置
        box_row = (box_idx // 3) * 3
        box_col = (box_idx % 3) * 3
        
        # 對每個數字 1-9
        for num in range(1, 10):
            # 檢查這個數字是否已經在這個宮中
            found = False
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    if self.grid[r][c] == num:
                        found = True
                        break
                if found:
                    break
            
            if found:
                continue
            
            # 找出這個數字可能出現的位置
            possible_positions = []
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    if (r, c) in self.candidates and num in self.candidates[(r, c)]:
                        possible_positions.append((r, c))
            
            # 如果只有一個位置可以放這個數字，那就是 Hidden Single
            if len(possible_positions) == 1:
                results.append((possible_positions[0][0], possible_positions[0][1], num))
        
        return results
    
    def update_candidates(self, row, col, num):
        """
        在填入一個數字後更新候選數字列表
        
        Args:
            row: 填入數字的行
            col: 填入數字的列
            num: 填入的數字
        """
        # 移除該格的候選數字
        if (row, col) in self.candidates:
            del self.candidates[(row, col)]
        
        # 更新同行的候選數字
        for c in range(9):
            if (row, c) in self.candidates:
                self.candidates[(row, c)].discard(num)
        
        # 更新同列的候選數字
        for r in range(9):
            if (r, col) in self.candidates:
                self.candidates[(r, col)].discard(num)
        
        # 更新同宮的候選數字
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) in self.candidates:
                    self.candidates[(r, c)].discard(num)
    
    def find_naked_pairs(self):
        """
        檢測 Naked Pairs：兩個格子有相同的兩個候選數字
        
        在某個單元（行、列或宮）中，如果有兩個格子都只有相同的兩個候選數字，
        那麼這兩個數字必定在這兩個格子中，可以從該單元的其他格子中排除這兩個數字。
        
        Returns:
            list: [('naked_pair', unit_type, unit_idx, cells, nums), ...]
                - unit_type: 'row', 'col', 或 'box'
                - unit_idx: 單元索引
                - cells: 形成 pair 的格子位置
                - nums: 構成 pair 的數字
        """
        results = []
        
        # 在每一行中尋找
        for row in range(9):
            results.extend(self._find_pairs_in_row(row))
        
        # 在每一列中尋找
        for col in range(9):
            results.extend(self._find_pairs_in_col(col))
        
        # 在每一宮中尋找
        for box_idx in range(9):
            results.extend(self._find_pairs_in_box(box_idx))
        
        return results
    
    def _find_pairs_in_row(self, row):
        """在指定行中尋找 Naked Pairs"""
        results = []
        
        # 找出該行中所有只有 2 個候選數字的格子
        bi_value_cells = []
        for col in range(9):
            if (row, col) in self.candidates and len(self.candidates[(row, col)]) == 2:
                bi_value_cells.append((row, col, self.candidates[(row, col)]))
        
        # 檢查是否有兩個格子有相同的候選數字
        for i in range(len(bi_value_cells)):
            for j in range(i + 1, len(bi_value_cells)):
                cell1 = bi_value_cells[i]
                cell2 = bi_value_cells[j]
                
                if cell1[2] == cell2[2]:  # 候選數字相同
                    pair_nums = tuple(sorted(cell1[2]))
                    results.append(('naked_pair', 'row', row, 
                                  [(cell1[0], cell1[1]), (cell2[0], cell2[1])], 
                                  pair_nums))
        
        return results
    
    def _find_pairs_in_col(self, col):
        """在指定列中尋找 Naked Pairs"""
        results = []
        
        # 找出該列中所有只有 2 個候選數字的格子
        bi_value_cells = []
        for row in range(9):
            if (row, col) in self.candidates and len(self.candidates[(row, col)]) == 2:
                bi_value_cells.append((row, col, self.candidates[(row, col)]))
        
        # 檢查是否有兩個格子有相同的候選數字
        for i in range(len(bi_value_cells)):
            for j in range(i + 1, len(bi_value_cells)):
                cell1 = bi_value_cells[i]
                cell2 = bi_value_cells[j]
                
                if cell1[2] == cell2[2]:  # 候選數字相同
                    pair_nums = tuple(sorted(cell1[2]))
                    results.append(('naked_pair', 'col', col, 
                                  [(cell1[0], cell1[1]), (cell2[0], cell2[1])], 
                                  pair_nums))
        
        return results
    
    def _find_pairs_in_box(self, box_idx):
        """在指定宮中尋找 Naked Pairs"""
        results = []
        
        # 計算宮的起始位置
        box_row = (box_idx // 3) * 3
        box_col = (box_idx % 3) * 3
        
        # 找出該宮中所有只有 2 個候選數字的格子
        bi_value_cells = []
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) in self.candidates and len(self.candidates[(r, c)]) == 2:
                    bi_value_cells.append((r, c, self.candidates[(r, c)]))
        
        # 檢查是否有兩個格子有相同的候選數字
        for i in range(len(bi_value_cells)):
            for j in range(i + 1, len(bi_value_cells)):
                cell1 = bi_value_cells[i]
                cell2 = bi_value_cells[j]
                
                if cell1[2] == cell2[2]:  # 候選數字相同
                    pair_nums = tuple(sorted(cell1[2]))
                    results.append(('naked_pair', 'box', box_idx, 
                                  [(cell1[0], cell1[1]), (cell2[0], cell2[1])], 
                                  pair_nums))
        
        return results
    
    def find_pointing_pairs(self):
        """
        檢測 Pointing Pairs（也稱為 Box-Line Reduction）
        
        在某個宮內，如果某個數字的候選位置都在同一行或同一列，
        那麼可以從該行/列的其他宮中排除這個數字。
        
        Returns:
            list: [('pointing_pair', box_idx, num, line_type, line_idx, positions), ...]
                - box_idx: 宮的索引
                - num: 數字
                - line_type: 'row' 或 'col'
                - line_idx: 行/列索引
                - positions: 該數字在宮內的位置
        """
        results = []
        
        # 檢查每一個宮
        for box_idx in range(9):
            box_row = (box_idx // 3) * 3
            box_col = (box_idx % 3) * 3
            
            # 對每個數字 1-9
            for num in range(1, 10):
                # 找出這個數字在該宮中的所有候選位置
                positions = []
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        if (r, c) in self.candidates and num in self.candidates[(r, c)]:
                            positions.append((r, c))
                
                if len(positions) < 2:
                    continue  # 少於 2 個位置，不形成 pointing pair
                
                # 檢查是否所有位置都在同一行
                if len(set(pos[0] for pos in positions)) == 1:
                    row = positions[0][0]
                    results.append(('pointing_pair', box_idx, num, 'row', row, positions))
                
                # 檢查是否所有位置都在同一列
                elif len(set(pos[1] for pos in positions)) == 1:
                    col = positions[0][1]
                    results.append(('pointing_pair', box_idx, num, 'col', col, positions))
        
        return results
    
    def apply_naked_pairs(self, pairs):
        """
        應用 Naked Pairs 消除候選數字
        
        Args:
            pairs: find_naked_pairs() 返回的結果
        
        Returns:
            int: 消除的候選數字數量
        """
        eliminated = 0
        
        for pair_info in pairs:
            _, unit_type, unit_idx, cells, nums = pair_info
            
            if unit_type == 'row':
                # 從該行的其他格子中移除這些數字
                row = unit_idx
                for col in range(9):
                    if (row, col) in self.candidates and (row, col) not in cells:
                        for num in nums:
                            if num in self.candidates[(row, col)]:
                                self.candidates[(row, col)].discard(num)
                                eliminated += 1
            
            elif unit_type == 'col':
                # 從該列的其他格子中移除這些數字
                col = unit_idx
                for row in range(9):
                    if (row, col) in self.candidates and (row, col) not in cells:
                        for num in nums:
                            if num in self.candidates[(row, col)]:
                                self.candidates[(row, col)].discard(num)
                                eliminated += 1
            
            elif unit_type == 'box':
                # 從該宮的其他格子中移除這些數字
                box_row = (unit_idx // 3) * 3
                box_col = (unit_idx % 3) * 3
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        if (r, c) in self.candidates and (r, c) not in cells:
                            for num in nums:
                                if num in self.candidates[(r, c)]:
                                    self.candidates[(r, c)].discard(num)
                                    eliminated += 1
        
        return eliminated
    
    def apply_pointing_pairs(self, pointings):
        """
        應用 Pointing Pairs 消除候選數字
        
        Args:
            pointings: find_pointing_pairs() 返回的結果
        
        Returns:
            int: 消除的候選數字數量
        """
        eliminated = 0
        
        for pointing_info in pointings:
            _, box_idx, num, line_type, line_idx, positions = pointing_info
            
            box_row = (box_idx // 3) * 3
            box_col = (box_idx % 3) * 3
            
            if line_type == 'row':
                # 從該行的其他宮中移除這個數字
                row = line_idx
                for col in range(9):
                    # 如果不在原宮內
                    if not (box_row <= row < box_row + 3 and box_col <= col < box_col + 3):
                        if (row, col) in self.candidates and num in self.candidates[(row, col)]:
                            self.candidates[(row, col)].discard(num)
                            eliminated += 1
            
            elif line_type == 'col':
                # 從該列的其他宮中移除這個數字
                col = line_idx
                for row in range(9):
                    # 如果不在原宮內
                    if not (box_row <= row < box_row + 3 and box_col <= col < box_col + 3):
                        if (row, col) in self.candidates and num in self.candidates[(row, col)]:
                            self.candidates[(row, col)].discard(num)
                            eliminated += 1
        
        return eliminated
    
    def find_x_wing(self):
        """
        檢測 X-Wing：某數字在兩行中只出現在相同的兩列（或兩列中只出現在相同的兩行）
        
        X-Wing 是一種進階技巧，當某個數字在兩行（或兩列）中只能放在相同的兩列（或兩行）時，
        形成一個矩形模式，可以從這兩列（或兩行）的其他位置排除該數字。
        
        Returns:
            list: [('x_wing', pattern_type, lines, cols_or_rows, num), ...]
                - pattern_type: 'rows' 或 'cols'
                - lines: 形成 X-Wing 的兩條線
                - cols_or_rows: 交叉的兩條線
                - num: 數字
        """
        results = []
        
        # 檢查行中的 X-Wing 模式
        for num in range(1, 10):
            results.extend(self._find_x_wing_in_rows(num))
        
        # 檢查列中的 X-Wing 模式
        for num in range(1, 10):
            results.extend(self._find_x_wing_in_cols(num))
        
        return results
    
    def _find_x_wing_in_rows(self, num):
        """在行中尋找 X-Wing 模式"""
        results = []
        
        # 找出每一行中該數字的候選位置（只考慮恰好 2 個位置的行）
        row_candidates = {}
        for row in range(9):
            positions = []
            for col in range(9):
                if (row, col) in self.candidates and num in self.candidates[(row, col)]:
                    positions.append(col)
            
            # 只有恰好 2 個候選位置的行才可能形成 X-Wing
            if len(positions) == 2:
                row_candidates[row] = tuple(positions)
        
        # 尋找兩行有相同候選列的情況
        rows = list(row_candidates.keys())
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                row1, row2 = rows[i], rows[j]
                if row_candidates[row1] == row_candidates[row2]:
                    # 找到 X-Wing！
                    cols = row_candidates[row1]
                    results.append(('x_wing', 'rows', (row1, row2), cols, num))
        
        return results
    
    def _find_x_wing_in_cols(self, num):
        """在列中尋找 X-Wing 模式"""
        results = []
        
        # 找出每一列中該數字的候選位置（只考慮恰好 2 個位置的列）
        col_candidates = {}
        for col in range(9):
            positions = []
            for row in range(9):
                if (row, col) in self.candidates and num in self.candidates[(row, col)]:
                    positions.append(row)
            
            # 只有恰好 2 個候選位置的列才可能形成 X-Wing
            if len(positions) == 2:
                col_candidates[col] = tuple(positions)
        
        # 尋找兩列有相同候選行的情況
        cols = list(col_candidates.keys())
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                col1, col2 = cols[i], cols[j]
                if col_candidates[col1] == col_candidates[col2]:
                    # 找到 X-Wing！
                    rows = col_candidates[col1]
                    results.append(('x_wing', 'cols', (col1, col2), rows, num))
        
        return results
    
    def apply_x_wing(self, x_wings):
        """
        應用 X-Wing 消除候選數字
        
        Args:
            x_wings: find_x_wing() 返回的結果
        
        Returns:
            int: 消除的候選數字數量
        """
        eliminated = 0
        
        for x_wing_info in x_wings:
            _, pattern_type, lines, cross_lines, num = x_wing_info
            
            if pattern_type == 'rows':
                # X-Wing 在行中：從這兩列的其他行中移除該數字
                row1, row2 = lines
                col1, col2 = cross_lines
                
                for row in range(9):
                    if row != row1 and row != row2:
                        # 從 col1 移除
                        if (row, col1) in self.candidates and num in self.candidates[(row, col1)]:
                            self.candidates[(row, col1)].discard(num)
                            eliminated += 1
                        # 從 col2 移除
                        if (row, col2) in self.candidates and num in self.candidates[(row, col2)]:
                            self.candidates[(row, col2)].discard(num)
                            eliminated += 1
            
            elif pattern_type == 'cols':
                # X-Wing 在列中：從這兩行的其他列中移除該數字
                col1, col2 = lines
                row1, row2 = cross_lines
                
                for col in range(9):
                    if col != col1 and col != col2:
                        # 從 row1 移除
                        if (row1, col) in self.candidates and num in self.candidates[(row1, col)]:
                            self.candidates[(row1, col)].discard(num)
                            eliminated += 1
                        # 從 row2 移除
                        if (row2, col) in self.candidates and num in self.candidates[(row2, col)]:
                            self.candidates[(row2, col)].discard(num)
                            eliminated += 1
        
        return eliminated

    def find_swordfish(self):
        """
        檢測 Swordfish：某數字在三行中只出現在相同的三列（或三列中只出現在相同的三行）
        
        Swordfish 是 X-Wing 的 3x3 擴展版本。當某個數字在三行中只能放在相同的三列時，
        形成一個 3x3 矩形模式，可以從這三列的其他位置排除該數字。
        
        Returns:
            list: [('swordfish', pattern_type, lines, cols_or_rows, num), ...]
                - pattern_type: 'rows' 或 'cols'
                - lines: 形成 Swordfish 的三條線 (tuple of 3)
                - cols_or_rows: 交叉的三條線 (tuple of 3)
                - num: 數字
        """
        results = []
        
        # 檢查行中的 Swordfish 模式
        for num in range(1, 10):
            results.extend(self._find_swordfish_in_rows(num))
        
        # 檢查列中的 Swordfish 模式
        for num in range(1, 10):
            results.extend(self._find_swordfish_in_cols(num))
        
        return results
    
    def _find_swordfish_in_rows(self, num):
        """在行中尋找 Swordfish 模式"""
        results = []
        
        # 找出每一行中該數字的候選位置（2-3 個位置的行才可能形成 Swordfish）
        row_candidates = {}
        for row in range(9):
            positions = []
            for col in range(9):
                if (row, col) in self.candidates and num in self.candidates[(row, col)]:
                    positions.append(col)
            
            # Swordfish 需要 2-3 個候選位置
            if 2 <= len(positions) <= 3:
                row_candidates[row] = set(positions)
        
        # 尋找三行的候選列的聯集恰好是 3 個列
        rows = list(row_candidates.keys())
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                for k in range(j + 1, len(rows)):
                    row1, row2, row3 = rows[i], rows[j], rows[k]
                    
                    # 計算三行候選列的聯集
                    union_cols = row_candidates[row1] | row_candidates[row2] | row_candidates[row3]
                    
                    # 如果聯集恰好是 3 個列，就形成 Swordfish
                    if len(union_cols) == 3:
                        results.append(('swordfish', 'rows', (row1, row2, row3), tuple(sorted(union_cols)), num))
        
        return results
    
    def _find_swordfish_in_cols(self, num):
        """在列中尋找 Swordfish 模式"""
        results = []
        
        # 找出每一列中該數字的候選位置（2-3 個位置的列才可能形成 Swordfish）
        col_candidates = {}
        for col in range(9):
            positions = []
            for row in range(9):
                if (row, col) in self.candidates and num in self.candidates[(row, col)]:
                    positions.append(row)
            
            # Swordfish 需要 2-3 個候選位置
            if 2 <= len(positions) <= 3:
                col_candidates[col] = set(positions)
        
        # 尋找三列的候選行的聯集恰好是 3 個行
        cols = list(col_candidates.keys())
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                for k in range(j + 1, len(cols)):
                    col1, col2, col3 = cols[i], cols[j], cols[k]
                    
                    # 計算三列候選行的聯集
                    union_rows = col_candidates[col1] | col_candidates[col2] | col_candidates[col3]
                    
                    # 如果聯集恰好是 3 個行，就形成 Swordfish
                    if len(union_rows) == 3:
                        results.append(('swordfish', 'cols', (col1, col2, col3), tuple(sorted(union_rows)), num))
        
        return results
    
    def apply_swordfish(self, swordfish_patterns):
        """
        應用 Swordfish 模式消除候選數
        
        Args:
            swordfish_patterns: find_swordfish() 返回的模式列表
        
        Returns:
            int: 消除的候選數數量
        """
        eliminated = 0
        
        for pattern in swordfish_patterns:
            _, pattern_type, lines, cross_lines, num = pattern
            
            if pattern_type == 'rows':
                # 行中的 Swordfish：從這三列的其他行中消除該數字
                rows = lines
                cols = cross_lines
                
                for col in cols:
                    for row in range(9):
                        # 不在 Swordfish 三行中的行，從該列消除候選數
                        if row not in rows:
                            if (row, col) in self.candidates and num in self.candidates[(row, col)]:
                                self.candidates[(row, col)].discard(num)
                                eliminated += 1
            
            else:  # pattern_type == 'cols'
                # 列中的 Swordfish：從這三行的其他列中消除該數字
                cols = lines
                rows = cross_lines
                
                for row in rows:
                    for col in range(9):
                        # 不在 Swordfish 三列中的列，從該行消除候選數
                        if col not in cols:
                            if (row, col) in self.candidates and num in self.candidates[(row, col)]:
                                self.candidates[(row, col)].discard(num)
                                eliminated += 1
        
        return eliminated

    def find_xy_wing(self):
        """
        檢測 XY-Wing：三個雙候選格形成樞紐模式
        
        XY-Wing 由三個雙候選格組成：
        - Pivot (樞紐): 有候選數 {X, Y}
        - Wing 1: 有候選數 {X, Z}，與 Pivot 在同一單元 (row/col/box)
        - Wing 2: 有候選數 {Y, Z}，與 Pivot 在同一單元 (row/col/box)
        
        如果一個格子能同時看到 Wing 1 和 Wing 2，則可以消除該格子的候選數 Z
        
        Returns:
            list: [('xy_wing', pivot, wing1, wing2, digit_to_eliminate), ...]
        """
        results = []
        
        # 1. 找出所有雙候選格 (bi-value cells)
        bi_value_cells = []
        for row in range(9):
            for col in range(9):
                if (row, col) in self.candidates and len(self.candidates[(row, col)]) == 2:
                    bi_value_cells.append((row, col, tuple(sorted(self.candidates[(row, col)]))))
        
        # 2. 嘗試每個雙候選格作為 Pivot
        for pivot_row, pivot_col, pivot_cands in bi_value_cells:
            X, Y = pivot_cands
            
            # 3. 找 Wing 1 (有 X 和另一個數字 Z 的格子)
            for wing1_row, wing1_col, wing1_cands in bi_value_cells:
                # Wing 1 必須與 Pivot 不同，且能被 Pivot 看到
                if (wing1_row, wing1_col) == (pivot_row, pivot_col):
                    continue
                if not self._can_see(pivot_row, pivot_col, wing1_row, wing1_col):
                    continue
                
                # Wing 1 必須包含 X
                if X not in wing1_cands:
                    continue
                
                # 找出 Z (Wing 1 中除了 X 的另一個數字)
                Z = [c for c in wing1_cands if c != X][0]
                
                # 4. 找 Wing 2 (有 Y 和 Z 的格子)
                for wing2_row, wing2_col, wing2_cands in bi_value_cells:
                    # Wing 2 必須與 Pivot 和 Wing 1 都不同
                    if (wing2_row, wing2_col) == (pivot_row, pivot_col):
                        continue
                    if (wing2_row, wing2_col) == (wing1_row, wing1_col):
                        continue
                    
                    # Wing 2 必須能被 Pivot 看到
                    if not self._can_see(pivot_row, pivot_col, wing2_row, wing2_col):
                        continue
                    
                    # Wing 2 必須恰好包含 Y 和 Z
                    if set(wing2_cands) == {Y, Z}:
                        # 找到 XY-Wing！
                        results.append(('xy_wing', 
                                      (pivot_row, pivot_col), 
                                      (wing1_row, wing1_col), 
                                      (wing2_row, wing2_col), 
                                      Z))
        
        return results
    
    def _can_see(self, r1, c1, r2, c2):
        """
        檢查兩個格子是否在同一單元 (row/col/box)
        
        Args:
            r1, c1: 第一個格子的位置
            r2, c2: 第二個格子的位置
        
        Returns:
            bool: 如果兩格在同一 row、col 或 box 中則返回 True
        """
        # 同一行
        if r1 == r2:
            return True
        
        # 同一列
        if c1 == c2:
            return True
        
        # 同一 box (3x3)
        if r1 // 3 == r2 // 3 and c1 // 3 == c2 // 3:
            return True
        
        return False
    
    def apply_xy_wing(self, xy_wing_patterns):
        """
        應用 XY-Wing 模式消除候選數
        
        對於每個 XY-Wing，從同時能看到兩個 Wing 的格子中消除 Z
        
        Args:
            xy_wing_patterns: find_xy_wing() 返回的模式列表
        
        Returns:
            int: 消除的候選數數量
        """
        eliminated = 0
        
        for pattern in xy_wing_patterns:
            _, pivot, wing1, wing2, Z = pattern
            pivot_row, pivot_col = pivot
            wing1_row, wing1_col = wing1
            wing2_row, wing2_col = wing2
            
            # 檢查所有空格
            for row in range(9):
                for col in range(9):
                    # 跳過 Pivot 和兩個 Wing
                    if (row, col) in [pivot, wing1, wing2]:
                        continue
                    
                    # 跳過沒有候選數的格子
                    if (row, col) not in self.candidates:
                        continue
                    
                    # 如果這個格子能同時看到兩個 Wing
                    if (self._can_see(row, col, wing1_row, wing1_col) and 
                        self._can_see(row, col, wing2_row, wing2_col)):
                        
                        # 從候選數中消除 Z
                        if Z in self.candidates[(row, col)]:
                            self.candidates[(row, col)].discard(Z)
                            eliminated += 1
        
        return eliminated
