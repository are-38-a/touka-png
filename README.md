# touka-png

指定した色を透過にして画像をトリミングするツール

## 機能

- 指定色を透過色に変換
- 色域の許容誤差設定（類似色も透過可能）
- 透過部分を除外して自動トリミング
- 全画像形式対応（PNG, JPG, GIF, BMP, TIFF, WebP）
- ディレクトリ内の全画像ファイルを一括処理
- 処理後のファイルは `-touka` サフィックス付きのPNGで保存

## 使い方

### 対話式モード（推奨）
```bash
# Windows
touka.exe

# Linux/macOS
./touka

# Python
python touka.py
```

起動後、以下を入力:
1. 透過にする色のカラーコード（例: FFFFFF, FFF, 000000）
2. 色域の許容誤差（0-255、デフォルト: 0）
   - 0: 完全一致のみ
   - 10: わずかな差を許容
   - 30: 大きな差を許容

### コマンドライン引数モード
```bash
# Windows
touka.exe #FFFFFF

# Linux/macOS
./touka #FFFFFF

# Python
python touka.py #FFFFFF
```
※この場合、許容誤差は0（完全一致）になります

## インストール

### リリースページから実行ファイルをダウンロード

[Releases](https://github.com/are-38-a/touka-png/releases) から各OS用の実行ファイルをダウンロードできます。

- Windows: `touka-windows.exe`
- Linux: `touka-linux`
- macOS: `touka-macos`

## ビルド方法

### ローカルビルド

#### Windows
```bash
build.bat
```

#### Linux/Mac
```bash
pip install -r requirements.txt
python build.py
```

### GitHub Actions

プッシュまたはタグ作成時に自動的にビルドされます。
タグ（例: `v1.0.0`）を作成すると、自動的にリリースが作成されます。

```bash
git tag v1.0.0
git push origin v1.0.0
```

## 対応画像形式

- PNG
- JPG / JPEG
- GIF
- BMP
- TIFF / TIF
- WebP

## 依存関係

- Pillow 10.2.0
- numpy 1.26.4
- pyinstaller 6.3.0（ビルド時のみ）

## 更新履歴

### v1.1.0
- 全画像形式対応（JPG, GIF, BMP, TIFF, WebP）
- 色域許容誤差機能を追加
- 対話式入力モードの改善

### v1.0.0
- 初回リリース
- PNG画像の透過処理
- 自動トリミング機能