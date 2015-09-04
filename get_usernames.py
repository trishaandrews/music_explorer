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

basedir="./pkls/"
artisthtml="./html/"

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
        #time.sleep(1) 
        if verbose > 0:
            print count,
            print "elapsed seconds:", time.time() - t1
            sys.stdout.flush()
        count += 1   

#failed after:
#line: 12699
#12 elapsed seconds: 105.508145094
#11 elapsed seconds: 127.551074982
#10 elapsed seconds: 77.4061279297
#12 elapsed seconds: 114.080958128
#11 elapsed seconds: 135.483647108
#11 elapsed seconds: 116.247781038
#13 elapsed seconds: 130.090771198
#31 elapsed seconds: 407.033605099
#9 elapsed seconds: 96.6621789932
#20 elapsed seconds: 235.159045935
#8 elapsed seconds: 98.0897989273
#13 elapsed seconds: 209.054129124
#7 elapsed seconds: 57.9254448414
#9 elapsed seconds: 115.961382151
#10 elapsed seconds: 115.521682978
#9 elapsed seconds: 94.6024179459
#9 elapsed seconds: 84.2044129372
#9 elapsed seconds: 88.7101960182
#7 elapsed seconds: 66.4792208672
#11 elapsed seconds: 127.638660908
#7 elapsed seconds: 75.2802710533
#8 elapsed seconds: 81.3885819912
#8 elapsed seconds: 92.1391868591
#11 elapsed seconds: 93.8353919983
#added: session.set_attribute('auto_load_images', False)
#25 elapsed seconds: 108.70004487
#23 elapsed seconds: 69.9956889153
#24 elapsed seconds: 82.3035378456
#24 elapsed seconds: 119.112738132
#24 elapsed seconds: 102.139042854
#moved session init out of loop
#539 elapsed seconds: 1603.91038299
#done? 
print "len artists:", len(artists)
get_many_usernames(artists[925:], verbose=1)

#username_urls = set(username_urls)

        
#print len(username_urls)

