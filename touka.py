#!/usr/bin/env python3
import os
import sys
import argparse
from PIL import Image
import numpy as np

def hex_to_rgb(hex_color):
    """16進数カラーコードをRGBタプルに変換"""
    hex_color = hex_color.lstrip('#')
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
    parser.add_argument('color', help='透過にする色のカラーコード (例: #FFFFFF または FFFFFF)')
    args = parser.parse_args()
    
    # カラーコードをRGBに変換
    try:
        target_color_rgb = hex_to_rgb(args.color)
    except Exception as e:
        print(f"エラー: 無効なカラーコードです - {args.color}")
        sys.exit(1)
    
    print(f"透過色: #{args.color.lstrip('#')} (RGB: {target_color_rgb})")
    
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

if __name__ == "__main__":
    main()