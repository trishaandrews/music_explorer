import time
import pickle
import scipy

import pandas as pd
import numpy as np

from pprint import pprint 
from collections import Counter

def pickle_stuff(filename, data):
    ''' save file '''
    with open(filename, 'w') as picklefile:
        pickle.dump(data, picklefile)

def unpickle(filename):
    ''' open file '''
    with open(filename, 'r') as picklefile:
        old_data = pickle.load(picklefile)
    return old_data

basedir = "./pkls/"
userdict = unpickle(basedir + "userdict.pkl")

kmeans = unpickle(basedir + "kmeans40.pkl")

with open(basedir + "zscore_df_csv.csv", 'r') as tf:
    tracks = pd.read_csv(tf, index_col=0)

#pprint(tracks.head())

listencounts = []
for k, v in userdict.iteritems():
    listencounts.append(len(v))

print sorted(listencounts)[-15:]

t1 = time.time()
count = 0
userclusters = {}
for user, trackidlist in userdict.iteritems():
    if count == 100000:
        print "100000!"
        print "elapsed time:", time.time()-t1
        count = 0
    userclusters[user] = []
    for trackid in trackidlist:
        track = tracks[tracks["track_id"] == trackid]
        track = track.iloc[:,1:] #leave out track_id
        cluster = kmeans.predict(track)
        userclusters[user].append(cluster[0]) #only one track used in predict
    count += 1
print "predict time:", time.time()-t1

#print userclusters
clustercounts = []
clusterfreqs = []
for k, v in userclusters.iteritems():
    num_clusters = kmeans.cluster_centers_.shape[0]
    indcounts = [0 for cl in range(num_clusters)]
    indfreqs = [0 for cl in range(num_clusters)]
    counts = Counter(v)
    countsum = float(sum(counts.values()))
    for name, c in counts.iteritems():
        indcounts[name] = c
        indfreqs[name] = c/countsum
    clustercounts.append(indcounts)
    clusterfreqs.append(indfreqs)
    if len(v) > 30:
        print k, len(v), counts
        print indcounts
        print indfreqs

with open(basedir+"clustercounts.txt", 'w') as cc:
    for clist in clustercounts:
        for c in clist:
            cc.write(str(c) + " ")
        cc.write("\n")

with open(basedir+"clusterfreqs.txt", 'w') as cf:
    for flist in clusterfreqs:
        for f in flist:
            cf.write(str(f) + " ")
        cf.write("\n")

'''
with open(basedir+"clustercounts.txt", 'r') as rc:
    for line in rc:
        countlist = [int(l) for l in line.split()]
        print countlist

with open(basedir + "clusterfreqs.txt", 'r') as rf:
    for line in rf:
        freqlist = [float(l) for l in line.split()]
        print freqlist
'''
