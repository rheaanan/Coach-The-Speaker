import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from numpy import array
from sklearn.externals import joblib
def predict_value(video_values):
	'''
	balance_data = pd.read_csv(
	'final_dataset_Averages_cleaned.csv', sep= ',')
	#print(balance_data)
	print ("Dataset Lenght:: ", len(balance_data))
	print ("Dataset Shape:: ", balance_data.shape)
	X = balance_data.values[:, 9].reshape(-1, 1)
	Y = balance_data.values[:,15]
	Y=Y.astype('int')
	#print(X)
	X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size = 0.3, random_state = 100)
	clf_gini = DecisionTreeClassifier(criterion = "gini", random_state = 100,
	                               max_depth=3, min_samples_leaf=5)
	clf_gini.fit(X_train, y_train)
	clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100, max_depth=3, min_samples_leaf=5)
	clf_entropy.fit(X_train, y_train)
	
	'''
	#print(clf_gini.predict([[11,48,0.007,0.129,0.008,0.006,0.85,1.05,8.41,18355.46,20199.77,19891.31,0.4036138363]]))
	vid_numpy = array(video_values[9]).reshape(-1, 1)
	#print(vid_numpy)
	clf_gini = joblib.load("main_model_dt_gini.pkl")
	y_pred = clf_gini.predict(vid_numpy)
	print(y_pred[0])
	return y_pred[0]

#predict_value(['name', 'id', 11,48,0.007,0.129,0.008,0.006,0.85,1.05,8.41,18355.46,20199.77,19891.31,0.4036138363, 'rq'])
