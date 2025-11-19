# test_techniques.py
# Tests for solving techniques detector

from SUDOKU import SudokuBoard
from solving_techniques import SudokuTechniques

def test_calculate_candidates():
    """測試候選數字計算是否正確"""
    # 使用一個簡單的測試題目
    puzzle = [
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
    
    board = SudokuBoard(puzzle)
    tech = SudokuTechniques(board)
    
    # 驗證候選數字系統已初始化
    assert len(tech.candidates) > 0, "Should have candidates for empty cells"
    
    # 檢查 (0, 2) 位置的候選數字
    assert (0, 2) in tech.candidates, "Position (0, 2) should have candidates"
    
    # 這個位置的候選數字應該是 {2, 4}（根據數獨規則排除其他數字）
    candidates_0_2 = tech.candidates[(0, 2)]
    assert 4 in candidates_0_2, "4 should be a candidate for (0, 2)"
    
    # 驗證不可能的數字不在候選列表中
    assert 5 not in candidates_0_2, "5 should not be a candidate (in same row)"
    assert 8 not in candidates_0_2, "8 should not be a candidate (in same column)"
    assert 9 not in candidates_0_2, "9 should not be a candidate (in same box)"
    
    print("✓ Candidate calculation test passed")


def test_naked_singles_detection():
    """測試 Naked Singles 檢測"""
    # 使用一個有明顯 Naked Single 的題目
    puzzle = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 0],  # (6, 8) 只能填 4
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]
    
    board = SudokuBoard(puzzle)
    tech = SudokuTechniques(board)
    
    naked_singles = tech.find_naked_singles()
    
    # 應該找到 (6, 8) 位置的 Naked Single
    assert len(naked_singles) > 0, "Should find at least one naked single"
    assert (6, 8, 4) in naked_singles, "Should find (6, 8) = 4 as naked single"
    
    print(f"✓ Found {len(naked_singles)} naked single(s): {naked_singles}")


def test_hidden_singles_detection():
    """測試 Hidden Singles 檢測"""
    # 使用一個需要 Hidden Single 技巧的題目
    puzzle = [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ]
    
    board = SudokuBoard(puzzle)
    tech = SudokuTechniques(board)
    
    hidden_singles = tech.find_hidden_singles()
    
    # 應該能找到 Hidden Singles
    assert len(hidden_singles) > 0, "Should find at least one hidden single"
    
    print(f"✓ Found {len(hidden_singles)} hidden single(s)")
    for row, col, num in hidden_singles[:5]:  # 顯示前 5 個
        print(f"  Position ({row}, {col}) = {num}")


def test_candidate_update():
    """測試候選數字更新機制"""
    puzzle = [
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
    
    board = SudokuBoard(puzzle)
    tech = SudokuTechniques(board)
    
    # 記錄初始候選數字數量
    initial_count = len(tech.candidates)
    
    # 假設我們在 (0, 2) 填入 4
    tech.update_candidates(0, 2, 4)
    
    # 候選數字應該減少（該格子不再有候選數字）
    assert len(tech.candidates) < initial_count, "Candidates should decrease after filling a cell"
    
    # (0, 2) 應該不在候選列表中
    assert (0, 2) not in tech.candidates, "Filled cell should not have candidates"
    
    print("✓ Candidate update test passed")


def test_easy_puzzle_with_singles_only():
    """測試只需要 Singles 技巧就能解決的簡單題目"""
    # 這個題目應該只需要 Naked Singles 和 Hidden Singles
    puzzle = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 0],
        [2, 8, 7, 4, 1, 9, 6, 0, 5],
        [3, 4, 5, 2, 8, 6, 0, 7, 9]
    ]
    
    board = SudokuBoard(puzzle)
    tech = SudokuTechniques(board)
    
    # 應該能找到 Naked Singles
    singles = tech.find_naked_singles()
    assert len(singles) == 3, f"Should find 3 naked singles, found {len(singles)}"
    
    print("✓ Easy puzzle test passed")


def test_naked_pairs_detection():
    """測試 Naked Pairs 檢測"""
    # 創建一個有 Naked Pairs 的情況
    # 這需要一個特定的候選數字配置
    puzzle = [
        [0, 0, 3, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 8, 0, 0, 3, 6],
        [0, 0, 8, 0, 0, 0, 1, 0, 0],
        [0, 4, 0, 0, 6, 0, 0, 7, 3],
        [0, 0, 0, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 5],
        [0, 0, 4, 0, 7, 0, 0, 6, 8],
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 6, 0, 0, 5, 0, 0]
    ]
    
    board = SudokuBoard(puzzle)
    tech = SudokuTechniques(board)
    
    naked_pairs = tech.find_naked_pairs()
    
    # 檢查是否找到了 Naked Pairs
    print(f"✓ Found {len(naked_pairs)} naked pair(s)")
    if naked_pairs:
        for pair in naked_pairs[:3]:  # 顯示前 3 個
            _, unit_type, unit_idx, cells, nums = pair
            print(f"  {unit_type} {unit_idx}: cells {cells}, nums {nums}")


