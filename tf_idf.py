# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 16:55:24 2018

@author: Administrator
"""

import jieba
from gensim import corpora,models,similarities
#import getData 
import Clustering
import selectData
import os

#获得原数据（已分词，去停词，加语料
#data = selectData.clusData(varname="title" , tablename="qa_original_data")
def trainData(data):
    path = os.getcwd() 
    class1 = Clustering.cluster(path)
    data_seg = class1.preTreating(inptdata= data)
    for i in range(0 , len(data_seg)):
        data_seg[i] = data_seg[i].split(" ")
    return data_seg

def textInput(text):
#test_test = "CRM宽带资源的地址在哪里"
    path = os.getcwd() 
    class1 = Clustering.cluster(path)
    sentence = class1.preTreating(inptdata= text)
    sentence = sentence[0].split(" ")
    return sentence

def ifidf(data , text):
    data_seg = trainData(data)
    sentence = textInput(text)
    dictionary = corpora.Dictionary(data_seg)#这就是一个词袋，就是以序号为键以单词为值的字典    
    corpus = [dictionary.doc2bow(doc) for doc in data_seg]#编号、频次
    test_corpus = dictionary.doc2bow(sentence)#测试句子的词表示
    tfidf = models.TfidfModel(corpus)
#tfidf[test_corpus]#词tiidf值
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
    sim = index[tfidf[test_corpus]]
    classify = list(zip(data , sim))
#    sim
    score = sorted(classify, key=lambda item: -item[1])
#    print(score)
    result = []
    for each in score:
        if each[1] != 0:
            result.append(each[0])
    return result
    
if __name__ == '__main__':
    data = selectData.clusData(varname="title" , tablename="qa_original_data")
    test_test = "CRM宽带资源的地址在哪里"
    result = ifidf(data=data , text=test_test)
    
    
    