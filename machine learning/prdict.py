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
df2 = pd.read_csv('/Device related/Smart TV.csv',index_col=[0],low_memory=False)

#difind labels
privilege_lebels = ['cvssV2_obtainOtherPrivilege', 'cvssV2_obtainAllPrivilege', 'cvssV2_obtainUserPrivilege']

metrics_lebels = ['cvssV2_confidentialityImpact', 'cvssV2_integrityImpact', 'cvssV2_availabilityImpact', 
                  'cvssV2_accessVector', 'cvssV2_accessComplexity', 'cvssV2_authentication']

#drop null data rows 
df = df.dropna(subset=privilege_lebels)
df = df.dropna(subset=metrics_lebels)

#difind input data
X_train = df['clean_description']
X_test =df2['clean_description']

#extract feature name from describtion
#N-gram with tf-idf
vectorizer = TfidfVectorizer(stop_words=['aka'], ngram_range=(1, 3), use_idf=False,
                               min_df=0.001, norm=None, smooth_idf=False, token_pattern=r'\S*[A-Za-z]\S+')
X_train_transformed = vectorizer.fit_transform(X_train)
X_test_transformed = vectorizer.transform(X_test)

#predict all privilege
y_allprivilege = df['cvssV2_obtainAllPrivilege']
le = preprocessing.LabelEncoder()
y_allprivilege = le.fit_transform(y_allprivilege)
ros = RandomOverSampler(random_state=42)
X_ros_train_allprivilege, y_ros_train_allprivilege = ros.fit_resample(X_train_transformed, y_allprivilege)
clf = LGBMClassifier(objective='binary', num_leaves=300, max_depth=500,
                     class_weight='balanced', random_state=42)
clf.fit(X_ros_train_allprivilege, y_ros_train_allprivilege)
y_pred_allprivilege = clf.predict(X_test_transformed)
obtainAllPrivilege = pd.DataFrame({'cvssV2_obtainAllPrivilege':y_pred_allprivilege},index = df2.index)

#predict OtherPrivilege
y_otherprivilege = df['cvssV2_obtainOtherPrivilege']
le = preprocessing.LabelEncoder()
y_otherprivilege = le.fit_transform(y_otherprivilege)
ros = RandomOverSampler(random_state=42)
X_ros_train_otherprivilege, y_ros_train_otherprivilege = ros.fit_resample(X_train_transformed, y_otherprivilege)
clf = LGBMClassifier(objective='binary', num_leaves=300, max_depth=500,
                     class_weight='balanced', random_state=42)
clf.fit(X_ros_train_otherprivilege, y_ros_train_otherprivilege)
y_pred_otherprivilege = clf.predict(X_test_transformed)
obtainOtherPrivilege = pd.DataFrame({'cvssV2_obtainOtherPrivilege':y_pred_otherprivilege},index = df2.index)

#predict UserPrivileg
y_Userprivilege = df['cvssV2_obtainUserPrivilege']
le = preprocessing.LabelEncoder()
y_Userprivilege = le.fit_transform(y_Userprivilege)
ros = RandomOverSampler(random_state=42)
X_ros_train_Userprivilege, y_ros_train_Userprivilege = ros.fit_resample(X_train_transformed, y_Userprivilege)
clf = LGBMClassifier(objective='binary', num_leaves=300, max_depth=500,
                     class_weight='balanced', random_state=42)
clf.fit(X_ros_train_Userprivilege, y_ros_train_Userprivilege)
y_pred_Userprivilege = clf.predict(X_test_transformed)
obtainUserPrivilege = pd.DataFrame({'cvssV2_obtainUserPrivilege':y_pred_Userprivilege},index = df2.index)

#predict confidentialityImpact
y_confidentiality = df['cvssV2_confidentialityImpact']
ros = RandomOverSampler(random_state=42)
X_ros_train_confidentiality, y_ros_train_confidentiality = ros.fit_resample(X_train_transformed, y_confidentiality)
clf = LGBMClassifier(objective='multiclass', num_leaves=200, max_depth=500,
                     class_weight='balanced', random_state=42)
