# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 19:01:24 2015

@author: Laetitia
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

N=10 #Number of intervals for X and Y coordinates. The number of regions is: N**2

def parse_date(date):
    d=datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
    year=d.year
    month=d.month
    day=d.day
    hour=d.hour
    return year, month, day, hour

def get_min_max_wo_outliers(train, test):
    df=pd.concat([train,test],axis=0,ignore_index=True)
    df=df[(df['X']<-122) & (df['Y']<50)]
    idx_min_X, idx_max_X, idx_min_Y, idx_max_Y=df['X'].idxmin(), df['X'].idxmax(), df['Y'].idxmin(), df['Y'].idxmax()
    min_X, max_X, min_Y, max_Y=df['X'][idx_min_X], df['X'][idx_max_X], df['Y'][idx_min_Y], df['Y'][idx_max_Y]
    return min_X, max_X, min_Y, max_Y

def intervals(X,Y):
    ind_X = np.floor((X - min_X) / len_int_X)
    ind_Y = np.floor((Y - min_Y) / len_int_Y)
    return ind_X*N+ind_Y

def get_features(df):
    print "Parsing date"
    df['year'], df['month'], df['day'], df['hour']=zip(*df['Dates'].apply(parse_date))
    
    print "Creating regions of SF"   
    df['region']=intervals(df['X'],df['Y'])
    
    dummies_region=pd.get_dummies(df['region'])
    dummies_pddistrict=pd.get_dummies(df['PdDistrict'])
    dummies_dayofweek=pd.get_dummies(df['DayOfWeek'])
    
    features=pd.concat([dummies_pddistrict,dummies_dayofweek,df.loc[:,'year':'hour'],dummies_region], axis=1)
    return features

def get_labels(df):
    #dummies_category=pd.get_dummies(train_df['Category'])
    target=df['Category']
    return target
    
train_df=pd.read_csv("train.csv")
test_df=pd.read_csv("test.csv")

min_X, max_X, min_Y, max_Y = get_min_max_wo_outliers(train_df, test_df)
len_int_X=(max_X - min_X)/N
len_int_Y=(max_Y - min_Y)/N

train_features=get_features(train_df)
train_labels=get_labels(train_df)

test_features=get_features(test_df)

train_features[110]=0

print "Fitting model"
clf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=10),
                         n_estimators=50)
clf.fit(train_features, train_labels)

print "Predicting test categories"
test_pred_proba=pd.DataFrame(clf.predict_proba(test_features),columns=clf.classes_)

print "Saving csv file"
test_pred_proba.index.name='Id'
test_pred_proba.to_csv(path_or_buf="test_pred.csv")