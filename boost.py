# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 10:00:52 2018

@author: Administrator
"""

import xgboost as xgb
import os
import selectData
import Clustering
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import accuracy_score

class boost:
   
    def __init__(self , data):
        path = os.getcwd() 
        class1 = Clustering.cluster(path)
        result = class1.kmeans(data=data)
        self.clus_result = result[0]
        self.weight = result[1]
        self.tfidf_model = result[2:5]
        self.class1 = class1
    
    def trainData(self):       
        content = []
        label = []
        for each in self.clus_result:
            content.append(each[0])
            label.append(each[2])
        train_data = [content , label]
        return train_data
    
    def train(self):
        train_data = self.trainData()
        X = train_data[0]
        Y = np.array(train_data[1])
        dtrain = xgb.DMatrix(self.weight, label=Y)
        param = {'max_depth':6, 'eta':0.5, 'eval_metric':'merror', 'silent':1, 'objective':'multi:softmax', 'num_class':20}
        num_round = 100 
        bst = xgb.train(param, dtrain, num_round)
        train_preds = bst.predict(dtrain)
        train_accuracy = accuracy_score(train_preds, dtrain.get_label())#95%
        print(train_accuracy)
        result = [train_preds , bst]
        return result

    def predict(self,text):
        train_res = self.train()   
        bst = train_res[1]
        train_answer = train_res[0]
        #text = "我想知道该如何释放UIM卡异常状态"
        text = self.class1.preTreating(text)
        test_tfidf = self.tfidf_model[1].transform(self.tfidf_model[0].transform(text))
        test_weight = test_tfidf.toarray()
        dtest = xgb.DMatrix(test_weight) 
        answer = bst.predict(dtest)#第19类
        result = [answer , train_answer]
        return result
        
    def getoriginData(self,text):
        result = {"sentence":None,
                  "sentencelabe":None,
                  "match_sentence1":None,
                  "match_snetence2":None}
        predict_res = self.predict(text)
        answer = predict_res[0]
        predictdata = predict_res[1]
        origindata = self.clus_result
#        print(origindata)
        originsen = []
        for each in origindata:
            originsen.append(each[1])
        boost_answer = list(zip(originsen , predictdata))
#        print(boost_answer)
        match1 = []
        for each in boost_answer:
            if each[1] == answer:
                match1.append(each[0])
        match2 = []
        for each in origindata:
            if each[2] == answer:
                match2.append(each[1])
        result["sentence"] = text
        result["sentencelabe"] = int(answer)
        result["match_sentence1"] = match1
        result["match_snetence2"] = match2
        return result

if __name__ == '__main__':
    data = selectData.clusData(varname="title" , tablename="qa_original_data")
    text = "我想知道该如何释放UIM卡异常状态"
    test = boost(data)
    result = test.getoriginData(text)
    for each in result["match_sentence1"]:
        print(each)
    print("==================================================================")
    for each in result["match_snetence2"]:
        print(each)