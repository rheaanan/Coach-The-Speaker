import numpy as np
from sklearn import svm
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def train_test(training_data, testing_data, result_file):
	data = np.array(list(csv.reader(open(training_data))))
	
	act_target = data[:,1]
	text = data[:,0]



	spam_t = np.where(act_target==" question", 1,-1)

	#target is ready. We need to restructure the text now into features.
	count_vect = CountVectorizer()
	X_train_counts = count_vect.fit_transform(text)
	#print(count_vect.get_feature_names())


	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
	#print(X_train_tfidf)


	#Train
	clf = svm.SVC(kernel='linear', C=5)
	clf.fit(X_train_tfidf,spam_t)

	#New Instance
	new_file = np.array(list(csv.reader(open(testing_data))))

	test_text = new_file[:,0]
	#actual_value = new_file[:,1]
	#av = np.where(actual_value==" question", 1,-1)

	X_new_counts = count_vect.transform(test_text)
	X_new_tfidf = tfidf_transformer.transform(X_new_counts)

	predicted = clf.predict(X_new_tfidf)
	
	total = len(new_file)
	res_file = open(result_file, "w")
	for i in range(total):
		av_i = new_file[i,0]
		#print(av_i, ",", predicted[i])
		d = av_i+ ","+str(predicted[i])+"\n"
		res_file.write(d)
	res_file.close()

#train_test("training_data2.csv", "test2.csv", "new_res.csv")