def test_pointing_pairs_detection():
    """測試 Pointing Pairs 檢測"""
    # 創建一個有 Pointing Pairs 的情況
    puzzle = [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ]
    
    board = SudokuBoard(puzzle)
    tech = SudokuTechniques(board)
    
    pointing_pairs = tech.find_pointing_pairs()
    
    # 檢查是否找到了 Pointing Pairs
    print(f"✓ Found {len(pointing_pairs)} pointing pair(s)")
    if pointing_pairs:
        for pointing in pointing_pairs[:3]:  # 顯示前 3 個
            _, box_idx, num, line_type, line_idx, positions = pointing
            print(f"  Box {box_idx}: num {num} in {line_type} {line_idx}")


def test_pairs_elimination():
    """測試 Pairs 消除候選數字的功能"""
    puzzle = [
        [0, 0, 3, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 8, 0, 0, 3, 6],
        [0, 0, 8, 0, 0, 0, 1, 0, 0],
        [0, 4, 0, 0, 6, 0, 0, 7, 3],
        [0, 0, 0, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 5],
        [0, 0, 4, 0, 7, 0, 0, 6, 8],
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 6, 0, 0, 5, 0, 0]
    ]
    
    board = SudokuBoard(puzzle)
    tech = SudokuTechniques(board)
    
    # 記錄初始候選數字總數
    initial_total = sum(len(cands) for cands in tech.candidates.values())
    
    # 應用 Naked Pairs
    naked_pairs = tech.find_naked_pairs()
    if naked_pairs:
        eliminated = tech.apply_naked_pairs(naked_pairs)
        print(f"✓ Naked Pairs eliminated {eliminated} candidates")
    
    # 應用 Pointing Pairs
    pointing_pairs = tech.find_pointing_pairs()
    if pointing_pairs:
        eliminated = tech.apply_pointing_pairs(pointing_pairs)
        print(f"✓ Pointing Pairs eliminated {eliminated} candidates")
    
    # 候選數字應該減少（如果找到了 pairs）
    final_total = sum(len(cands) for cands in tech.candidates.values())
    if naked_pairs or pointing_pairs:
        assert final_total < initial_total, "Candidates should decrease after applying pairs"
    
    print("✓ Pairs elimination test passed")


