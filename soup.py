#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Written by Victor Liu
# June 2013
#

# read and parse URL page into BeatifulSoup object

import cookielib, urllib2, urlparse
from bs4 import BeautifulSoup

##
# return url base
#
def GetBaseURL(url):
    base = urlparse.urlparse(url)
    return urlparse.urlunparse((base.scheme, base.netloc, '', '', '', ''))

##
# save Beautifulsoup object into a file
#
def savePrettify(filename, soup, url):
    print "save prettify to", filename
    tmp = open(filename, "w")
    tmp.write(url)
    tmp.write(soup.prettify().encode("utf8"))
    tmp.close()

def GetSoupStr(str):
    return BeautifulSoup(str)

##
# Get Beautifulsoup from URL, optionally save soup to file
# Return: soup
#
def GetSoup(url, saveFile=None):
    print "get", url
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    request = urllib2.Request(url)
    soup = None
    try:
        page = opener.open(request)
        soup = BeautifulSoup(page)
    except urllib2.HTTPError:
        print "http error:", url
        return None
    except urllib2.URLError:
        print "url error: ", url
        return None

    # optionally save source
    if (soup is not None) and (saveFile is not None):
        savePrettify(saveFile, soup, url)

    return soup

##
# run from command line
# print html content or save it to file
#
#   $ soup.py [URL] [filename]
#
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        soup = GetSoup(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        soup = GetSoup(sys.argv[1])
        if soup is not None:
            print soup
    else:
        print "Parse URL and opitionally save into file"
        print " soup.py [URL] [filename]"

