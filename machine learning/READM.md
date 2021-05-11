# Machine learing
## 1. Data processing 
The training data set: 
<img width="943" alt="Screen Shot 2021-02-09 at 9 30 40 pm" src="https://user-images.githubusercontent.com/74897092/107354841-951f9d00-6b1e-11eb-9fe0-b8b6a50fbaf8.png">

It can be observed from graphs above, this is imbalance dataset. So, we use random over-sampling to deal with data set. Method: RandomOverSampler(generate new samples in the minority classes by randomly sampling with replacement of the currently available samples).

The distribution of each class after over-sampling shows in under graphs.
<img width="857" alt="Screen Shot 2021-02-09 at 9 38 32 pm" src="https://user-images.githubusercontent.com/74897092/107355376-49212800-6b1f-11eb-9638-d8b9dd204745.png">

N-gram with tf-idf is useed in this text convert.

we Split 80% the data into training, 10% validation for cross validation and 10% testing set for evaluation 

## 2. Tune Model
In our project, we need to predict six elements of CVSS base score (Confidentiality, Integrity, Availability, AccessVector, AccessVector, AccessComplexity, Authentication) and three types of privileges (AllPrivilege, OtherPrivilege, UserPrivilege). It can be seen from graphs that privileges as Binary classification, and the elements are Multi-class classification, so here we should tune them to separate with same model (LGBM) and different objective.

For Privilege: clf = LGBMClassifier(objective='binary', random_state=42)
For Elements: clf = LGBMClassifier(objective='multiclass',  random_state=42)
tune two hyperparameters ('num_leaves', 'max_depth') in LGBM model. 
‘num_leaves’ is the main parameter to control the complexity of the tree models, as well as the larger value for better accuracy.
But if the value is too large, it might cause the over-fitting. Hence, here we also should be tuning the ‘max_depth’ to limit the tree depth explicitly and to avoid the overfitting. 
Theoretically, the value of 'num_leaves’ is smaller than 2^(max_depth) that could avoid overfitting. 
First, we set range for each hyperparameters as table below.
<img width="937" alt="Screen Shot 2021-02-09 at 9 11 39 pm" src="https://user-images.githubusercontent.com/74897092/107356278-833ef980-6b20-11eb-83c7-3c8e8fb1e035.png">

Use grid search to try out every possible combination of hyperparameters.
<img width="884" alt="Screen Shot 2021-02-09 at 9 11 58 pm" src="https://user-images.githubusercontent.com/74897092/107356699-0bbd9a00-6b21-11eb-9697-b14bacaf9fe5.png">
<img width="886" alt="Screen Shot 2021-02-09 at 9 12 15 pm" src="https://user-images.githubusercontent.com/74897092/107356855-41628300-6b21-11eb-9ea8-2d943163a1cc.png">

## 3. Evaluation
Input test data set to evaluation

<img width="677" alt="Screen Shot 2021-02-09 at 9 12 27 pm" src="https://user-images.githubusercontent.com/74897092/107357185-a6b67400-6b21-11eb-84b9-46c833042f53.png">

## 4. Predict result 
Enter the hyperparameter of the best score of each label to  predict the vulnerabilities of IoT systems.
