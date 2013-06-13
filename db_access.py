#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Written by Victor Liu
# June 2013
#

# SQLITE3 database interface classes

import os
import sqlite3

import lianhuanhua_columns as COLUMN

## 
# get relative path of the database file
#
def GetDBPath():
    filePath = os.path.dirname(os.path.abspath(__file__))
    #upPath = filePath.rpartition("/")[0]
    return filePath

##
# [internal function]
# generate names and values used by SQL insert
#
def GetNamesAndValues(dictRow):
    names = ""
    args = ""
    values = ()
    for key in dictRow:
        if names != "":
            names += "," + key
            args += ",?"
        else:
            names += key
            args += "?"
        if dictRow[key] is None:
            print "None value in", key
        values = values + (dictRow[key],)

    if names != "": 
        names = "(" + names + ") VALUES(" + args + ")"
    return (names, values)

##
# review DB class
#   CreateTable()
#   InsertRow(Dict row)
#
class DirectoryDB():
    def __init__(self):
        self.dbFileName = GetDBPath() + "/" + COLUMN.DB_FILE
        self.tableName = COLUMN.TABLE_DIRECTORY
        self.conn = None
        if not os.path.exists(self.dbFileName):
            print "create DB", self.dbFileName
        self.CreateTable()

    def OpenConnection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.dbFileName)

    def CloseConnection(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def CreateTable(self):
        print "create table", self.tableName , " in ", self.dbFileName
        sql = "CREATE TABLE " + self.tableName
        sql += "(" + "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP"
        sql += "," + COLUMN.DIR_CATAGORY + " TEXT"
        sql += "," + COLUMN.DIR_TITLE + " TEXT"
        sql += "," + COLUMN.DIR_LINK + " TEXT"
        sql += "," + COLUMN.DIR_FOLDER + " TEXT"
        sql += ")"
        try:
            self.OpenConnection()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            cursor.close()
            self.conn.commit()
            self.CloseConnection()
        except:
            print "!!! table created"

    ##
    # GetRow
    #
    def GetRows(self, columns=None, where=None):
        cols = None
        if columns is None:
            cols = '*'
        else:
            for c in columns:
                if cols is None:
                    cols = c
                else:
                    cols += "," + c 
        sql = "SELECT " + cols + " FROM " + self.tableName
        clause = ""
        values = ()
        if not where is None:
            for key in where:
                clause = key + "=?"
                values = (where[key],)
                break   # accept only one arg
        self.OpenConnection()
        cursor = self.conn.cursor()
        if clause is not "":
            sql += " WHERE " + clause
        cursor.execute(sql, values)
        result = cursor.fetchall()
        rows = []
        for row in result:
            c = 0
            record = {}
            for cloumn in cursor.description:
                record[cloumn[0]] = row[c]
                c += 1
            rows.append(record)
        cursor.close()
        self.CloseConnection()
        return rows
 
    ##
    # check existing row
    # return 0 or >0
    #
    def IsRowExist(self, row):
        sql = "SELECT * FROM " + self.tableName
        sql += " WHERE " + COLUMN.DIR_LINK + "=?"
        values = (row[COLUMN.DIR_LINK],)
        self.OpenConnection()
        cursor = self.conn.cursor()
        cursor.execute(sql, values)
        rows = cursor.fetchall()
        count = len(rows)
        cursor.close()
        self.CloseConnection()
        return count

    ##
    # insert dictionary row into table
    # return True if successful, or False
    #
    def InsertRow(self, row):
        # check row existing before insert
        if self.IsRowExist(row) > 0:
            return False

        #print "insert into", self.tableName
        (names, values) = GetNamesAndValues(row)
        if names == "":
            return False
        try:
            sql = "INSERT INTO " + self.tableName + names
            # connect to DB
            self.OpenConnection()
            cursor = self.conn.cursor()
            cursor.execute(sql, values)
            cursor.close()
            self.conn.commit()
            self.CloseConnection()
        except:
            print "!!! insert failed"
            print sql
            print values
            raise
            return False
        return True
    
class ContentDB():
    def __init__(self):
        self.dbFileName = GetDBPath() + "/" + COLUMN.DB_FILE
        self.tableName = COLUMN.TABLE_CONTENT
        self.conn = None
        if not os.path.exists(self.dbFileName):
            print "create DB", self.dbFileName
        self.CreateTable()

    def OpenConnection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.dbFileName)

    def CloseConnection(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def CreateTable(self):
        print "create table", self.tableName , " in ", self.dbFileName
        sql = "CREATE TABLE " + self.tableName
        sql += "(" + "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP"
        sql += "," + COLUMN.CONT_ID + " INTEGER"
        sql += "," + COLUMN.CONT_PAGE + " INTEGER"
        sql += "," + COLUMN.CONT_LINK + " TEXT"
        sql += "," + COLUMN.CONT_FILE + " TEXT"
        sql += ")"
        try:
            self.OpenConnection()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            cursor.close()
            self.conn.commit()
            self.CloseConnection()
        except:
            print "!!! table created"

    ##
    # GetRow
    #
    def GetRows(self, columns=None, where=None):
        cols = None
        if columns is None:
            cols = '*'
        else:
            for c in columns:
                if cols is None:
                    cols = c
                else:
                    cols += "," + c 
        sql = "SELECT " + cols + " FROM " + self.tableName
        clause = ""
        values = ()
        if not where is None:
            for key in where:
                clause = key + "=?"
                values = (where[key],)
                break   # accept only one arg
        self.OpenConnection()
        cursor = self.conn.cursor()
        if clause is not "":
            sql += " WHERE " + clause
        cursor.execute(sql, values)
        result = cursor.fetchall()
        rows = []
        for row in result:
            c = 0
            record = {}
            for cloumn in cursor.description:
                record[cloumn[0]] = row[c]
                c += 1
            rows.append(record)
        cursor.close()
        self.CloseConnection()
        return rows
 
    ##
    # check existing row
    # return 0 or >0
    #
    def IsRowExist(self, row):
        sql = "SELECT * FROM " + self.tableName
        sql += " WHERE " + COLUMN.CONT_LINK + "=?"
        values = (row[COLUMN.CONT_LINK],)
        self.OpenConnection()
        cursor = self.conn.cursor()
        cursor.execute(sql, values)
        count = len(cursor.fetchall())
        cursor.close()
        self.CloseConnection()
        return count

    ##
    # insert dictionary row into table
    # return True if successful, or False
    #
    def InsertRows(self, rows):
        # check row existing before insert
        if self.IsRowExist(rows[0]) > 0:
            return False

        #print "insert into", self.tableName
        sql = ""
        names = ""
        values = ()
        print "InsertRows: ", len(rows)
        try:
            # connect to DB
            self.OpenConnection()
            cursor = self.conn.cursor()
            for row in rows:
                (names, values) = GetNamesAndValues(row)
                sql = "INSERT INTO " + self.tableName + names
                cursor.execute(sql, values)
            cursor.close()
            self.conn.commit()
            self.CloseConnection()
        except:
            print "!!! insert failed"
            print sql
            print values
            raise
            return False
        return True
    
if __name__ == "__main__":
    # create database file and table
    db = DirectoryDB()

    # insert a row to table
    row = {COLUMN.DIR_CATAGORY:u"名著连环画",
           COLUMN.DIR_TITLE:u"西游记25功满取经回",
           COLUMN.DIR_LINK:"url",
           COLUMN.DIR_FOLDER:u"data/西游记25功满取经回"
          }
    db.InsertRow(row)
    print db.GetRows(COLUMN.DIR_LINK + "='url'")
    

