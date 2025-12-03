#!/usr/bin/env python3
"""
簡單測試GUI啟動速度
"""

import time
import os

# 清空緩存以模擬最壞情況
cache_file = "puzzle_cache.json"
if os.path.exists(cache_file):
    backup_name = f"{cache_file}.backup"
    os.rename(cache_file, backup_name)
    print(f"📦 緩存已備份為 {backup_name}")
else:
    print("📝 沒有現有緩存")

print("\n🚀 現在啟動GUI測試快速啟動...")
print("⏱️ 觀察GUI視窗顯示的時間")
print("💡 預期：GUI視窗應該在1-2秒內出現，題目應該立即生成")

# 啟動GUI
os.system("python sudoku_gui.py")
