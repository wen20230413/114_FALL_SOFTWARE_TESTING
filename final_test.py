#!/usr/bin/env python3
"""
簡單的GUI啟動測試，專門測試預設題目的效果
"""

import os
import time

# 清空緩存來純測試預設題目
cache_file = "puzzle_cache.json"
if os.path.exists(cache_file):
    os.rename(cache_file, f"{cache_file}.backup")
    print("🗑️ 已移除緩存，純使用預設題目")

print("\n🚀 啟動GUI測試 - 純預設題目模式")
print("📋 系統應該使用預設題目，無需等待生成")
print("⚡ 預期啟動時間：1-3秒")
print("💡 觀察輸出中的 '📋 Using preset ... puzzle...' 訊息")
print("\n" + "="*50)

start_time = time.time()
os.system("python sudoku_gui.py")

# 恢復緩存
if os.path.exists(f"{cache_file}.backup"):
    os.rename(f"{cache_file}.backup", cache_file)
    print("📦 已恢復緩存文件")
