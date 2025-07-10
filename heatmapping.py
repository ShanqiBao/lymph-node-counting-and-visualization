import os
import matplotlib.pyplot as plt
from rt_utils import RTStructBuilder
import numpy as np
import matplotlib
import csv
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

matplotlib.use('Agg')

def main():
    d=np.load('/root/autodl-tmp/f126/o_250509_heatmapDrawing/temp/NPC/NPC_d_4.npy', allow_pickle=True)
    marked=np.load('/root/autodl-tmp/f126/o_250509_heatmapDrawing/temp/NPC/NPC_marked_4.npy', allow_pickle=True)
    num = 85 # 512//6
    cmap_colors = [
                   (0, 0, 0, 0), # sin color
                   (0.1, 0.5, 1, 1), # azul
                   (1, 1, 0, 1), # amarilla
                   (1, 0, 0, 1) # roja
    ]
    
    for aa in range(429):
        if marked[aa] == 0:
            continue
        pic = np.zeros((num, num))
        for bb in range(num):
            for cc in range(num):
                pic[bb, cc] = d[bb, cc, aa]
        mycmap = LinearSegmentedColormap.from_list('my_colormap', cmap_colors)
        norm = plt.Normalize(vmin=0, vmax=1)  # 归一化

        output_dir = "/root/autodl-tmp/f126/o_250509_heatmapDrawing/NPC/NPC4"
        os.makedirs(output_dir, exist_ok=True)

        pic_normalized = np.zeros_like(pic) # 将 pic 的数值映射到颜色区间
        pic_normalized[pic >= 0] = 0 # sin color
        pic_normalized[(pic > 0) & (pic < 0.05)] = 0.333 # azul
        pic_normalized[(pic >= 0.05) & (pic <= 0.2)] = 0.666 # amarilla
        pic_normalized[pic > 0.2] = 1.0  # roja

        fig_size = (5.12, 5.12)
        dpi = 100
        fig = plt.figure(figsize=fig_size, dpi=dpi)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        im = ax.imshow(pic_normalized, cmap=mycmap, norm=norm, interpolation='gaussian', alpha=1)
        plt.savefig(f"{output_dir}/NPC_48_{aa+1}.png", transparent=True)
        plt.close()

    print(f"Saved in '{output_dir}'!")


if __name__ == '__main__':
    main() 
