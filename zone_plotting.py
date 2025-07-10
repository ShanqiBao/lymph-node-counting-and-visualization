import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from skimage import measure
import os

def main():
    names = ['IVa_L', 'IVa_R', 'IVb_L', 'IVb_R', 'PLV_L', 'PLV_R', 'Vb_L', 'Vb_R', 'Vc_L', 'Vc_R', 'VIa', 'VIb', 'VIb_L', 'VIb_R']
    p1 = Path("/root/autodl-tmp/f126/Data/zone")
    p2 = Path("/root/autodl-tmp/f126/o_zone")
    
    if not p2.exists(): # 确保输出目录存在，递归地创建所有缺失的上级目录
        p2.mkdir(parents=True)
    
    for nn in names:
        fn1 = f"{nn}.npy"
        fp1 = p1 / fn1
        voxel_data = np.load(fp1)
        output_dir = p2 / nn
        if not output_dir.exists():
            output_dir.mkdir()
        
        for z in range(voxel_data.shape[2]):
            slice_data = voxel_data[:, :, z]
            contours = measure.find_contours(slice_data, 0.5) # 提取二值图像边界。其中有淋巴结的地方值为 1，背景为 0，故 0.5 可提取其边界⭐
            if not contours:
                continue
            
            fig = plt.figure(figsize=(5.12, 5.12), dpi=100)
            ax = fig.add_axes([0, 0, 1, 1])  # [left, bottom, width, height]
            ax.set_xlim(0, 512)
            ax.set_ylim(0, 512)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.invert_yaxis()
            
            for contour in contours:
                x = contour[:, 1] 
                y = contour[:, 0] 
                ax.plot(x, y, 'c-', linewidth=0.5)
            
            output_path = output_dir / f"{nn}_{z}.png"
            plt.savefig(output_path, dpi=100, transparent=True)
            plt.close()


if __name__ == '__main__':
    main()
