# coding=utf-8

import sys, os
from weibopy.auth import OAuthHandler
from weibopy.api import API
import time
import random, math
import urllib, urllib2
import md5 # deprecated in Python 2.5 or after

def str2code(s):
    # code = ''
    # for c in s:
    #     h = hex(ord(c))
    #     code += h[2:]
    # return code
    m = md5.new()
    m.update(s)
    return m.hexdigest()

try:
    filenames = ['/home/caq/fortune-zh-1.9/tang.poem', '/home/caq/fortune-zh-1.9/song.poem']
    poem = ['', '']
    title = ['', '']
    author = ['', '']
    for current in [0, 1]:
        f = open(filenames[current])
        for line in f.readlines():
            line = line.strip()
            if line.startswith('题目:'):
                line = line[line.find(':')+1:]
            elif line.startswith('作者:'): # tang
                line = line[line.find(':')+1:] + ' '
                author[current] = line.strip()
            elif line.startswith('作者：'): # song
                line = line[line.find('：')+len('：'):] + ' '
                author[current] = line.strip()
            if line.startswith('《'):
                title[current] = line.strip()
                title[current] = title[current][len('《') : title[current].find('》')]
            if line.endswith('） ') or line.endswith('）'):
                line = line[:line.find('（')] + ' '
                author[current] = line.strip()
            poem[current] += line
        f.close()

    msg = '#唐宋诗词#'
    rnd = random.randint(0, 3)
    if rnd <= 2:
        choose = 0
    else:
        choose = 1
    msg += poem[choose]
    msg += '[' + time.strftime('%H:%M', time.localtime(time.time())) + ']'

    imgfilename = '/home/caq/fortune-zh-1.9/poemimg/' + str2code(title[choose]) + '-' + str2code(author[choose]) + '.jpg'
    hasimg = True

    if not os.path.isfile(imgfilename):
        hasimg = False
        params = {'client':'ms-opera-mini', 'channel':'new', 'imgtype':'photo', 'q':title[choose] + ' ' + author[choose], 'site':'images'}
        content = urllib2.urlopen(urllib2.Request('http://www.google.com/m/search', urllib.urlencode(params))).read()
        content = content[content.find('<br/>'):]
        imgsrc = ''
        imgsrcind = content.find('&amp;imgurl=')
        if imgsrcind >= 0:
            imgsrc = content[imgsrcind+12 : content.find('&amp;imgrefurl', imgsrcind+8)]
        if len(imgsrc) > 0:
            imgsrc = urllib.unquote(imgsrc)
            print imgsrc
            try:
                imgfile = open(imgfilename, 'wb')
                imgfile.write(urllib2.urlopen(imgsrc).read())
                imgfile.close()
                hasimg = True
            except:
                pass

    f = open('/home/caq/fortune-zh-1.9/tangsong.config')
    cks = f.readline().strip().split('\t')
    tks = f.readline().strip().split('\t')
    # consumer_key, consumer_secret
    auth = OAuthHandler(cks[0], cks[1])
    # token, tokenSecret
    auth.setToken(tks[0], tks[1])
    api = API(auth)

    umsg = msg.decode('utf-8')
    currp = 0
    totalp = int(math.ceil(float(len(umsg)) / 139))
    if len(umsg) > 130:
        for currp in range(0, totalp):
            # print '(' + str(currp+1) + '/' + str(totalp) + ')' + umsg[currp*130:currp*130+130]
            thismsg = '(' + str(currp+1) + '/' + str(totalp) + ')' + umsg[currp*130:currp*130+130]
            if currp == 0:
                api.upload(filename=imgfilename, status=thismsg.encode('utf-8'))
            else:
                api.update_status(thismsg)
            time.sleep(1)
    else:
        # print umsg
        if hasimg:
            api.upload(filename=imgfilename, status=umsg.encode('utf-8'))
        else:
            api.update_status(umsg)
except:
    #raise
    pass
