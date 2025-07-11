import csv
import pickle
import numpy as np
from pathlib import Path

def main():
    with open('/root/autodl-tmp/f126/o_250508_Counting/LC/res1/LC_c_8.pickle', 'rb') as f:
        c = pickle.load(f)
    # ns = {"a": [(1, 2, 3), (4, 5, 6)], "b": [(9, 9, 9)]}
    # print(c)
    names=['IVa_L','IVa_R','IVb_L','IVb_R','PLV_L','PLV_R','Vb_L','Vb_R','Vc_L','Vc_R','VIa','VIb','VIb_L','VIb_R']
    p1 = Path("/root/autodl-tmp/f126/Data/zone")
    p2= Path("/root/autodl-tmp/f126/o_250508_Counting/LC/res")

    for nn in names:
        fn1 = f"{nn}.npy"
        fp1 = p1 / fn1
        n = np.load(fp1)
        # print(n[n!=0].sum())
        for key, value in c.items():
            # print(key,value)
            for v in value:
                i, j, k = v
                # print(i, j, k)
                # k += 5 # 若错位
                N = nn
                if(n[i,j,k] == 1):
                    if N != 'VIb' and N != 'VIa':
                        N = N[:-2]
                    fn2 = f"LC8_{N}.csv"
                    fp2 = p2 / fn2
                    with open(fp2, mode='a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([key])
            

if __name__ == '__main__':
    main()