def test_x_wing_detection():
    """測試 X-Wing 檢測"""
    # 創建一個可能有 X-Wing 的題目
    puzzle = [
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
    
    # 使用一個部分填充的題目
    puzzle2 = [
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
    
    board = SudokuBoard(puzzle2)
    tech = SudokuTechniques(board)
    
    x_wings = tech.find_x_wing()
    
    # X-Wing 比較罕見，可能找不到
    print(f"✓ Found {len(x_wings)} X-Wing(s)")
    if x_wings:
        for x_wing in x_wings[:2]:  # 顯示前 2 個
            _, pattern_type, lines, cross_lines, num = x_wing
            print(f"  {pattern_type}: lines {lines}, cross {cross_lines}, num {num}")


def test_x_wing_elimination():
    """測試 X-Wing 消除候選數字的功能"""
    # 使用標準題目測試
    puzzle = [
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
    
    board = SudokuBoard(puzzle)
    tech = SudokuTechniques(board)
    
    # 記錄初始候選數字總數
    initial_total = sum(len(cands) for cands in tech.candidates.values())
    
    # 查找並應用 X-Wing
    x_wings = tech.find_x_wing()
    if x_wings:
        eliminated = tech.apply_x_wing(x_wings)
        print(f"✓ X-Wing eliminated {eliminated} candidates")
        
        # 候選數字應該減少
        final_total = sum(len(cands) for cands in tech.candidates.values())
        assert final_total <= initial_total, "Candidates should not increase"
    else:
        print("✓ No X-Wing found (this is normal for easy puzzles)")
    
    print("✓ X-Wing elimination test passed")


if __name__ == "__main__":
    print("Running technique detection tests...\n")
    
    test_calculate_candidates()
    test_naked_singles_detection()
    test_hidden_singles_detection()
    test_candidate_update()
    test_easy_puzzle_with_singles_only()
    test_naked_pairs_detection()
    test_pointing_pairs_detection()
    test_pairs_elimination()
    test_x_wing_detection()
    test_x_wing_elimination()
    test_swordfish_detection()
    test_swordfish_elimination()
    test_xy_wing_detection()
    test_xy_wing_elimination()
    
    print("\n✅ All tests passed!")


def test_xy_wing_detection():
    """測試 XY-Wing 檢測 (樞紐模式)"""
    # 創建一個包含 XY-Wing 模式的題目
    # 這需要精心設計：三個雙候選格形成樞紐模式
    puzzle = [
        [0, 0, 3, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 8, 0, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 0, 0, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 8, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 3, 0, 0]
    ]
    
    board = SudokuBoard(puzzle)
    tech = SudokuTechniques(board)
    
    # 檢測 XY-Wing
    xy_wings = tech.find_xy_wing()
    
    # 應該返回一個列表
    assert isinstance(xy_wings, list), "Should return a list"
    
    # 驗證返回格式
    if len(xy_wings) > 0:
        pattern = xy_wings[0]
        assert len(pattern) == 5, "Each pattern should have 5 elements"
        assert pattern[0] == 'xy_wing', "First element should be 'xy_wing'"
        
        # 驗證三個位置都是 tuple
        pivot, wing1, wing2, digit = pattern[1], pattern[2], pattern[3], pattern[4]
        assert isinstance(pivot, tuple) and len(pivot) == 2, "Pivot should be (row, col)"
        assert isinstance(wing1, tuple) and len(wing1) == 2, "Wing1 should be (row, col)"
        assert isinstance(wing2, tuple) and len(wing2) == 2, "Wing2 should be (row, col)"
        assert isinstance(digit, int) and 1 <= digit <= 9, "Should have a valid digit"
        
        print(f"✓ Found {len(xy_wings)} XY-Wing pattern(s)")
    else:
        print("✓ XY-Wing detection works (no pattern found in this puzzle)")


def test_xy_wing_elimination():
    """測試 XY-Wing 消除候選數"""
    # 使用一個簡化的測試場景
    puzzle = [
        [0, 0, 3, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 8, 0, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 0, 0, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 8, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 3, 0, 0]
    ]
    
    board = SudokuBoard(puzzle)
    tech = SudokuTechniques(board)
    
    # 找出 XY-Wing
    xy_wings = tech.find_xy_wing()
    
    if len(xy_wings) > 0:
        # 記錄消除前的候選數總數
        before_count = sum(len(cands) for cands in tech.candidates.values())
        
        # 應用 XY-Wing
        eliminated = tech.apply_xy_wing(xy_wings)
        
        # 記錄消除後的候選數總數
        after_count = sum(len(cands) for cands in tech.candidates.values())
        
        # 驗證消除數量一致
        assert before_count - after_count == eliminated, "Eliminated count should match"
        
        print(f"✓ XY-Wing elimination test passed (eliminated {eliminated} candidates)")
    else:
        # 即使沒找到 XY-Wing，apply 方法也應該正常工作
        eliminated = tech.apply_xy_wing([])
        assert eliminated == 0, "Should eliminate 0 candidates when no pattern found"
        print("✓ XY-Wing elimination test passed (no pattern to apply)")


def test_swordfish_detection():
    """測試 Swordfish 檢測 (3x3 X-Wing 模式)"""
    # 創建一個包含 Swordfish 模式的題目
    # 這是一個精心設計的測試案例，數字 2 在三行中只出現在相同的三列
    puzzle = [
        [0, 0, 3, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 8, 0, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 0, 0, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 8, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 3, 0, 0]
    ]
    
    board = SudokuBoard(puzzle)
    tech = SudokuTechniques(board)
    
    # 檢測 Swordfish
    swordfish = tech.find_swordfish()
    
    # 應該能找到至少一個 Swordfish 模式
    # 注意：實際能否找到取決於題目設計，這裡主要測試方法能正常執行
    assert isinstance(swordfish, list), "Should return a list"
    
    # 驗證返回格式
    if len(swordfish) > 0:
        pattern = swordfish[0]
        assert len(pattern) == 5, "Each pattern should have 5 elements"
        assert pattern[0] == 'swordfish', "First element should be 'swordfish'"
        assert pattern[1] in ['rows', 'cols'], "Pattern type should be 'rows' or 'cols'"
        assert len(pattern[2]) == 3, "Should have 3 lines"
        assert len(pattern[3]) == 3, "Should have 3 cross lines"
        assert isinstance(pattern[4], int) and 1 <= pattern[4] <= 9, "Should have a valid digit"
        print(f"✓ Found {len(swordfish)} Swordfish pattern(s)")
    else:
        print("✓ Swordfish detection works (no pattern found in this puzzle)")


def test_swordfish_elimination():
    """測試 Swordfish 消除候選數"""
    # 使用一個簡化的測試場景
    # 手動構造一個確定有 Swordfish 的情況
    puzzle = [
        [0, 0, 3, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 8, 0, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 0, 0, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 8, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 3, 0, 0]
    ]
    
    board = SudokuBoard(puzzle)
    tech = SudokuTechniques(board)
    
    # 找出 Swordfish
    swordfish = tech.find_swordfish()
    
    if len(swordfish) > 0:
        # 記錄消除前的候選數總數
        before_count = sum(len(cands) for cands in tech.candidates.values())
        
        # 應用 Swordfish
        eliminated = tech.apply_swordfish(swordfish)
        
        # 記錄消除後的候選數總數
        after_count = sum(len(cands) for cands in tech.candidates.values())
        
        # 驗證消除數量一致
        assert before_count - after_count == eliminated, "Eliminated count should match"
        
        print(f"✓ Swordfish elimination test passed (eliminated {eliminated} candidates)")
    else:
        # 即使沒找到 Swordfish，apply 方法也應該正常工作
        eliminated = tech.apply_swordfish([])
        assert eliminated == 0, "Should eliminate 0 candidates when no pattern found"
        print("✓ Swordfish elimination test passed (no pattern to apply)")
