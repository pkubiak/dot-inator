#! /usr/bin/python2
import sys
from PIL import Image, ImageDraw
import random
from math import *

def dist2(a,b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

radius = 9
# Dotiffy single image
def dotiffy(img, n = 100):
    w, h = img.size

    # TODO: adjust this values according to image size
    padding = 1
    minimum = 3
    maximum = 15
    min_size = 3

    res = []
    i = 0
    while i < n:
        x = random.randint(0, w-1)
        y = random.randint(0, h-1)

        c=image.getpixel((x,y))
        if c[3] > 250:
            m = 10000
            for j in xrange(len(res)):
                m = min(m, dist2((res[j]['cx'], res[j]['cy']), (x,y)) - res[j]['r'] - padding - minimum)

            if m >= 0:
                r = random.uniform(0, min(m, maximum-minimum))
                res.append({'cx': x, 'cy': y, 'r': r+minimum, 'color': c})
                i+=1
    return res


# output buffer
svg = []
frames = []
count = 1200
ps = 0.7

ile = len(sys.argv)-1

for file_name in sys.argv[1:]:
    image = Image.open(file_name)

    frame = dotiffy(image, count)
    frames.append(frame)

svg.append('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
svg.append("""
    <svg
       version=\"1.1\"
       viewBox=\"0 0 2cm 2cm\"
       xmlns:dc="http://purl.org/dc/elements/1.1/"
       xmlns:cc="http://creativecommons.org/ns#"
       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
       xmlns:svg="http://www.w3.org/2000/svg"
       xmlns="http://www.w3.org/2000/svg">
    """)
frames.append(frames[0])

for i in xrange(count):

    cx_values = '; '.join([str(frames[f//2][i]['cx']) for f in xrange(2*len(frames))])
    cy_values = '; '.join([str(frames[f//2][i]['cy']) for f in xrange(2*len(frames))])
    radiuses = '; '.join([str(frames[f//2][i]['r']) for f in xrange(2*len(frames))])
    colors = []
    for f in frames:
        c = f[i]['color']
        # print c

        colors.append("rgba(%(r)d, %(g)d, %(b)d, %(a)f)" % {'r': c[0], 'g': c[1], 'b': c[2], 'a': float(c[3])/255.0})
        colors.append("rgba(%(r)d, %(g)d, %(b)d, %(a)f)" % {'r': c[0], 'g': c[1], 'b': c[2], 'a': float(c[3])/255.0})

    colors = '; '.join(colors)

    times = []
    F = len(frames)
    s = ps*0.5/float(F-1)

    '; '.join([str(float(f)/float(len(frames)-1)) for f in xrange(len(frames))])
    for f in xrange(F):
        t = float(f)/float(F-1)
        times.append(str(max(t-s,0.0)))
        times.append(str(min(t+s,1.0)))
    times = '; '.join(times)

    svg.append("""
        <circle id='path%(id)s' style='stroke:none' r='%(radius)s' cx='%(cx)s' cy='%(cy)s'>
            <animate attributeName='cx' begin='0s' values='%(cx_values)s' keyTimes='%(times)s' dur="%(dur)ds" repeatCount="indefinite"/>
            <animate attributeName='cy' begin='0s' values='%(cy_values)s' keyTimes='%(times)s' dur="%(dur)ds" repeatCount="indefinite"/>
            <animate attributeName='fill' begin='0s' values='%(colors)s' keyTimes='%(times)s' dur="%(dur)ds" repeatCount="indefinite"/>
            <animate attributeName='r' begin='0s' values='%(radiuses)s' keyTimes='%(times)s' dur="%(dur)ds" repeatCount="indefinite"/>
        </circle>
    """ % {'id': 1000+i, 'cx_values': cx_values, 'times': times, 'cy_values': cy_values, 'colors': colors, 'cx': 0, 'cy': 0, 'radius': 9, 'dur': 2*ile, 'radiuses': radiuses})

svg.append("</svg>")
print "\n".join(svg)


# TODO: parametry typu float
# TODO: programowanie linowe
# TODO: generowanie animacji
