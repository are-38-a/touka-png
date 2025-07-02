#!/usr/bin/env python3
import os
import sys
import subprocess

def main():
    print("touka.exe のビルドを開始します...")
    
    # PyInstallerコマンドを構築
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name", "touka",
        "--clean",
        "--noconfirm",
        "--add-data", "requirements.txt;.",  # Windowsの場合はセミコロン
        "touka.py"
    ]
    
    # Linux/MacOSの場合はコロンを使用
    if sys.platform != "win32":
        cmd[9] = "requirements.txt:."
    
    try:
        subprocess.run(cmd, check=True)
        print("\nビルド成功！")
        print("実行ファイル: dist/touka.exe (Windows) または dist/touka (Linux/Mac)")
    except subprocess.CalledProcessError as e:
        print(f"\nビルドエラー: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())