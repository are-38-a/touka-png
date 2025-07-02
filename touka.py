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

def make_transparent_and_crop(image_path, target_color_rgb, output_path):
    """指定色を透過にして画像をトリミング"""
    img = Image.open(image_path).convert('RGBA')
    data = np.array(img)
    
    # RGBチャンネルを抽出
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # 指定色のピクセルを透過に
    mask = (r == target_color_rgb[0]) & (g == target_color_rgb[1]) & (b == target_color_rgb[2])
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
    
    print(f"透過色: #{color_code.lstrip('#')} (RGB: {target_color_rgb})")
    
    # 現在のディレクトリ内のPNGファイルを取得
    png_files = [f for f in os.listdir('.') if f.lower().endswith('.png') and not f.endswith('-touka.png')]
    
    if not png_files:
        print("エラー: PNGファイルが見つかりません。")
        sys.exit(1)
    
    print(f"{len(png_files)}個のPNGファイルを処理します...")
    
    success_count = 0
    for png_file in png_files:
        base_name = os.path.splitext(png_file)[0]
        output_file = f"{base_name}-touka.png"
        
        try:
            if make_transparent_and_crop(png_file, target_color_rgb, output_file):
                print(f"✓ {png_file} → {output_file}")
                success_count += 1
        except Exception as e:
            print(f"✗ {png_file} の処理中にエラーが発生しました: {e}")
    
    print(f"\n処理完了: {success_count}/{len(png_files)} ファイル")
    
    # Windows環境でウィンドウがすぐ閉じないようにする
    if sys.platform == "win32" or not sys.stdin.isatty():
        input("\nEnterキーを押して終了...")

if __name__ == "__main__":
    main()