clf.fit(X_ros_train_confidentiality, y_ros_train_confidentiality)
y_pred_confidentiality = clf.predict(X_test_transformed)
confidentialityImpact = pd.DataFrame({'cvssV2_confidentialityImpact':y_pred_confidentiality},index = df2.index)

#predict integrityImpact
y_integrity = df['cvssV2_integrityImpact']
ros = RandomOverSampler(random_state=42)
X_ros_train_integrity, y_ros_train_integrity = ros.fit_resample(X_train_transformed, y_integrity)
clf = LGBMClassifier(objective='multiclass', num_leaves=100, max_depth=500,
                     class_weight='balanced', random_state=42)
clf.fit(X_ros_train_integrity, y_ros_train_integrity)
y_pred_integrity = clf.predict(X_test_transformed)
integrityImpact = pd.DataFrame({'cvssV2_integrityImpact':y_pred_integrity},index = df2.index)

#predict availabilityImpact
y_availability = df['cvssV2_availabilityImpact']
ros = RandomOverSampler(random_state=42)
X_ros_train_availability, y_ros_train_availability = ros.fit_resample(X_train_transformed, y_availability)
clf = LGBMClassifier(objective='multiclass', num_leaves=100, max_depth=100,
                     class_weight='balanced', random_state=42)
clf.fit(X_ros_train_availability, y_ros_train_availability)
y_pred_availability = clf.predict(X_test_transformed)
availabilityImpact = pd.DataFrame({'cvssV2_availabilityImpact':y_pred_availability},index = df2.index)

#predict accessVector
y_accessVector = df['cvssV2_accessVector']
ros = RandomOverSampler(random_state=42)
X_ros_train_accessVector, y_ros_train_accessVector = ros.fit_resample(X_train_transformed, y_accessVector)
clf = LGBMClassifier(objective='multiclass', num_leaves=200, max_depth=500,
                     class_weight='balanced', random_state=42)
clf.fit(X_ros_train_accessVector, y_ros_train_accessVector)
y_pred_accessVector = clf.predict(X_test_transformed)
accessVector = pd.DataFrame({'cvssV2_accessVector':y_pred_accessVector},index = df2.index)

#predict accessComplexity
y_Complexity = df['cvssV2_accessComplexity']
ros = RandomOverSampler(random_state=42)
X_ros_train_Complexity, y_ros_train_Complexity = ros.fit_resample(X_train_transformed, y_Complexity)
clf = LGBMClassifier(objective='multiclass', num_leaves=300, max_depth=500,
                     class_weight='balanced', random_state=42)
clf.fit(X_ros_train_Complexity, y_ros_train_Complexity)
y_pred_Complexity = clf.predict(X_test_transformed)
accessComplexity = pd.DataFrame({'cvssV2_accessComplexity':y_pred_Complexity},index = df2.index)

#predict authentication
y_authentication = df['cvssV2_authentication']
ros = RandomOverSampler(random_state=42)
X_ros_train_authentication, y_ros_train_authentication = ros.fit_resample(X_train_transformed, y_authentication)
clf = LGBMClassifier(objective='multiclass', num_leaves=300, max_depth=500,
                     class_weight='balanced', random_state=42)
clf.fit(X_ros_train_authentication, y_ros_train_authentication)
y_pred_authentication = clf.predict(X_test_transformed)
authentication = pd.DataFrame({'cvssV2_authentication':y_pred_authentication},index = df2.index)

#concat all result
pred_result = pd.concat([confidentialityImpact,integrityImpact,availabilityImpact,accessVector,accessComplexity,authentication,
                   obtainOtherPrivilege,obtainAllPrivilege,obtainUserPrivilege], axis=1)
            
