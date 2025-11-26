# fix_unicode.py
# 修復 Unicode 字符問題

import sys
import re

def fix_unicode_in_file(filename):
    """修復文件中的 Unicode 字符"""
    try:
        # 嘗試不同的編碼
        encodings = ['utf-8', 'cp950', 'gbk', 'latin1']
        content = None
        
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"Successfully read {filename} with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"Could not read {filename} with any encoding")
            return False
        
        # 替換 Unicode 字符
        content = content.replace('✓', '[PASS]')
        content = content.replace('✅', '[SUCCESS]')
        content = content.replace('❌', '[FAIL]')
        content = content.replace('🎉', '[CELEBRATE]')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed Unicode characters in {filename}")
        return True
        
    except Exception as e:
        print(f"Error fixing {filename}: {e}")
        return False

def main():
    files_to_fix = [
        'test_difficulty_engine.py',
        'test_techniques.py',
        'run_all_tests.py'
    ]
    
    success_count = 0
    for filename in files_to_fix:
        if fix_unicode_in_file(filename):
            success_count += 1
    
    print(f"\nFixed {success_count}/{len(files_to_fix)} files")
    return success_count == len(files_to_fix)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
