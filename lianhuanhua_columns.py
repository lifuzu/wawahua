#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Written by Victor Liu
# June 2013
#

##
# this file defines column names for review database
#
DB_FILE = "database/lianhuanhua.db"

# Directory Table
TABLE_DIRECTORY = "directory"
DIR_CATAGORY = "catagory"   # catagory of the book
DIR_LINK = "link"   # source url
DIR_TITLE = "title" # book's title
DIR_FOLDER = "folder" # folder if saved

# Content Table
TABLE_CONTENT = "content"
CONT_ID = "dir_id"  # ROWID in Directory Table
CONT_PAGE = "page" # page number
CONT_LINK = "link" # source url
CONT_FILE = "file" # filename if saved

