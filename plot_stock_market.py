from __future__ import print_function

# Author: Gael Varoquaux gael.varoquaux@normalesup.org
# License: BSD 3 clause

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import pandas as pd
from sklearn import cluster, covariance, manifold



sys.path.insert(0, "D:\download\Doc\Python_A")
import LoadData_v1


Savedir="D:\\download\\Doc\\MLshare\\data\\";


stock_basics=pd.read_csv(Savedir+"stock_basics.csv",dtype={"code":'U'})
print(stock_basics.dtypes)
print(stock_basics.head())


Datafiles=pd.DataFrame(os.listdir(Savedir),columns=["filename"])
Datafiles=Datafiles[~Datafiles['filename'].isin(["stock_basics.csv","zz500s.csv"])]

Datafiles['code']=Datafiles['filename'].str.slice(0,6)
print(Datafiles)


Datafiles_v=pd.merge(stock_basics,Datafiles['code'].drop_duplicates(),on=["code"],how="inner")

print(Datafiles_v.head())


symbol_dict = {}

for index, row in Datafiles_v.iterrows():
    symbol_dict[row["code"]]=row['name']

print(symbol_dict)

######################################################################
symbols, names = np.array(sorted(symbol_dict.items())).T

quotes = {}
for symbol in symbols:
    quotes[symbol]=LoadData_v1.ReadOneShare(symbol)


formerge=[]

basemerge=pd.DataFrame(columns=['date'])
for tmpk in quotes:
    tmpv=quotes[tmpk]
    tmpv["variation"]=tmpv["close"]-tmpv["open"]
    tmpv["variation_std"]=(tmpv["variation"]-tmpv["variation"].mean())/tmpv["variation"].std()
    tmpm=tmpv[["date","variation_std"]].rename(columns={"variation_std":"variation_std_"+tmpk})
    formerge.append(tmpm)
    basemerge=basemerge.merge(tmpm,on=["date"],how='outer')

   

len_symbols=len(symbols)
tmpcorr=np.eye(len_symbols)
tmpcorr_set=set()
len_symbols=len(symbols)
for tmpi in range(len_symbols):
    for tmpj in range(len_symbols):
        if tmpi==tmpj:continue

        if (tmpj,tmpi) in tmpcorr_set:
            tmpcorr[tmpi,tmpj]=tmpcorr[(tmpj,tmpi)]
            #print("already calc:",tmpcorr[tmpi,tmpj])
        else:
            tmpdf=basemerge[["variation_std_"+symbols[tmpi],"variation_std_"+symbols[tmpj]]].dropna(axis=0,how='any')
            tmpcorr[tmpi,tmpj]=np.corrcoef(tmpdf["variation_std_"+symbols[tmpi]],tmpdf["variation_std_"+symbols[tmpj]])[0,1]
            tmpcorr_set.add((tmpi,tmpj))
            #print("        calc:",tmpcorr[tmpi,tmpj])
            

            


_, labels = cluster.affinity_propagation(tmpcorr)
n_labels = labels.max()

for i in range(n_labels + 1):
    print('Cluster %i: %s' % ((i + 1), ', '.join(names[labels == i])))


