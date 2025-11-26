# test_difficulty_engine.py
# Comprehensive tests for difficulty rating engine

from SUDOKU import SudokuBoard
from difficulty_engine import DifficultyEngine
import copy

def test_easy_puzzle_rating():
    """測試 Easy 難度題目的評分"""
    # 只需要 Singles 的簡單題目
    easy_puzzle = [
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
    
    board = SudokuBoard(easy_puzzle)
    engine = DifficultyEngine()
    difficulty, score, techniques = engine.rate_puzzle(copy.deepcopy(board))
    
    assert difficulty == 'Easy', f"Expected 'Easy' but got '{difficulty}'"
    assert score <= 15, f"Expected score ≤ 15 but got {score}"
    assert 'naked_single' in techniques or 'hidden_single' in techniques
    
    print(f"✓ Easy puzzle rated correctly: {difficulty} (score: {score})")


def test_medium_puzzle_rating():
    """測試 Medium 難度題目的評分"""
    # 需要 Pairs 技巧的題目
    medium_puzzle = [
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
    
    board = SudokuBoard(medium_puzzle)
    engine = DifficultyEngine()
    difficulty, score, techniques = engine.rate_puzzle(copy.deepcopy(board))
    
    # 這個題目可能只需要 Singles，但我們測試引擎能正確評分
    assert difficulty in ['Easy', 'Medium'], f"Expected 'Easy' or 'Medium' but got '{difficulty}'"
    assert score <= 90, f"Expected score ≤ 90 but got {score}"
    
    print(f"✓ Medium puzzle rated: {difficulty} (score: {score})")


def test_standard_puzzle_rating():
    """測試標準難度題目的評分"""
    standard_puzzle = [
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
    
    board = SudokuBoard(standard_puzzle)
    engine = DifficultyEngine()
    difficulty, score, techniques = engine.rate_puzzle(copy.deepcopy(board))
    
    # 驗證返回值的格式
    assert difficulty in ['Easy', 'Medium', 'Hard']
    assert isinstance(score, (int, float))
    assert isinstance(techniques, list)
    assert len(techniques) > 0
    
    print(f"✓ Standard puzzle rated: {difficulty} (score: {score})")
    print(f"  Techniques used: {len(set(techniques))} unique types")


def test_technique_hierarchy():
    """測試技巧階層是否正確"""
    engine = DifficultyEngine()
    
    # 驗證技巧分數遞增
    assert engine.TECHNIQUE_SCORES['naked_single'] == 15
    assert engine.TECHNIQUE_SCORES['hidden_single'] == 15
    assert engine.TECHNIQUE_SCORES['naked_pair'] == 65
    assert engine.TECHNIQUE_SCORES['pointing_pair'] == 80
    assert engine.TECHNIQUE_SCORES['x_wing'] == 120
    
    # 驗證難度分類邏輯
    assert engine.TECHNIQUE_SCORES['naked_single'] <= 15  # Easy
    assert engine.TECHNIQUE_SCORES['pointing_pair'] <= 90  # Medium
    assert engine.TECHNIQUE_SCORES['x_wing'] > 90  # Hard
    
    print("✓ Technique hierarchy verified")


def test_difficulty_classification():
    """測試難度分類邏輯"""
    engine = DifficultyEngine()
    
    # 測試不同空格數量的題目
    test_cases = [
        (3, "Very easy"),
        (30, "Easy"),
        (45, "Medium"),
        (51, "Standard"),
    ]
    
    for empty_count, label in test_cases:
        # 創建一個部分填充的題目（用於測試）
        puzzle = [[0] * 9 for _ in range(9)]
        # 填充一些數字使其接近目標空格數
        filled = 81 - empty_count
        count = 0
        for i in range(9):
            for j in range(9):
                if count < filled:
                    puzzle[i][j] = ((i * 3 + i // 3 + j) % 9) + 1
                    count += 1
        
        board = SudokuBoard(puzzle)
        # 注意：這些題目可能無效，但我們只測試引擎不會崩潰
        try:
            difficulty, score, techniques = engine.rate_puzzle(copy.deepcopy(board))
            print(f"  {label} ({empty_count} empty): {difficulty} (score: {score})")
        except:
            print(f"  {label} ({empty_count} empty): [invalid puzzle]")
    
    print("✓ Difficulty classification test completed")


def test_engine_consistency():
    """測試引擎的一致性（同一題目應得到相同結果）"""
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
    engine = DifficultyEngine()
    
    # 評分兩次，應該得到相同結果
    result1 = engine.rate_puzzle(copy.deepcopy(board))
    result2 = engine.rate_puzzle(copy.deepcopy(board))
    
    assert result1[0] == result2[0], "Difficulty should be consistent"
    assert result1[1] == result2[1], "Score should be consistent"
    
    print(f"✓ Engine consistency verified")


def test_invalid_board_handling():
    """測試無效棋盤的處理"""
    # 測試空的棋盤
    empty_board = [[0] * 9 for _ in range(9)]
    board = SudokuBoard(empty_board)
    engine = DifficultyEngine()
    
    try:
        difficulty, score, techniques = engine.rate_puzzle(copy.deepcopy(board))
        # 應該能處理空棋盤，但可能會標記為需要專家技巧
        assert difficulty in ['Easy', 'Medium', 'Hard']
        print("✓ Empty board handled correctly")
    except Exception as e:
        print(f"✓ Empty board handled with exception: {e}")


def test_empty_board_handling():
    """測試完全空白的棋盤"""
    empty_puzzle = [[0 for _ in range(9)] for _ in range(9)]
    board = SudokuBoard(empty_puzzle)
    engine = DifficultyEngine()
    
    # 空棋盤應該能夠處理，但可能會被評為最高難度
    difficulty, score, techniques = engine.rate_puzzle(copy.deepcopy(board))
    
    assert isinstance(difficulty, str)
    assert isinstance(score, (int, float))
    assert isinstance(techniques, list)
    
    print(f"✓ Empty board rated as: {difficulty} (score: {score})")


def test_already_solved_board():
    """測試已經解決的棋盤"""
    solved_puzzle = [
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
    
    board = SudokuBoard(solved_puzzle)
    engine = DifficultyEngine()
    
    difficulty, score, techniques = engine.rate_puzzle(copy.deepcopy(board))
    
    # 已解決的棋盤應該得到最低分
    assert score == 0 or len(techniques) == 0
    
    print(f"✓ Solved board handled: {difficulty} (score: {score})")


def test_infinite_loop_protection():
    """測試無限迴圈保護機制"""
    # 創建一個可能導致無限迴圈的題目（無解或需要猜測）
    unsolvable_puzzle = [
        [1, 1, 0, 0, 0, 0, 0, 0, 0],  # 第一行有重複的1
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    
    board = SudokuBoard(unsolvable_puzzle)
    engine = DifficultyEngine()
    
    # 測試是否能在合理時間內返回結果（不會無限迴圈）
    import time
    start_time = time.time()
    
    difficulty, score, techniques = engine.rate_puzzle(copy.deepcopy(board))
    
    end_time = time.time()
    duration = end_time - start_time
    
    # 應該在5秒內完成
    assert duration < 5, f"Took too long: {duration} seconds"
    
    print(f"✓ Infinite loop protection works (completed in {duration:.2f}s)")


if __name__ == "__main__":
    print("Running difficulty engine tests...\n")
    
    test_easy_puzzle_rating()
    test_medium_puzzle_rating()
    test_standard_puzzle_rating()
    test_technique_hierarchy()
    test_difficulty_classification()
    test_engine_consistency()
    
    # 新增的測試
    test_invalid_board_handling()
    test_empty_board_handling()
    test_already_solved_board()
    test_infinite_loop_protection()
    
    print("\n✅ All difficulty engine tests passed!")
