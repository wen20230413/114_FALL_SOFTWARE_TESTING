#!/usr/bin/env python3
"""
測試撤銷/重做功能
"""

print("🔄 撤銷/重做功能測試指南")
print("=" * 50)
print("GUI啟動後，請按以下步驟測試：")
print()
print("📝 基本操作測試：")
print("1. 點擊任意空白格子")
print("2. 按數字鍵 1-9 輸入數字")
print("3. 點擊 '↶ Undo' 按鈕或按 Ctrl+Z")
print("   → 應該撤銷剛才的輸入")
print("4. 點擊 '↷ Redo' 按鈕或按 Ctrl+Y") 
print("   → 應該重做剛才撤銷的操作")
print()
print("🔍 進階測試：")
print("5. 連續輸入多個數字")
print("6. 連續按多次 Ctrl+Z 撤銷")
print("7. 按 Ctrl+Y 重做部分操作")
print("8. 再輸入新數字（應該清空重做堆疊）")
print("9. 生成新題目（應該清空所有歷史）")
print()
print("✅ 預期行為：")
print("- 按鈕在無操作時應該是禁用的")
print("- 快捷鍵 Ctrl+Z / Ctrl+Y 應該正常工作")
print("- 每次操作後按鈕狀態應該正確更新")
print("- 新題目生成後歷史應該清空")
print()

# 使用現有的緩存文件啟動GUI
import os
if os.path.exists("puzzle_cache.json"):
    print("🚀 啟動GUI進行測試...")
    os.system("python sudoku_gui.py")
else:
    print("❌ 沒有找到緩存文件，請先運行一次完整的GUI")
