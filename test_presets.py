#!/usr/bin/env python3
"""
測試預設題目系統的性能
"""

import time
import os

def test_puzzle_availability():
    """測試各難度題目的可用性"""
    print("🧪 測試預設題目系統...")
    
    from puzzle_cache import PuzzleCache
    
    cache = PuzzleCache()
    
    difficulties = ["Easy", "Medium", "Hard"]
    
    for difficulty in difficulties:
        start_time = time.time()
        
        puzzle = cache.get_puzzle(difficulty)
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # 轉換為毫秒
        
        if puzzle:
            print(f"✅ {difficulty}: 可用 ({response_time:.1f}ms)")
        else:
            print(f"❌ {difficulty}: 不可用 ({response_time:.1f}ms)")
    
    print(f"\n📋 預設題目統計:")
    from preset_puzzles import get_preset_count
    for difficulty in difficulties:
        count = get_preset_count(difficulty)
        print(f"  {difficulty}: {count} 個預設題目")

def test_startup_with_presets():
    """測試帶預設題目的GUI啟動速度"""
    print("\n🚀 測試GUI啟動（帶預設題目）...")
    
    # 清空緩存以測試純預設題目性能
    cache_file = "puzzle_cache.json"
    if os.path.exists(cache_file):
        os.rename(cache_file, f"{cache_file}.temp")
        print("🗑️ 暫時移除緩存，純測試預設題目")
    
    print("💡 現在啟動GUI應該非常快，因為使用預設題目...")
    print("   - Easy, Medium, Hard 題目都應該立即可用")
    print("   - 不需要等待任何生成過程")
    print("   - 啟動時間應該在1-2秒內")
    
    input("\n按Enter啟動GUI測試...")
    
    start_time = time.time()
    os.system("python sudoku_gui.py")
    
    # 恢復緩存文件
    if os.path.exists(f"{cache_file}.temp"):
        os.rename(f"{cache_file}.temp", cache_file)
        print("📦 已恢復緩存文件")

if __name__ == "__main__":
    print("🎯 預設題目系統測試")
    print("=" * 40)
    
    test_puzzle_availability()
    test_startup_with_presets()
