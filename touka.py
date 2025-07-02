#!/usr/bin/env python3
import os
import sys
import argparse
from PIL import Image
import numpy as np

def hex_to_rgb(hex_color):
    """16進数カラーコードをRGBタプルに変換"""
    # 先頭の#を削除
    hex_color = hex_color.lstrip('#')
    
    # 有効な16進数文字のみかチェック
    if not all(c in '0123456789abcdefABCDEF' for c in hex_color):
        raise ValueError(f"無効な文字が含まれています: {hex_color}")
    
    # 3文字の短縮形式（例: FFF → FFFFFF）
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    # 6文字でない場合はエラー
    if len(hex_color) != 6:
        raise ValueError(f"カラーコードは3文字または6文字である必要があります（現在: {len(hex_color)}文字）")
    
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def make_transparent_and_crop(image_path, target_color_rgb, output_path, tolerance=0):
    """指定色を透過にして画像をトリミング"""
    img = Image.open(image_path).convert('RGBA')
    data = np.array(img)
    
    # RGBチャンネルを抽出
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # 指定色のピクセルを透過に（許容誤差を考慮）
    if tolerance == 0:
        mask = (r == target_color_rgb[0]) & (g == target_color_rgb[1]) & (b == target_color_rgb[2])
    else:
        # 各チャンネルの差分を計算
        dr = np.abs(r - target_color_rgb[0])
        dg = np.abs(g - target_color_rgb[1])
        db = np.abs(b - target_color_rgb[2])
        mask = (dr <= tolerance) & (dg <= tolerance) & (db <= tolerance)
    
    data[mask] = [0, 0, 0, 0]
    
    # 新しい画像を作成
    new_img = Image.fromarray(data, 'RGBA')
    
    # 透過部分を除外してトリミング
    bbox = new_img.getbbox()
    if bbox:
        cropped_img = new_img.crop(bbox)
        cropped_img.save(output_path, 'PNG')
        return True
    else:
        # 画像が完全に透過の場合は保存しない
        print(f"警告: {image_path} は完全に透過になりました。スキップします。")
        return False

def main():
    parser = argparse.ArgumentParser(description='指定色を透過にしてPNG画像をトリミング')
    parser.add_argument('color', nargs='?', help='透過にする色のカラーコード (例: #FFFFFF または FFFFFF)')
    args = parser.parse_args()
    
    # カラーコードを取得（引数がない場合は入力を求める）
    if args.color:
        color_code = args.color
        # コマンドライン引数の場合、エラーなら終了
        try:
            target_color_rgb = hex_to_rgb(color_code)
        except ValueError as e:
            print(f"エラー: {e}")
            print(f"無効なカラーコードです: {color_code}")
            if sys.platform == "win32" or not sys.stdin.isatty():
                input("\nEnterキーを押して終了...")
            sys.exit(1)
    else:
        # 対話式モードの場合、正しい入力まで繰り返す
        while True:
            print("\n透過にする色のカラーコードを入力してください")
            print("例: FFFFFF (白), 000000 (黒), FF0000 (赤), FFF (白の短縮形)")
            color_code = input("カラーコード: ").strip()
            
            if not color_code:
                print("エラー: カラーコードが入力されていません")
                continue
            
            try:
                target_color_rgb = hex_to_rgb(color_code)
                break  # 成功したらループを抜ける
            except ValueError as e:
                print(f"\nエラー: {e}")
                print("もう一度入力してください")
    
    print(f"\n透過色: #{color_code.lstrip('#')} (RGB: {target_color_rgb})")
    
    # 許容誤差の入力
    tolerance = 0
    if not args.color:  # 対話式モードの場合のみ
        print("\n色域の許容誤差を入力してください（0-255）")
        print("0: 完全一致のみ, 10: わずかな差を許容, 30: 大きな差を許容")
        while True:
            tolerance_input = input("許容誤差 [0]: ").strip()
            if not tolerance_input:
                tolerance = 0
                break
            try:
                tolerance = int(tolerance_input)
                if 0 <= tolerance <= 255:
                    break
                else:
                    print("エラー: 0から255の範囲で入力してください")
            except ValueError:
                print("エラー: 整数を入力してください")
    
    if tolerance > 0:
        print(f"許容誤差: {tolerance}")
    
    # 現在のディレクトリ内の画像ファイルを取得
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.webp')
    image_files = [f for f in os.listdir('.') if f.lower().endswith(image_extensions) and not f.endswith('-touka.png')]
    
    if not image_files:
        print("エラー: 画像ファイルが見つかりません。")
        if sys.platform == "win32" or not sys.stdin.isatty():
            input("\nEnterキーを押して終了...")
        sys.exit(1)
    
    print(f"\n{len(image_files)}個の画像ファイルを処理します...")
    
    success_count = 0
    for image_file in image_files:
        base_name = os.path.splitext(image_file)[0]
        output_file = f"{base_name}-touka.png"
        
        try:
            if make_transparent_and_crop(image_file, target_color_rgb, output_file, tolerance):
                print(f"✓ {image_file} → {output_file}")
                success_count += 1
        except Exception as e:
            print(f"✗ {image_file} の処理中にエラーが発生しました: {e}")
    
    print(f"\n処理完了: {success_count}/{len(image_files)} ファイル")
    
    # Windows環境でウィンドウがすぐ閉じないようにする
    if sys.platform == "win32" or not sys.stdin.isatty():
        input("\nEnterキーを押して終了...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n処理が中断されました")
        if sys.platform == "win32" or not sys.stdin.isatty():
            input("Enterキーを押して終了...")
    except Exception as e:
        print(f"\n\n予期しないエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        if sys.platform == "win32" or not sys.stdin.isatty():
            input("\nEnterキーを押して終了...")