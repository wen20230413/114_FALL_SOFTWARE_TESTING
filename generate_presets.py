#!/usr/bin/env python3
"""
生成並驗證預設題目
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from SUDOKU import generate, SudokuBoard
from difficulty_engine import DifficultyEngine

def generate_preset_puzzles():
    """生成每個難度的預設題目"""
    engine = DifficultyEngine()
    
    preset_puzzles = {
        "Easy": [],
        "Medium": [],
        "Hard": []
    }
    
    print("🔄 生成預設題目...")
    
    # 生成 Easy 題目
    print("📝 生成 Easy 題目...")
    for i in range(3):
        attempts = 0
        while len(preset_puzzles["Easy"]) <= i and attempts < 50:
            try:
                puzzle, solution = generate(35, max_attempts=10)
                difficulty, score, techniques = engine.rate_puzzle(puzzle)
                
                if difficulty == "Easy":
                    preset_puzzles["Easy"].append({
                        "puzzle": puzzle.grid,
                        "solution": solution.grid,
                        "difficulty": difficulty,
                        "score": score,
                        "techniques": techniques
                    })
                    print(f"  ✅ Easy 題目 {i+1}/3 完成 (score: {score})")
                    break
                    
            except Exception as e:
                print(f"  ⚠️ 生成失敗: {e}")
            
            attempts += 1
    
    # 生成 Medium 題目
    print("📝 生成 Medium 題目...")
    for i in range(3):
        attempts = 0
        while len(preset_puzzles["Medium"]) <= i and attempts < 50:
            try:
                puzzle, solution = generate(45, max_attempts=10)
                difficulty, score, techniques = engine.rate_puzzle(puzzle)
                
                if difficulty == "Medium":
                    preset_puzzles["Medium"].append({
                        "puzzle": puzzle.grid,
                        "solution": solution.grid,
                        "difficulty": difficulty,
                        "score": score,
                        "techniques": techniques
                    })
                    print(f"  ✅ Medium 題目 {i+1}/3 完成 (score: {score})")
                    break
                    
            except Exception as e:
                print(f"  ⚠️ 生成失敗: {e}")
            
            attempts += 1
    
    # 生成 Hard 題目
    print("📝 生成 Hard 題目...")  
    for i in range(3):
        attempts = 0
        while len(preset_puzzles["Hard"]) <= i and attempts < 30:
            try:
                puzzle, solution = generate(55, max_attempts=5)
                difficulty, score, techniques = engine.rate_puzzle(puzzle)
                
                if difficulty == "Hard":
                    preset_puzzles["Hard"].append({
                        "puzzle": puzzle.grid,
                        "solution": solution.grid,
                        "difficulty": difficulty,
                        "score": score,
                        "techniques": techniques
                    })
                    print(f"  ✅ Hard 題目 {i+1}/3 完成 (score: {score})")
                    break
                elif difficulty == "Medium" and score >= 80:  # 接受高分 Medium 作為 Hard
                    preset_puzzles["Hard"].append({
                        "puzzle": puzzle.grid,
                        "solution": solution.grid,
                        "difficulty": "Hard",  # 標記為 Hard
                        "score": score,
                        "techniques": techniques
                    })
                    print(f"  ✅ Hard 題目 {i+1}/3 完成 (高分Medium: {score})")
                    break
                    
            except Exception as e:
                print(f"  ⚠️ 生成失敗: {e}")
            
            attempts += 1
    
    return preset_puzzles

def save_preset_puzzles(preset_puzzles):
    """保存預設題目到文件"""
    content = '''#!/usr/bin/env python3
"""
預設題目庫 - 自動生成
包含每個難度級別預先準備好的題目，立即可用
"""

# 預設題目數據
PRESET_PUZZLES = ''' + str(preset_puzzles) + '''

def get_preset_puzzles():
    """返回所有預設題目"""
    return PRESET_PUZZLES

def get_random_preset_puzzle(difficulty):
    """隨機獲取指定難度的預設題目"""
    import random
    
    if difficulty in PRESET_PUZZLES and PRESET_PUZZLES[difficulty]:
        return random.choice(PRESET_PUZZLES[difficulty])
    
    return None

def get_preset_count(difficulty):
    """獲取指定難度的預設題目數量"""
    return len(PRESET_PUZZLES.get(difficulty, []))
'''
    
    with open("preset_puzzles.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("💾 預設題目已保存到 preset_puzzles.py")

if __name__ == "__main__":
    preset_puzzles = generate_preset_puzzles()
    
    print("\n📊 生成結果:")
    for difficulty, puzzles in preset_puzzles.items():
        print(f"  {difficulty}: {len(puzzles)} 個題目")
    
    if any(len(puzzles) > 0 for puzzles in preset_puzzles.values()):
        save_preset_puzzles(preset_puzzles)
        print("\n✅ 預設題目庫創建完成！")
    else:
        print("\n❌ 沒有成功生成題目")
