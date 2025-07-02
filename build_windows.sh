#!/bin/bash

echo "Windows用EXEのクロスビルドを開始します..."

# 仮想環境を有効化
source venv/bin/activate

# Windows用のPyInstallerでビルド
# --target-architecture=x86_64-w64 オプションを使用
python -m PyInstaller \
    --onefile \
    --console \
    --name touka \
    --clean \
    --noconfirm \
    --distpath dist_windows \
    --workpath build_windows \
    --specpath . \
    touka.py

echo "ビルド完了！"
echo "出力先: dist_windows/touka.exe"