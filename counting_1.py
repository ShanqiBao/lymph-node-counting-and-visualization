import os
from rt_utils import RTStructBuilder
import numpy as np
import pickle

matplotlib.use('Agg')

dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]
visited=np.full((550, 550, 450), 0, dtype=int)
mask_3d = None

def dfs(x, y, z, l):
    global visited
    visited[x, y, z] = 1
    l.append((x, y, z))
    for di in range(8):
        x2=x + dx[di]
        y2=y + dy[di]
        if x2 < 0 or x2 >= 512 or y2 < 0 or y2 >= 512:
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
    c={}
    for n in roi_names:
    # for n in roi_names[:min(5, roi_names.__len__())]:
        if '0' <= n[0] <= '9' or (n[0] =='C' and '0' <= n[1] <= '9'):
            if n.find('245684')!=-1 or n.find('246276')!=-1 or n.find('215328_LN4')!=-1:
                continue
            mask_3d = rtstruct.get_roi_mask_by_name(n)
            mask_3d = mask_3d.astype('uint8')
            tot += 1
            visited = np.full((550, 550, 450), 0, dtype=int)
            print(n, tot)
            for kk in range(mask_3d.shape[2]):
                for ii in range(mask_3d.shape[0]):
                    for jj in range(mask_3d.shape[1]):
                        if mask_3d[ii, jj, kk] == 0 or visited[ii,jj,kk]:
                            continue
                        l=[]
                        dfs(ii,jj,kk,l)
                        # print(l)
                        lxx=0
                        lyy=0
                        for li in l:
                            lx,ly,lz=li
                            lxx+=lx
                            lyy+=ly
                        # print(len(l))
                        lxx//=len(l)
                        lyy//=len(l)
                        if n not in c:
                            c[n] = []
                        c[n].append((lxx,lyy,kk)) # 一个淋巴结由多个小点构成，取其坐标均值作为该淋巴结的最终坐标。c中存储淋巴结名称及其最终坐标
    # print(c)
    with open('/root/autodl-tmp/f126/o_250508_Counting/res/NPC/c/NPC_c_48.pickle', 'wb') as f:
        pickle.dump(c, f)
    print("counting_1.py done!")

if __name__ == '__main__':
    main()
