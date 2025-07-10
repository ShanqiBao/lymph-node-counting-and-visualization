import os
from rt_utils import RTStructBuilder  # 用于处理RT结构文件，从中提取mask，其中包含淋巴结信息⭐
import numpy as np
import csv
import pickle

matplotlib.use('Agg')

dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]
marked = np.zeros((500, 1), dtype=int)
visited=np.zeros((550, 550, 450), dtype=int)
mask_3d = None

def dfs(x, y, z, l):
    global visited
    visited[x, y, z] = 1
    l.append((x, y, z))
    for di in range(8):
        x2=x + dx[di]
        y2=y + dy[di]
        if x2 < 0 or x2 >= 512 or y2 < 0 or y2 >= 512: # 图像尺寸512*512
            continue
        if mask_3d[x2, y2, z] == 0:
            continue
        if visited[x2, y2, z]:
            continue
        dfs(x2, y2, z, l)

def main():
    global mask_3d
    global visited
    dcm_path = "/root/autodl-tmp/f126/0000682737(1)"
    rt_path = "/root/autodl-tmp/f126/0000682737(1)/RTSTRUCT.0000682737.default_2.16.840.1.114337.1.11480.1740628339.0.dcm"
    rtstruct = RTStructBuilder.create_from(
        dicom_series_path=dcm_path,
        rt_struct_path=rt_path
    )

    roi_names = rtstruct.get_roi_names()
    tot = 0
    q={}
    for n in roi_names:
    # for n in roi_names[:min(5, roi_names.__len__())]:
        if '0' <= n[0] <= '9' or (n[0] =='C' and '0' <= n[1] <= '9'): # 选出某癌种相关淋巴结
            if n.find('245684')!=-1 or n.find('246276')!=-1 or n.find('215328_LN4')!=-1: # 去掉某些编号的淋巴结
                continue
            mask_3d = rtstruct.get_roi_mask_by_name(n)
            mask_3d = mask_3d.astype('uint8')
            tot += 1
            visited = np.full((550, 550, 450), 0, dtype=int) # 每加载新的mask，一定要更新visited数组
            print(n, tot)
            for kk in range(mask_3d.shape[2]):
                for ii in range(mask_3d.shape[0]):
                    for jj in range(mask_3d.shape[1]):
                        if mask_3d[ii, jj, kk] == 0 or visited[ii,jj,kk]:  # 若不是淋巴结点，则跳过
                            continue
                        l=[]
                        dfs(ii,jj,kk,l)
                        lxx=0
                        lyy=0
                        for li in l:
                            lx,ly,lz=li
                            lxx+=lx
                            lyy+=ly
                        lxx//=len(l)
                        lyy//=len(l)
                        if kk not in q:
                            q[kk] = []
                            marked[kk] = 1
                        q[kk].append((lxx,lyy))

    cell_sz = 6 # 以6*6网格化图像
    d = np.zeros((550, 550, 450))
    for key, value in q.items():
        for iii, jjj in value:
            iii //= cell_sz
            iii = int(iii)
            jjj //= cell_sz
            jjj = int(jjj)
            d[iii, jjj, key] += 1
    
    d=d/np.max(d)
    pr = d[d != 0]
    sorted_pr = np.sort(pr)
    with open('/root/autodl-tmp/f126/o_250509_heatmapDrawing/res/NPC/NPC_pr_48.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for sp in sorted_pr:
            writer.writerow([sp])
    with open('/root/autodl-tmp/f126/o_250509_heatmapDrawing/res/NPC/NPC_q_48.pickle', 'wb') as f:
        pickle.dump(q, f)
    np.save('/root/autodl-tmp/f126/o_250509_heatmapDrawing/res/NPC/NPC_d_48.npy', d)
    np.save('/root/autodl-tmp/f126/o_250509_heatmapDrawing/res/NPC/NPC_marked_48.npy',marked)
    print("get_q_d_marked_NPC_48.py done!")

if __name__ == '__main__':
    main()
