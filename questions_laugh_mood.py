import moviepy.editor as mp
from pydub import AudioSegment
import os
import vad as vd
import wit_speech_to_text as wst
import sys
import time
import svm_on_new_file as questions_svm
import list_all_classfied_sentences as list_sen
import search_for_relavant_questions as srq
import shutil
import split_audio as sa
import remove_space as rs
from OpenVokaturi.examples.voka_one_file import detect_emotion

def convert_to_mp3(in_path, file_name,out_path):
	print(os.getcwd())
	clip = mp.VideoFileClip(in_path+'/'+file_name).subclip(20,100)
	
	clip.audio.write_audiofile(out_path+"/"+file_name+".mp3")

def convert_to_wav(file_name):
	sound = AudioSegment.from_mp3(file_name)
	sound = sound.set_channels(1)
	sound = sound.set_frame_rate(32000)
	sound.export(file_name+".wav", format="wav")



def main_function(in_path, file_name):
	start = time.time()
	dir_name = file_name+"_dir"
	if os.path.exists(dir_name):
		os.chdir(dir_name)
	else:
		os.makedirs(dir_name)
		#os.chdir(dir_name)
		print("Directory does not exits!! Created the directory")
		try:
			convert_to_mp3(in_path, file_name, dir_name)
		except Exception as e:
			print("could not convert to mp3")
			print(e)
			sys.exit(1)
		print("Converted to mp3 successfully")
		os.chdir(dir_name)
		try:
			mp4_file_name = file_name + ".mp3"
			convert_to_wav(mp4_file_name)
		except Exception as e:
			print("could not convert to wav")
			print(e)
			sys.exit(1)
		print("Converted to wav successfully")
	
	mp4_file_name = file_name + ".mp3"
	try:
		chunks_dir_name = file_name + "_chunks"
		wav_file_name = mp4_file_name + ".wav"
		vd.convert_to_chunks(wav_file_name, 2, chunks_dir_name)
	except Exception as e:
		print("could not convert to chunks")
		print(e)
		sys.exit(1)
	print("Conversion to chunks successful")
	try :
		print(chunks_dir_name)
		wst.speech_to_text(chunks_dir_name)
	except Exception as e:
		print("could not translate chunks")
		print(e)
		sys.exit(1)
	print("Translation to chunks successful")

	try:
		questions_svm.train_test("../train_1.csv",chunks_dir_name+"/res_file_question.csv", "classification.csv")
	except Exception as e:
		print("Question classification does not work")
		print(e)
		sys.exit(1)
	try:
		list_sen.list_sentences("classification.csv", "list_of_questions.csv")
	except Exception as e:
		print("Listing questions does not work")
		print(e)
		sys.exit(1)
	
	try:
		srq.search_for_relvant_questions("../keywords.txt","list_of_questions.csv","../questions_results.csv",file_name)
	except Exception as e:
		print("Searching for relvant questions does not work")
		print(e)
		#return 1
		sys.exit(1)
	try:
		wav_file_name = mp4_file_name + ".wav"
		sa.split(wav_file_name, mp4_file_name+'_laugh_chunks')
	except Exception as e:
		print("could not split the video")
		print(e)
		#sys.exit(1)
		return 1
	try:
		#print(os.getcwd())
		os.chdir('..')
		print(mp4_file_name+'_dir')
		x = 'python2 pyAudioAnalysis/audioAnalysis.py classifyFolder -i ' + dir_name+'/'+mp4_file_name+'_dir'+' --model svm --classifier svm1 > ' + dir_name+'/laugh_result'
		print(x)
		os.system(x)
	except Exception as e:
		print("could not execute cmd")
		print(e)
		#sys.exit(1)
		return 1
	print("laughter detected")
	try:
		rs.remove_space(dir_name,'laugh_result', file_name)
	except Exception as e:
		print("Could not rename")
		print(e)
		#sys.exit(1)
		return 1
	print("result written csv")
	try:
		os.chdir('OpenVokaturi/examples')
		detect_emotion('../../'+ dir_name, wav_file_name, "emotion_results.csv")
		os.chdir("../..")
	except Exception as e:
		print("Emotion detection did not work")
		print(e)
		#sys.exit(1)
		return 1
	print("Emotion detection worked!!")

	end = time.time()
	os.chdir("..")
	print("Total time of execution: ",end - start,"seconds")
main_function('test', "file_1.mp4")
		
