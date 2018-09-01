# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 15:24:16 2018

@author: Administrator
"""
from LightMysql import LightMysql
import jieba
       

def getData(varname , tablename):
    str1 = " " + varname + " "
    str2 = tablename + " "
    # 配置信息，其中host, port, user, passwd, db为必需
    dbconfig = {'host':'127.0.0.1',
                'port': 3306,
                'user':'root',
                'passwd':'root',
                'db':'guangxi',
                'charset':'utf8'}
    result = None
    try:
        QUERY_ALL_ALARMOBJET = " SELECT"
        QUERY_ALL_ALARMOBJET += str1
        QUERY_ALL_ALARMOBJET += " FROM " + str2;
#        QUERY_ALL_ALARMOBJET += " WHERE 1=1 and status=1 "
#        QUERY_ALL_ALARMOBJET += " and y= " + str(type)
        db = LightMysql(dbconfig)  # 创建LightMysql对象，若连接超时，会自动重连
        sql_select = QUERY_ALL_ALARMOBJET
#         print(sql_select)
        result, colmun = db.query(sql_select, 'all')  # 返回有多少行
    except Exception as e:
        logging.error(e)
    finally:
        if(db != None):
            db.close()  # 操作结束，关闭对象
    return result
    
def clusData(varname , tablename):
    data = getData(varname , tablename)
    sentence = []
    for sen in data:
        sentence.append(sen[0])
#    print(sentence)
#    sentence = "\n".join(sentence)
    return sentence
    
    
    
if __name__ == '__main__':
    data = clusData(varname="title" , tablename="qa_original_data")