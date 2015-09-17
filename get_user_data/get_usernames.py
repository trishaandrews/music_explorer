import requests
import time
import re
import pickle
import unicodedata
import json
import sys
import dryscrape
from bs4 import BeautifulSoup
#from datetime import datetime
from pprint import pprint


# ##These are the fields I think I want:

# ```
# <div class="nowslider_copywrap">
#   <a class="nowslider_name" href="/user/sl_p">sl_p</a><br>
#   <a class="nowslider_artist" href="/music/Coldplay">Coldplay</a><br>
#   <a class="nowslider_track" href="/music/Coldplay/_/The+Scientist">The Scientist</a>
#   <div class="nowslider_scrobbles">Plays: 145</div>
# </div>
# 
# <div class="username"> <a href="/user/PsychedelicBina">PsychedelicBina</a>
# ```

basedir="../pkls/"

with open(basedir+"topartist_urls.txt", 'r') as auf:
    artists = auf.read().split()


def get_many_usernames(artist_urls, verbose=0):
    session = dryscrape.Session()
    session.set_attribute('auto_load_images', False)
    t1 = time.time()
    count = 0
    for url in artist_urls:
        username_urls = []       
        session.visit(url)
        time.sleep(1)
        page = session.body()
        soup = BeautifulSoup(page)
        usernames = soup.find_all(class_="username")
        for un in usernames:
            username_urls.append(un.a.get('href'))
        slidernames = soup.find_all(class_="nowslider_name")
        for sn in slidernames:
            username_urls.append(sn.get('href'))
        #slightly minimize repeats 
        #(not all of them, though, so do this again later!)
        username_urls = set(username_urls)
        with open("username_urls2.txt", 'a') as uuf:
            for uu in username_urls:
                uuf.write(uu+"\n")
        if verbose > 0:
            print count,
            print "elapsed seconds:", time.time() - t1
            sys.stdout.flush()
        count += 1   

print "len artists:", len(artists)
get_many_usernames(artists, verbose=1)

#username_urls = set(username_urls)

        
#print len(username_urls)

