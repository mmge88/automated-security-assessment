#loading library
import pandas as pd
import numpy as np
from lightgbm import LGBMClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn import preprocessing
import time
from collections import Counter
from sklearn.datasets import make_classification
from imblearn.over_sampling import RandomOverSampler

#loading file
# 'all_clean.csv' download from 'https://drive.google.com/file/d/1CvWDTGYrirHTlG4HBJzTlQc6gAb79yqH/view?usp=sharing'
df = pd.read_csv('all_clean.csv',index_col=[0],low_memory=False)

#difind labels
privilege_lebels = ['cvssV2_obtainOtherPrivilege', 'cvssV2_obtainAllPrivilege', 'cvssV2_obtainUserPrivilege']

metrics_lebels = ['cvssV2_confidentialityImpact', 'cvssV2_integrityImpact', 'cvssV2_availabilityImpact', 
                  'cvssV2_accessVector', 'cvssV2_accessComplexity', 'cvssV2_authentication']

#drop null data rows 
df = df.dropna(subset=privilege_lebels)
df = df.dropna(subset=metrics_lebels)

#difind input data
X = df['clean_description']

#extract feature name from describtion
def extract_feature(X):
    #N-gram with tf-idf
    vectorizer = TfidfVectorizer(stop_words=['aka'], ngram_range=(1, 3), use_idf=False,
                               min_df=0.001, norm=None, smooth_idf=False, token_pattern=r'\S*[A-Za-z]\S+')


    X_transformed = vectorizer.fit_transform(X)

    
    return  X_transformed

def datapreproces(X_transformed, y):
    
    #oversmapling to deal with imbalance dataset
    ros = RandomOverSampler(random_state=42)
    X_res, y_res = ros.fit_resample(X_transformed, y)
    
    x_train, x_test, y_train, y_test = train_test_split(X_res, y_res,test_size=0.2,shuffle=True,random_state=42)
    x_test, x_val, y_test, y_val = train_test_split(x_test, y_test,test_size=0.5,shuffle=True,random_state=42)

    return x_train, x_test, x_val, y_test, y_train, y_val

#the function for model tuning
def modeltuning(x_val,y_val):
    clf = LGBMClassifier(objective='multiclass', random_state=42)
    distributions = {'num_leaves':[100,300,500],
                     'max_depth':[100,200,300]
                    }
    #random search 
    search = GridSearchCV(clf, distributions,scoring='f1_weighted')
    search.fit(x_val,y_val)
    return search.cv_results_, search.best_params_

#evaluation for element of base score
def model_metric(x_train, x_test, y_train, y_test, numleaves, maxdepth):
    clf = LGBMClassifier(num_leaves=numleaves, max_depth=maxdepth, objective='multiclass', random_state=42)
    clf.fit(x_train,y_train)
    y_pred = clf.predict(x_test)

    return accuracy_score(y_test, y_pred), f1_score(y_test, y_pred, average='macro',zero_division=0),\
           f1_score(y_test, y_pred, average='weighted',zero_division=0),precision_score(y_test, y_pred, average='macro',zero_division=0),\
           precision_score(y_test, y_pred, average='weighted',zero_division=0),recall_score(y_test, y_pred, average='macro',zero_division=0),\
           recall_score(y_test, y_pred, average='weighted',zero_division=0)

#svae the result to txt file and csv
params = open("best_params_under.txt", "a")
for label in metrics_lebels:
    start_time = time.time()
    y = df[label]
    #calling extract_feature function
    X_transformed = extract_feature(X)
   
    x_train, x_test, x_val, y_test, y_train, y_val = datapreproces(X_transformed, y)
   
    history, best_params = modeltuning(x_val,y_val)
    numleaves,maxdepth= best_params['num_leaves'],best_params['max_depth']
    
    acc_score,f1_1,f1_2,p1,p2,r1,r2 = model_metric(x_train, x_test, y_train, y_test, numleaves, maxdepth)
    random_search_history = pd.DataFrame(history)

    random_search_history.to_csv('%s_under.csv' % label)
    params.write(label + '--- %s seconds ---' % (time.time() - start_time) + '\n' + str(best_params) + '\taccuracy score: ' +  str(acc_score) + '\tf1_score(macro): ' + str(f1_1) +
                '\tf1_score(weight): ' + str(f1_2) + '\tprecision_score(macro)'+ str(p1) + '\tprecision_score(weighted)' + str(p2) + 'recall_score(macro): '
                + str(r1) + '\trecall_score(weighted): ' + str(r2) + '')
    params.write("\n\n")
params.close()