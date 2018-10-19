import numpy as np
import csv
def list_sentences(file_name, res_file):
	file_data = np.array(list(csv.reader(open(file_name))))
	#print(file_data)
	chunk = file_data[:,0]
	classification = file_data[:,1]
	l = len(classification)
	res_file = open(res_file, "a")
	for i in range(0,l):
		if(classification[i]=="1"):
			#print(chunk[i])
			d = chunk[i] +":"+"\n"

			res_file.write(d)
	res_file.close()
	

#list_sentences("svm_results.txt", "questions_try.txt")
