def search_for_relvant_questions(keyword_file, questions_file, res_file, video_file):
	keyword_list = [line.rstrip('\n') for line in open(keyword_file)]
	question_list = [line.rstrip('\n') for line in open(questions_file)]
	#print(keyword_list)
	#print(question_file[3])
	no_of_rel_questions = 0
	no_of_questions = len(question_list)
	print("No of questions are: ", no_of_questions)
	for keyword in keyword_list:
		for question in question_list:
			if keyword in question:
				#print(keyword , "*", question)
				question_list.remove(question) #So that if mutiple words are contained in the same question it is counted only once
				no_of_rel_questions += 1
	print("No of relevant questions are: ", no_of_rel_questions)
	res_file = open(res_file, "a")
	r = [no_of_questions, no_of_rel_questions]
	d = video_file+","+str(no_of_questions)+","+str(no_of_rel_questions)+"\n"
	
	res_file.write(d)
	res_file.close()
	return r
#search_for_relvant_questions("trial_keywords","questions")
