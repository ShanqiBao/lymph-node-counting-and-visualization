from PIL import Image
from pathlib import Path
import re

def overlay_images(bottom_image_path, top_image_path, output_path, position=(0, 0)):
    bottom_image = Image.open(bottom_image_path)
    top_image = Image.open(top_image_path)
    bottom_image = bottom_image.convert("RGBA")
    top_image = top_image.convert("RGBA")
    overlay = Image.new("RGBA", bottom_image.size)
    overlay.paste(bottom_image, (0, 0))
    overlay.paste(top_image, position, top_image)
    overlay.save(output_path, "PNG")


def traverse_png_files(folder_path):
    folder = Path(folder_path)
    for file in folder.rglob('*.png'):
        top_image_path = file
        strs=str(file)
        # print(strs)
        pattern = r'NPC_10_(\d+)'
        match = re.search(pattern, strs)
        number_part = match.group(1)
        bottom_image_path = f"/root/autodl-tmp/f126/ctPng/CT{str((int(number_part)-217)//6+37)}.png" # 144-(x+4*((151-x)//3+1)-62)
        output_path = f"/root/autodl-tmp/f126/o_250509_heatmapDrawing/res/NPC/NPC_10_{int(number_part)}.png"
        overlay_images(bottom_image_path, top_image_path, output_path)
        

if __name__ == "__main__":
    folder_path = '/root/autodl-tmp/f126/o_250509_heatmapDrawing/temp/NPC/NPC10'
    traverse_png_files(folder_path)
