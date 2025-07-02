# touka-png

指定した色を透過にしてPNG画像をトリミングするツール

## 機能

- 指定色を透過色に変換
- 透過部分を除外して自動トリミング
- ディレクトリ内の全PNGファイルを一括処理
- 処理後のファイルは `-touka` サフィックス付きで保存

## 使い方

### Pythonで実行
```bash
python touka.py #FFFFFF
```

### 実行ファイルで実行
```bash
# Windows
touka.exe #FFFFFF

# Linux/macOS
./touka #FFFFFF
```

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

## 依存関係

- Pillow 10.2.0
- numpy 1.26.4
- pyinstaller 6.3.0（ビルド時のみ）