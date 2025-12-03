#!/usr/bin/env python3
"""
測試進度條功能
先清空緩存，然後啟動GUI觀察進度條
"""

import os
import json

def clear_cache():
    """清空緩存文件以測試進度條"""
    cache_file = "puzzle_cache.json"
    if os.path.exists(cache_file):
        # 創建一個幾乎空的緩存
        empty_cache = {
            "Easy": [],
            "Medium": [],
            "Hard": []
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(empty_cache, f, indent=2, ensure_ascii=False)
        
        print("✅ 緩存已清空，準備測試進度條")
    else:
        print("📝 緩存文件不存在，將建立新的緩存")

if __name__ == "__main__":
    print("🧪 進度條測試準備")
    clear_cache()
    print("請啟動 GUI 來觀察進度條: python sudoku_gui.py")
    print("或直接運行以下命令:")
    print("python sudoku_gui.py")
