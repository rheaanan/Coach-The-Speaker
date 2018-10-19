from wit import Wit
import os
access_token = 'GL472M2BHX4W2FSNNH4DN376P4YHJP25'
client = Wit(access_token)
resp = None


def RecognizeSpeech(AUDIO_FILENAME):
	res_file = open("res_file_question.csv", "a")
	audio_file = open(AUDIO_FILENAME, 'rb') 
	try:
		resp = client.speech(audio_file, None, {'Content-Type': 'audio/wav'})
		res_file.write(str(resp['_text'])+ ","+ AUDIO_FILENAME +' response'+'\n')
	except:
		print("Could not translate: ", AUDIO_FILENAME)




def speech_to_text(dir_name):
	print("WORKING ON DIRECTORY: ", dir_name)
	file_list = os.listdir(dir_name)
	total_len = len(file_list)
	os.chdir(dir_name)
	
	count = 1

	for my_file in file_list:
		print("Working on....."+my_file)
		text =  RecognizeSpeech(my_file)		
		print("Completed file no "+str(count)+"/"+str(total_len))
		count = count + 1
	os.chdir("..")

