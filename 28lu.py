#!/usr/bin/python
# -*- coding: utf8 -*-
#
import soup as SOUP
import lianhuanhua_columns as COLUMN
import db_access as DB

db = DB.DirectoryDB()

def GetGroup(url, catagory):
    base = SOUP.GetBaseURL(url)
    soup = SOUP.GetSoup(url)
    if soup is None:
        return

    items = soup.find("div", {"class":"lhhlist"})
    if items is None:
        items = soup.find("div", {"class":"zjlist"})
    if items is None:
        return

    items = items.find_all("li")
    for item in items:
        row = {}
        row[COLUMN.DIR_CATAGORY] = catagory
        row[COLUMN.DIR_TITLE] = item.a.text
        row[COLUMN.DIR_LINK] = base + item.a['href']
    
        rows = db.GetRows(None, {COLUMN.DIR_LINK: row[COLUMN.DIR_LINK]})
        if len(rows) == 0:
            print "insert row", row[COLUMN.DIR_TITLE].encode('utf8')
            db.InsertRow(row)

    # next page
    nextPage = soup.find("div", {"class":"nextpage"})
    if nextPage is None:
        return

    links = nextPage.find_all("a")
    tagText = u"下一页"
    for link in links:
        if link.text == tagText:
            if base + link['href'] != url:
                GetGroup(base + link['href'], catagory)
            else:
                return

def GetList(url):
    base = SOUP.GetBaseURL(url)
    soup = SOUP.GetSoup(url)
    main_nav = soup.find("div", {"id":"main_nav"})
    group = main_nav.find_all("li")
    for item in group:
        if item.a['href'] == "/":
            continue    # ignore 'home'
        GetGroup(base + item.a['href'], item.a['title'])

if __name__ == "__main__":
    url = "http://www.28lu.com"
    GetList(url)

