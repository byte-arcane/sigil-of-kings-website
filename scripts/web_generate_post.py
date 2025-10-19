import argparse
import os
import sys
import subprocess

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "kate"
        subprocess.call([opener, filename])

fmt = """---
layout: post
title: $TITLE
date: $YEAR-$MONTH-$DAY 00:00:00.000000000 +00:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- random
tags: []
image: assets/$YEAR/$MONTH/$IMAGE
video: assets/video/$VIDEO
meta:
author:
permalink: "/$YEAR/$MONTH/$DAY/$TITLE_DASH/"
---

Hello
"""

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--title', help="title", type=str, required=True)
parser.add_argument('-d', '--date', help="date (e.g. 5/12/22)", type=str, required=True)
parser.add_argument('-i', '--image', help="image", type=str, required=False)
parser.add_argument('-v', '--video', help="video", type=str, required=False)
args = parser.parse_args()

title_dash = args.title.lower().replace(' ','-').replace('\'','').replace(',','').replace(':','')

(day,month,year) = args.date.split('/')
if len(year) == 2:
    year = "20"+year
if len(day) == 1:
    day = "0"+day
if len(month) == 1:
    month = "0"+month

if args.video:
    fmt = fmt.replace('$VIDEO',args.video)
    fmt = fmt.replace('image: assets/$YEAR/$MONTH/$IMAGE\n','')
elif args.image:
    fmt = fmt.replace('$IMAGE',args.image)
    fmt = fmt.replace('video: assets/video/$VIDEO\n','')
else:
    fmt = fmt.replace('image: assets/$YEAR/$MONTH/$IMAGE\n','')
    fmt = fmt.replace('video: assets/video/$VIDEO\n','')
    
fmt = fmt.replace('$YEAR',year)
fmt = fmt.replace('$MONTH',month)
fmt = fmt.replace('$DAY',day)
fmt = fmt.replace('$TITLE_DASH',title_dash)
fmt = fmt.replace('$TITLE',args.title)

fname =  os.path.dirname(__file__) + f'/../_posts/{year}-{month}-{day}-{title_dash}.html'
with open( fname, 'wt') as fp:
    fp.write(fmt)
open_file(fname)



# Example call: web_generate_post.py --title "My awesome post" --date 2/4/22 --video some_amazing_stuff_tw.mp4
# Then fill content with: https://markdowntohtml.com/
