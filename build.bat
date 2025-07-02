@echo off
echo touka.exe のビルドを開始します...

REM 仮想環境の作成（オプション）
if not exist venv (
    echo 仮想環境を作成中...
    python -m venv venv
)

REM 仮想環境の有効化
call venv\Scripts\activate.bat

REM 依存関係のインストール
echo 依存関係をインストール中...
pip install -r requirements.txt

REM PyInstallerでビルド
echo EXEファイルをビルド中...
pyinstaller --onefile --console --name touka --clean --noconfirm touka.py

echo.
echo ビルド完了！
echo 実行ファイル: dist\touka.exe
echo.
echo 使い方: touka.exe #FFFFFF
pause