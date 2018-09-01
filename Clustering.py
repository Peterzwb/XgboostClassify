# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 15:19:05 2018

@author: Administrator
"""

import selectData
#import getTool
import jieba
import os        
import re          
import codecs
import shutil
import numpy as np
from sklearn.cluster import KMeans
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer 

#pathname = os.path.dirname(os.path.abspath(__file__))
#print(pathname)

class cluster:
#    path = os.getcwd()
#    path_dict = path + "\\tool\\dict.txt"
#    path_stopwords = path + "\\tool\\stop_word.txt"
    def __init__(self , path):
#        self.data = data
        self.path = path
        self.path_dict = path + "\\tool\\dict.txt"
        self.path_stopwords = path + "\\tool\\stop_word.txt"
#        jieba.load_userdict(path_dict)

#data = selectData.clusData(varname="title" , tablename="qa_original_data")
#tool = getTool.getData()
#data_try2 = tool.pretreatment(2)


    def preTreating(self,inptdata):
        sen = []
        jieba.load_userdict(self.path_dict)
        stopwords = codecs.open(self.path_stopwords,'r').readlines()
        stopwords = [ w.strip() for w in stopwords]
        data = inptdata
        if type(data) == list:
#            jieba.load_userdict(self.path_dict)
#            stopwords = codecs.open(self.path_stopwords,'r').readlines()
#            stopwords = [ w.strip() for w in stopwords]
            for i in range(0,len(data)):
                seg = jieba.cut_for_search(data[i].lower() , HMM = False)
                seg = " ".join(seg)
                seg = seg.split(" ")
        #        print(seg)
                words = [w for w in seg if w not in stopwords]
                words = " ".join(words)
                sen.append(words)
        elif type(data) == str:
            seg = jieba.cut_for_search(data.lower() , HMM = False)
            seg = " ".join(seg)
            seg = seg.split(" ")
    #        print(seg)
            words = [w for w in seg if w not in stopwords]
            words = " ".join(words)
            sen.append(words)
    #    sen = "\n".join(sen) 
        return sen
    #获得加入新词的分好词，去停用词，分为一行一句话的列表

    def tfidf(self,data):
        data_try = self.preTreating(inptdata= data)
        
        #将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频       
        vectorizer = CountVectorizer()
        #该类会统计每个词语的tf-idf权值
        transformer = TfidfTransformer()
        vectorizer.fit_transform(data_try)
        transformer.fit_transform(vectorizer.fit_transform(data_try))
        tfidf = transformer.fit_transform(vectorizer.fit_transform(data_try))
        #获取词袋模型中的所有词语  
        word = vectorizer.get_feature_names()
        #将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
        weight = tfidf.toarray()
        return weight , data_try , vectorizer , transformer
        
    #开始k-means
    def kmeans(self,data):
        weight,data_seg,vectorizer,transformer = self.tfidf(data)
        clf = KMeans(n_clusters=20)   #景区 动物 人物 国家
        result = clf.fit(weight)
        label = result.labels_
    #    print(len(result.labels_))
        data_label = zip(data_seg , data , label.tolist())
        result_data = list(data_label)
        result = [result_data, weight , vectorizer , transformer]
#        return result_data , weight , vectorizer , transformer
        return result

    

if __name__ == '__main__':
    path = os.getcwd()    
    data = selectData.clusData(varname="title" , tablename="qa_original_data")
    class1 = cluster(path)
    result = class1.kmeans(data=data)