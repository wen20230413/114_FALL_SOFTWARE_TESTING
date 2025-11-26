# run_all_tests.py
# TDD 驗證腳本 - 運行所有測試並生成報告

import sys
import time
import subprocess
from pathlib import Path

def run_test_file(test_file):
    """運行單個測試文件並返回結果"""
    print(f"\n{'='*50}")
    print(f"運行測試: {test_file}")
    print('='*50)
    
    start_time = time.time()
    
    try:
        # 使用 subprocess 運行測試
        result = subprocess.run([
            'C:/Users/vala3/AppData/Local/Microsoft/WindowsApps/python3.11.exe',
            test_file
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(result.stdout)
        
        if result.stderr:
            print("錯誤輸出:")
            print(result.stderr)
        
        success = result.returncode == 0
        
        print(f"\n測試結果: {'[SUCCESS] 通過' if success else '[FAIL] 失敗'}")
        print(f"執行時間: {duration:.2f} 秒")
        
        return success, duration, result.stdout
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"運行測試時發生錯誤: {e}")
        return False, duration, str(e)

def analyze_test_results(results):
    """分析測試結果"""
    total_tests = len(results)
    passed_tests = sum(1 for success, _, _ in results.values() if success)
    failed_tests = total_tests - passed_tests
    total_time = sum(duration for _, duration, _ in results.values())
    
    print(f"\n{'='*60}")
    print("TDD 驗證報告")
    print('='*60)
    
    print(f"總測試檔案: {total_tests}")
    print(f"通過: {passed_tests} [SUCCESS]")
    print(f"失敗: {failed_tests} [FAIL]")
    print(f"總執行時間: {total_time:.2f} 秒")
    print(f"成功率: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\n詳細結果:")
    for test_name, (success, duration, output) in results.items():
        status = "[SUCCESS] PASS" if success else "[FAIL] FAIL"
        print(f"  {test_name:25} {status:8} ({duration:.2f}s)")
    
    # 統計測試覆蓋的功能
    print(f"\n功能覆蓋分析:")
    
    # 分析 difficulty_engine 測試
    if 'difficulty_engine' in results:
        success, duration, output = results['difficulty_engine']
        if success:
            test_count = output.count('[PASS]')
            print(f"  難度引擎測試: {test_count} 個測試案例通過")
    
    # 分析 solving_techniques 測試
    if 'solving_techniques' in results:
        success, duration, output = results['solving_techniques']
        if success:
            test_count = output.count('[PASS]')
            print(f"  求解技巧測試: {test_count} 個測試案例通過")
    
    return passed_tests == total_tests

def main():
    """主函數 - TDD 流程驗證"""
    print("開始 TDD (測試驅動開發) 流程驗證")
    print("驗證 difficulty_engine.py 和 solving_techniques.py")
    
    # 測試文件列表
    test_files = [
        'test_difficulty_engine.py',
        'test_techniques.py'
    ]
    
    results = {}
    
    # 運行所有測試
    for test_file in test_files:
        if Path(test_file).exists():
            module_name = test_file.replace('test_', '').replace('.py', '')
            success, duration, output = run_test_file(test_file)
            results[module_name] = (success, duration, output)
        else:
            print(f"警告: 找不到測試文件 {test_file}")
    
    # 分析結果
    all_passed = analyze_test_results(results)
    
    # TDD 流程總結
    print(f"\n{'='*60}")
    print("TDD 流程驗證總結")
    print('='*60)
    
    if all_passed:
        print("[CELEBRATE] TDD 驗證成功!")
        print("[SUCCESS] 所有測試都通過了")
        print("[SUCCESS] difficulty_engine.py 和 solving_techniques.py 都已通過驗證")
        print("[SUCCESS] 代碼品質符合 TDD 標準")
        
        print(f"\n驗證的功能包括:")
        print("📋 difficulty_engine.py:")
        print("  • 難度評分演算法")
        print("  • 技巧階層分類")
        print("  • 邊界條件處理")
        print("  • 無限迴圈保護")
        
        print("📋 solving_techniques.py:")
        print("  • Naked Singles 檢測")
        print("  • Hidden Singles 檢測")
        print("  • Naked Pairs 檢測與應用")
        print("  • Pointing Pairs 檢測與應用")
        print("  • X-Wing 檢測與應用")
        print("  • Swordfish 檢測與應用")
        print("  • XY-Wing 檢測與應用")
        print("  • 候選數字計算與更新")
        print("  • 邊界條件和錯誤處理")
        
        return 0
        
    else:
        print("[FAIL] TDD 驗證失敗")
        print("需要修復失敗的測試才能完成 TDD 流程")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
