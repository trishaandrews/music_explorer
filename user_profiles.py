import time
import pickle
import scipy

import pandas as pd
import numpy as np

from pprint import pprint 


def pickle_stuff(filename, data):
    ''' save file '''
    with open(filename, 'w') as picklefile:
        pickle.dump(data, picklefile)

def unpickle(filename):
    ''' open file '''
    with open(filename, 'r') as picklefile:
        old_data = pickle.load(picklefile)
    return old_data

with open("mismatch_tracks.txt", 'r') as mtf:
    bad_tracks = mtf.read().split()

print bad_tracks[:5]

btset = set(bad_tracks)

with open(basedir + "titles_csv3.csv", 'r') as tf:
    titles = pd.read_csv(tf, index_col=0)
#titles = unpickle("titles_df.pkl")
#print titles.head()
users = []
songs = []
userdict = {}
userlim = 10000
usercount = 0

t1 = time.time()
#this is a 3gb file
with open("train_triplets.txt", 'r') as ttf:
    for line in ttf:
        if usercount >= userlim:
            print "10000!"
            print "elapsed time:", time.time() - t1
            usercount = 0
        #I'm not going to use play count, which would be splits[2]
        splits = line.split()
        user = splits[0]
        song = splits[1]
        if song in titles.song_id.values:
            trackmatches = titles[titles["song_id"] == song]
            trackmatches = trackmatches["track_id"].values
            for track in trackmatches:
                if track not in btset:
                    if user in userdict:
                        userdict[user].append(track)
                    else:
                        userdict[user] = [track]
                        usercount += 1
print "dictionary time:", time.time()-t1
#dictionary time: 12287.5914891

listencounts = []
for k, v in userdict.iteritems():
    listencounts.append(len(v))

print sorted(listencounts)[-15:]

pickle_stuff("userdict.pkl", userdict)


