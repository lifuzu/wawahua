#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Written by Victor Liu
# Jun 2013
#

import soup as SOUP
import lianhuanhua_columns as COLUMN
import db_access as DB

contentDb = DB.ContentDB()
directoryDb = DB.DirectoryDB()

def GetContent(rowId, url, rows):
    base = SOUP.GetBaseURL(url)
    soup = SOUP.GetSoup(url)

    contentleft = soup.find("td", {"class":"contentleft"})
    if contentleft is not None:
        contentpic = contentleft.find("div", {"class":"contentpic"})
        if contentpic is not None:
            pics = contentpic.find_all("img")
            for pic in pics:
                row = {}
                row[COLUMN.CONT_ID] = rowId
                row[COLUMN.CONT_PAGE] = len(rows) + 1
                row[COLUMN.CONT_LINK] = base + pic['src']
                row[COLUMN.CONT_FILE] = ""
                rows.append(row)
                
    nextpage = contentleft.find("div", {"class":"nextpagec"})
    if nextpage is not None:
        links = nextpage.find_all("a")
        for link in links:
            if link.text == u'下一页':
                if base + link['href'] != url:
                    GetContent(rowId, base + link['href'], rows)
    

def GetAllContent():
    rows = directoryDb.GetRows(["ROWID", COLUMN.DIR_LINK])
    for row in rows:
        GetLinkContent(row['rowid'], row[COLUMN.DIR_LINK])

def GetIdContent(rowId):
    rows = directoryDb.GetRows(["ROWID", COLUMN.DIR_LINK], {"ROWID":rowId})
    if len(rows) == 0:
        print "no row:", rowId
        return;

    row = rows[0]
    GetLinkContent(rowId, row[COLUMN.DIR_LINK])

def GetLinkContent(rowId, link):
    print "Get content: ", rowId
    done = contentDb.GetRows(["ROWID"], {COLUMN.CONT_ID:rowId})
    if len(done) == 0:
        rows = []
        GetContent(rowId, link, rows)
        contentDb.InsertRows(rows)
    else:
        print rowId, " exists"


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        GetIdContent(sys.argv[1])
    else:
        GetAllContent()
    #url = sys.argv[1]
    #GetContent(0, url, {'page':0})

