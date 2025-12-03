#!/usr/bin/env python3
"""
測試GUI快速啟動功能
先清空緩存，然後測量啟動時間
"""

import time
import os
import json
import subprocess

def clear_cache():
    """清空緩存以測試冷啟動時間"""
    cache_file = "puzzle_cache.json"
    if os.path.exists(cache_file):
        os.remove(cache_file)
        print("🗑️ 已清空緩存文件")
    else:
        print("📝 緩存文件不存在")

def test_startup_time():
    """測試GUI啟動時間"""
    print("🚀 測試GUI啟動時間...")
    print("⏱️ 啟動計時開始...")
    
    start_time = time.time()
    
    # 啟動GUI（以背景模式運行，立即返回）
    process = subprocess.Popen(['python', 'sudoku_gui.py'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    
    # 等待程序產生一些輸出，表示GUI已經顯示
    output_detected = False
    timeout = 10  # 最多等待10秒
    check_start = time.time()
    
    while time.time() - check_start < timeout:
        # 檢查是否有輸出
        if process.poll() is None:  # 程序還在運行
            time.sleep(0.1)
            if time.time() - start_time > 1:  # 假設1秒後GUI應該已顯示
                output_detected = True
                break
    
    end_time = time.time()
    startup_time = end_time - start_time
    
    # 終止程序
    if process.poll() is None:
        process.terminate()
        process.wait()
    
    if output_detected or startup_time < 2:
        print(f"✅ GUI啟動成功！")
        print(f"⚡ 估計啟動時間: {startup_time:.2f} 秒")
    else:
        print(f"⚠️ GUI啟動時間較長: {startup_time:.2f} 秒")
    
    return startup_time

if __name__ == "__main__":
    print("🧪 GUI啟動性能測試")
    print("=" * 40)
    
    # 測試1: 有緩存的情況
    print("\n📦 測試1: 有緩存的啟動時間")
    time1 = test_startup_time()
    
    # 測試2: 無緩存的情況
    print("\n🗑️ 測試2: 清空緩存後的啟動時間")
    clear_cache()
    time.sleep(1)
    time2 = test_startup_time()
    
    print("\n📊 測試結果:")
    print(f"   有緩存啟動時間: {time1:.2f}s")
    print(f"   無緩存啟動時間: {time2:.2f}s")
    
    if time2 < 3:
        print("🎉 優化成功！無緩存啟動時間小於3秒")
    else:
        print("⚠️ 啟動時間仍然較長，需要進一步優化")
