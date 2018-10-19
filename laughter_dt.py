import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
import pickle
from sklearn.externals import joblib
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
print(balance_data)
print ("Dataset Lenght:: ", len(balance_data))
print ("Dataset Shape:: ", balance_data.shape)
X = balance_data.values[:, 3].reshape(-1, 1)
Y = balance_data.values[:,15]
Y=Y.astype('int')
my_split=0.3
print(X)
devs=[]
accs=[]
errs=[]
max_acc_err=0
for i in range(100):
    X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size = my_split)
    clf_gini = DecisionTreeClassifier(criterion = "gini", random_state = 100, max_depth=3)
    clf_gini.fit(X_train, y_train)
    
    
    #print(clf_gini.predict([[11,48,0.007,0.129,0.008,0.006,0.85,1.05,8.41,18355.46,20199.77,19891.31,0.4036138363]]))
    
    y_pred = clf_gini.predict(X_test)
    predicted_list = list(zip(y_pred,y_test))
    rms= 0
    for a,b in predicted_list:
    	rms+=abs(a-b)
    dev = rms/len(predicted_list)
    devs.append(dev)
    acc = accuracy_score(y_test,y_pred)
    err=err_func(y_test,y_pred)
    accs.append(acc)
    errs.append(err)
    if err > max_acc_err:
        max_y_pred = y_pred
        joblib.dump(clf_gini,"laughter_dt_gini.pkl")
        max_acc_err = err
tree.export_graphviz(clf_gini,out_file="laughtertree_gini.dot")
#print("devs",devs)
#print("accuracies",accs)
print("Average dev:", sum(devs)/len(devs))
print("Average acc:", sum(accs)/len(accs))
print("Avg new Accuracy:", sum(errs)/len(errs))
print(max_acc_err)
print(max_y_pred)



'''import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
balance_data = pd.read_csv(
'final_dataset_Averages.csv', sep= ',')
#print(balance_data)
print ("Dataset Lenght:: ", len(balance_data))
print ("Dataset Shape:: ", balance_data.shape)
X = balance_data.values[:, 3].reshape(-1, 1)
Y = balance_data.values[:,15]
Y=Y.astype('int')
#print(X)
sum_accuracy = 0
sum_deviation = 0
acc_array = []
devi_arr = []
for i in range(0, 10):
	X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size = 0.2)
	clf_gini = DecisionTreeClassifier(criterion = "gini", random_state = 100,
	                               max_depth=3, min_samples_leaf=5)
	clf_gini.fit(X_train, y_train)
	clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100,
	 max_depth=3, min_samples_leaf=5)
	clf_entropy.fit(X_train, y_train)
	#print(clf_gini.predict([[11,48,0.007,0.129,0.008,0.006,0.85,1.05,8.41,18355.46,20199.77,19891.31,0.4036138363]]))
	y_pred = clf_gini.predict(X_test)
	predicted_list = list(zip(y_pred,y_test))
	rms= 0
	for a,b in predicted_list:
		rms+=abs(a-b)

	accuracy = accuracy_score(y_test,y_pred)
	devi = (rms/len(predicted_list))
	#print("final value: ", (rms/len(predicted_list)))
	#print ("Accuracy is ", accuracy_score(y_test,y_pred)*100)
	sum_accuracy += accuracy
	sum_deviation += devi
	acc_array.append(accuracy)
	devi_arr.append(devi)
print("Accuracy array: ", acc_array)
print("deviation array: ", devi_arr)
print("Avg accuracy: ", sum_accuracy/10)   
print("Avg deviation ", sum_deviation/10)
'''