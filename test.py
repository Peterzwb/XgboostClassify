# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 16:39:43 2018

@author: Administrator
"""

import boost
import tf_idf
import selectData


if __name__ == '__main__':
    data = selectData.clusData(varname="title" , tablename="qa_original_data")
    text = "我想知道该如何释放UIM卡异常状态"
    test = boost.boost(data)
    result_boost = test.getoriginData(text)
    for each in result_boost["match_sentence1"]:
        print(each)
    print("==================================================================")
    for each in result_boost["match_snetence2"]:
        print(each)
        
#    data = selectData.clusData(varname="title" , tablename="qa_original_data")
#    test_test = "CRM宽带资源的地址在哪里"
    result_idf = tf_idf.ifidf(data=data , text=text)
    print("==================================================================")
    for each in result_idf:
        print(each)
        
    for each in result_idf:
        if each in result_boost["match_snetence2"]:
            print(True)