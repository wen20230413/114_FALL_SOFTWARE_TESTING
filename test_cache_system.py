# test_cache_system.py
# 測試新的緩存系統

from puzzle_cache import PuzzleCache
from difficulty_engine import DifficultyEngine
import time

def test_cache_system():
    """測試緩存系統的功能"""
    print("🧪 Testing Puzzle Cache System")
    print("=" * 50)
    
    # 初始化
    cache = PuzzleCache()
    engine = DifficultyEngine()
    
    # 顯示初始狀態
    print("\n📊 Initial cache status:")
    status = cache.get_cache_status()
    for difficulty, info in status.items():
        print(f"  {difficulty}: {info['current']}/{info['target']}")
    
    # 測試獲取不同難度的題目
    difficulties = ["Easy", "Medium", "Hard"]
    
    for difficulty in difficulties:
        print(f"\n🎯 Testing {difficulty} puzzle retrieval...")
        
        start_time = time.time()
        puzzle_data = cache.get_puzzle(difficulty)
        end_time = time.time()
        
        if puzzle_data:
            puzzle, solution = puzzle_data
            # 驗證難度
            rated_difficulty, score, techniques = engine.rate_puzzle(puzzle)
            
            print(f"  ✅ Retrieved {difficulty} puzzle in {end_time - start_time:.3f}s")
            print(f"  📈 Actual difficulty: {rated_difficulty} (score: {score})")
            
            # 計算空格數
            empty_count = sum(row.count(0) for row in puzzle.grid)
            print(f"  🔢 Empty cells: {empty_count}")
            
        else:
            print(f"  ❌ No {difficulty} puzzle available in cache")
    
    # 最終緩存狀態
    print(f"\n📊 Final cache status:")
    status = cache.get_cache_status()
    for difficulty, info in status.items():
        print(f"  {difficulty}: {info['current']}/{info['target']}")
    
    print("\n✅ Cache system test completed!")

if __name__ == "__main__":
    test_cache_system()
