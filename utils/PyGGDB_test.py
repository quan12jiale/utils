# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 09:04:24 2020

@author: quan1
"""
import os
import PyGGDB as GGDB

DBField = GGDB.DBField
DBRecord = GGDB.DBRecord
DBTable = GGDB.DBTable
Database = GGDB.Database
FileMode = GGDB.FileMode

"""
该脚本主要用于新添加构件时，
自动化更新ModelInfo.GDB的ElementPropertyDict表。
SyslInfo.GDB的ActionLayer、ElementVisibleSetting表。
UserInfo.GDB的ElementVisibleSetting表，
这张表的第6个字段是自增字段，因此84行应该改为for j in range(nFieldCount - 2)
"""

def updatedbfield(dboldrecord: GGDB.DBRecord, dbfield: GGDB.DBField,
                  dbnewrecord: GGDB.DBRecord):
    ftype = dbfield.Type()
    fieldName = dbfield.Name()
    if fieldName == "ElementTypeID":
        return dbfield.SetInt64(dbnewrecord, 1300)
    
    if (ftype == GGDB.FIELDTYPE_INT) or (ftype == GGDB.FIELDTYPE_ID):
        fvalue = dbfield.GetInteger(dboldrecord)
        return dbfield.SetInteger(dbnewrecord, fvalue)
    
    elif ftype == GGDB.FIELDTYPE_INT64:
        fvalue = dbfield.GetInt64(dboldrecord)
        return dbfield.SetInt64(dbnewrecord, fvalue)
    
    elif ftype == GGDB.FIELDTYPE_DOUBLE:
        fvalue = dbfield.GetDouble(dboldrecord)
        return dbfield.SetDouble(dbnewrecord, fvalue)
    
    elif ftype == GGDB.FIELDTYPE_BOOL:
        fvalue = dbfield.GetBool(dboldrecord)
        if isinstance(fvalue, str):
            if fvalue.isdigit():
                fvalue = (int(fvalue, 10) != 0)
            else:
                fvalue = (fvalue and (fvalue.lower() == "true"))
        return dbfield.SetBool(dbnewrecord, True if fvalue else False)
    
    elif ftype == GGDB.FIELDTYPE_MEMO:
        fvalue = dbfield.GetString(dboldrecord)
        return dbfield.SetString(dbnewrecord, fvalue)
    return False

def dbadd(db : GGDB.Database, tablename : str) -> bool:
    """
    dbtable : GGDB.Database
    """
    dbtable = db.GetTable(tablename)
    if not dbtable:
        return False
    
    addrList = GGDB.FileAddressList()
    strQuery = "ElementTypeID == 19"
    bQueryOk = dbtable.Query(strQuery, addrList)
    if bQueryOk == False:
        return False
    # 记录条数
    nRecordCount = addrList.Count
    # 字段个数
    nFieldCount = dbtable.FieldCount()
    for j in range(nFieldCount - 1):
        dbfield = dbtable.GetField(j + 1)
        fieldName = dbfield.Name()
        print("第{}个字段：{}".format((j + 1), fieldName))
    for i in range(nRecordCount):
        dboldrecord = dbtable.CreateRecordMap(addrList.GetItem(i))
        
        rAddr = dbtable.NewRecord()
        dbnewrecord = dbtable.CreateRecordMap(rAddr)
        # 第一个字段是 ~%@InnerID@%
        for j in range(nFieldCount - 2):
            dbfield = dbtable.GetField(j + 1)
            if not updatedbfield(dboldrecord, dbfield, dbnewrecord):
                dbtable.DeleteRecord(rAddr)
                return False
            
        # 添加记录
        if not dbtable.AddRecord(rAddr):
            return False
    print("{} nRecordCount = {}".format(tablename, nRecordCount))
    print("{} nFieldCount = {}".format(tablename, nFieldCount))
    print("Success Add")
    return True


class Amd:
    """
    add
    modify
    delete
    """
    def __init__(self):
        self.db = GGDB.Database(256)

    def __del__(self):
        self.close_db()
    
    def open_db(self, dbpath : str, tablename : str):
        if not os.access(dbpath, os.F_OK | os.W_OK):
            return
        if not self.db.Open(dbpath, None, GGDB.NORMAL):
            return
        
        self.db.BeginPauseCmdLog()
        self.db.BeginEdit()
        try:
            if not dbadd(self.db, tablename):
                self.db.Rollback()
        except UnicodeDecodeError as error:
            self.db.Rollback()
            print("UnicodeDecodeError: {}".format(error))
        except Exception as error:
            self.db.Rollback()
            print(error)
        finally:
            self.db.EndEdit("", "")
            self.db.EndPauseCmdLog()
    
    def close_db(self):
        if self.db.IsOpen():
            self.db.Close()


def main():
    dbpath = r"F:\GTJ\resource\GTJ\UserInfo.GDB"
    tablename = "ElementVisibleSetting"
    obj = Amd()
    obj.open_db(dbpath, tablename)

    
if __name__ == '__main__':
    main()
