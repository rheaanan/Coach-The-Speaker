# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 12:28:20 2018

@author: SHR
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 11:12:06 2018

@author: SHR
"""
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

def err_func(Y_actual, Y_pred):
    l = len(Y_actual)
    c = 0
    for i in range(l):
        diff = abs(Y_actual[i]-Y_pred[i])
        if(diff<=1):
            c+=1
    return c*100/l

balance_data = pd.read_csv(
'final_dataset_Averages_cleaned.csv', sep= ',')
#print(balance_data)
print ("Dataset Lenght:: ", len(balance_data))
print ("Dataset Shape:: ", balance_data.shape)
X = balance_data.values[:, 14].reshape(-1, 1)
y = balance_data.values[:,15]
y=y.astype('int')

devs=[]
errs=[]
accs=[]
my_split=0.2
for i in range(100):
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=my_split)


	#scaler = StandardScaler()

	# Fit on training set only.
	#scaler.fit(X_train)

	#X_train = scaler.transform(X_train)
	#X_test = scaler.transform(X_test)

	#PCA


	#pca = PCA(.95)
	#Fit PCA on training set. Note: you are fitting PCA on the training set only
	#pca.fit(X_train)

	#print("Number of components pca: ",pca.n_components_)

	#X_train = pca.transform(X_train)
	#X_test = pca.transform(X_test)


	
	svm_model_linear = SVC(kernel = 'linear', C = 1).fit(X_train, y_train)
	svm_predictions = svm_model_linear.predict(X_test)

	# model accuracy for X_test
	accuracy = svm_model_linear.score(X_test, y_test)

	# creating a confusion matrix
	cm = confusion_matrix(y_test, svm_predictions)

	predicted_list=list(zip(svm_predictions,y_test))
	cm = confusion_matrix(y_test, svm_predictions)
	rms= 0
	for a,b in predicted_list:
	    rms+=abs(a-b)
	dev = rms/len(predicted_list)
	err = err_func(y_test, svm_predictions)
	devs.append(dev)
	errs.append(err)
	accs.append(accuracy)
print("Accuracy",sum(accs)/len(accs))
print("Avg deviation",sum(devs)/len(devs))
print('Avg new accuracy', sum(errs)/len(errs))
'''
from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd

balance_data = pd.read_csv(
'final_dataset_Averages.csv', sep= ',')
print(balance_data)
print ("Dataset Length:: ", len(balance_data))
print ("Dataset Shape:: ", balance_data.shape)
X = balance_data.values[:, 14].reshape(-1, 1)
y = balance_data.values[:,15]
y=y.astype('int')
sum_accuracy = 0
sum_deviation = 0
acc_array = []
devi_arr = []
for i in range(0, 10):
	X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.3)
	from sklearn.svm import SVC
	svm_model_linear = SVC(kernel = 'linear', C = 1).fit(X_train, y_train)
	svm_predictions = svm_model_linear.predict(X_test)

	# model accuracy for X_test
	accuracy = svm_model_linear.score(X_test, y_test)

	# creating a confusion matrix
	cm = confusion_matrix(y_test, svm_predictions)

	predicted_list=list(zip(svm_predictions,y_test))
	cm = confusion_matrix(y_test, svm_predictions)
	rms= 0
	for a,b in predicted_list:
	    rms+=abs(a-b)

	
	devi = rms/len(predicted_list)
	sum_accuracy += accuracy
	sum_deviation += devi
	acc_array.append(accuracy)
	devi_arr.append(devi)
print("Accuracy array: ", acc_array)
print("deviation array: ", devi_arr)
print("Avg accuracy: ", sum_accuracy/10)   
print("Avg deviation ", sum_deviation/10)
'''