pred_result['cvssV2_obtainOtherPrivilege'].replace({0: "FALSE", 1: "TRUE"}, inplace=True)
pred_result['cvssV2_obtainAllPrivilege'].replace({0: "FALSE", 1: "TRUE"}, inplace=True)
pred_result['cvssV2_obtainUserPrivilege'].replace({0: "FALSE", 1: "TRUE"}, inplace=True)

#The base equation (formula version 2.10) 
AccessVector = pred_result['cvssV2_accessVector'].replace({'LOCAL': 0.395, 'NETWORK': 1.0, 'ADJACENT_NETWORK':0.646})
AccessComplexity =  pred_result['cvssV2_accessComplexity'].replace({'HIGH': 0.35, 'MEDIUM': 0.61, 'LOW': 0.71})
Authentication = pred_result['cvssV2_authentication'].replace({'NONE': 0.704, 'SINGLE': 0.56, 'MULTIPLE': 0.45})
ConfImpact = pred_result['cvssV2_confidentialityImpact'].replace({'PARTIAL': 0.275, 'NONE': 0.0, 'COMPLETE': 0.660})
IntegImpact = pred_result['cvssV2_integrityImpact'].replace({'PARTIAL': 0.275, 'NONE': 0.0, 'COMPLETE': 0.660})
AvailImpact = pred_result['cvssV2_availabilityImpact'].replace({'PARTIAL': 0.275, 'NONE': 0.0, 'COMPLETE': 0.660})

#Impact = 10.41*(1-(1-ConfImpact)*(1-IntegImpact)*(1-AvailImpact))
#Exploitability = 20* AccessVector*AccessComplexity*Authentication
Impact = []
Exploitability = []
for index in pred_result.index:
    Imp = 10.41*(1-(1-ConfImpact[index])*(1-IntegImpact[index])*(1-AvailImpact[index]))
    Exp = 20* AccessVector[index]*AccessComplexity[index]*Authentication[index]
    Impact.append(Imp)
    Exploitability.append(Exp)

#BaseScore = round_to_1_decimal(((0.6*Impact)+(0.4*Exploitability)-1.5)*f(Impact))
#f(impact)= 0 if Impact=0, 1.176 otherwise
BaseScore = []
for n in range(len(Impact)):
    if Impact[n] == 0:
        Score= round(((0.6*Impact[n])+(0.4*Exploitability[n])-1.5)*0,1)
        BaseScore.append(Score)
    else: 
        Score= round(((0.6*Impact[n])+(0.4*Exploitability[n])-1.5)*1.176,1)
        BaseScore.append(Score)

#append base score with output
bs=pd.DataFrame({'ImpactScore':np.round(Impact, 1),'ExploitabilityScore':np.round(Exploitability, 1),'BaseScore':BaseScore,},index = pred_result.index)
result = pd.concat([pred_result,bs], axis=1)

drop = df2.drop(['cvssV2_version','cvssV2_vectorString','cvssV2_accessVector', 'cvssV2_accessComplexity', 'cvssV2_authentication', 
          'cvssV2_confidentialityImpact', 'cvssV2_integrityImpact', 'cvssV2_availabilityImpact','cvssV2_baseScore',
          'cvssV2_severity','cvssV2_exploitabilityScore','cvssV2_impactScore','cvssV2_obtainAllPrivilege','cvssV2_obtainUserPrivilege',
         'cvssV2_obtainOtherPrivilege','cvssV2_userInteractionRequired','cvssV3_version','cvssV3_vectorString','cvssV3_attackVector', 'cvssV3_attackComplexity', 'cvssV3_privilegesRequired', 
          'cvssV3_confidentialityImpact', 'cvssV3_integrityImpact', 'cvssV3_availabilityImpact','cvssV3_baseScore',
          'cvssV3_userInteraction','cvssV3_scope','cvssV3_impactScore','cvssV3_baseSeverity','cvssV3_exploitabilityScore',
         'cvssV3_impactScore','cvssV2_acInsufInfo'], axis = 1) 
final_result = pd.concat([drop,result], axis=1)
final_result.to_csv("/predicted result/Smart TV.csv",index = False)