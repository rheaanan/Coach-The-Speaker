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
import rate_of_speech_and_pitch as rsp
from OpenVokaturi.examples.voka_one_file import detect_emotion
import screenshot_one_file as sc
import board_one_file as my_board
import dt_for_flask_main_model as mm
import dt_for_flask_questions as qq
import dt_for_flask_rate_of_speech as ros
import dt_for_flask_amplitude as am
import dt_for_flask_pitch as pi
import dt_for_flask_board as bo
import dt_for_flask_laughter as la
import dt_for_flask_mood as mo
import text_out as suggestion
import json
def convert_to_mp3(in_path, file_name,out_path):
	#print(os.getcwd())
	clip = mp.VideoFileClip(in_path+'/'+file_name).subclip(20,320)
	#clip = mp.VideoFileClip(in_path+'/'+file_name).subclip(1240,1860)
	#clip = mp.VideoFileClip(in_path+'/'+file_name).subclip(1860,2460)
	clip.audio.write_audiofile(out_path+"/"+file_name+".mp3")

def convert_to_wav(file_name):
	sound = AudioSegment.from_mp3(file_name)
	sound = sound.set_channels(1)
	sound = sound.set_frame_rate(32000)
	sound.export(file_name+".wav", format="wav")



def main_function(in_path, file_name):
	result_list = ['actual name', file_name]
	start = time.time()
	dir_name = file_name+"_dir"
	if os.path.exists(dir_name):
		os.chdir(dir_name)
	else:
		os.makedirs(dir_name)
		os.chdir(dir_name)
		print("Directory does not exits!! Created the directory")
		try:
			sc.get_shots('../'+in_path+'/'+file_name)
		except Exception as e:
			print(e)
			return {"status":"error"}
		print("SCREENSHOT DONE")
		try:
			x = my_board.board()
			print(x)
		except Exception as e:
			print(e)
			return {"status":"error"}
		print("board value: ",x)
		os.chdir('..')
		try:
			convert_to_mp3(in_path, file_name, dir_name)
		except Exception as e:
			print("could not convert to mp3")
			print(e)
			#sys.exit(1)
			#return 1
			return {"status":"error"}
		
		print(os.getcwd())
		os.chdir(dir_name)
		print("Converted to mp3 successfully")
		try:
			print("ABC")
			mp4_file_name = file_name + ".mp3"
			convert_to_wav(mp4_file_name)
			print("ABC")
			
		except Exception as e:
			print("could not convert to wav")
			print(e)
			#sys.exit(1)
			return {"status":"error"}
		print("Converted to wav successfully")
	
	mp4_file_name = file_name + ".mp3"
	try:
		chunks_dir_name = file_name + "_chunks"
		wav_file_name = mp4_file_name + ".wav"
		vd.convert_to_chunks(wav_file_name, 2, chunks_dir_name)
	except Exception as e:
		print("could not convert to chunks")
		print(e)
		#sys.exit(1)
		return {"status":"error"}
	print("Conversion to chunks successful")
	try :
		print(chunks_dir_name)
		wst.speech_to_text(chunks_dir_name)
	except Exception as e:
		print("could not translate chunks")
		print(e)
		#sys.exit(1)
		return {"status":"error"}
	print("Translation to chunks successful")

	try:
		questions_svm.train_test("../train_1.csv",chunks_dir_name+"/res_file_question.csv", "classification.csv")
	except Exception as e:
		print("Question classification does not work")
		print(e)
		#sys.exit(1)
		return {"status":"error"}
	try:
		list_sen.list_sentences("classification.csv", "list_of_questions.csv")
	except Exception as e:
		print("Listing questions does not work")
		print(e)
		#sys.exit(1)
		return {"status":"error"}
	
	try:
		q_res = srq.search_for_relvant_questions("../keywords.txt","list_of_questions.csv","../questions_results.csv",file_name)
		result_list.extend(q_res)
	except Exception as e:
		print("Searching for relvant questions does not work")
		print(e)
		return {"status":"error"}
		#sys.exit(1)
	try:
		wav_file_name = mp4_file_name + ".wav"
		sa.split(wav_file_name, mp4_file_name+'_laugh_chunks')
	except Exception as e:
		print("could not split the video")
		print(e)
		#sys.exit(1)
		return {"status":"error"}
	try:
		#print(os.getcwd())
		os.chdir('..')
		print(mp4_file_name+'_dir')
		z = 'python2 pyAudioAnalysis/audioAnalysis.py classifyFolder -i ' + dir_name+'/'+mp4_file_name+'_laugh_chunks'+' --model svm --classifier svm1 > ' + dir_name+'/laugh_result'
		print(z)
		os.system(z)
	except Exception as e:
		print("could not execute cmd")
		print(e)
		#sys.exit(1)
		return {"status":"error"}
	print("laughter detected")
	try:
		l_res = rs.remove_space(dir_name,'laugh_result', file_name)
		result_list.extend(l_res)
	except Exception as e:
		print("Could not rename")
		print(e)
		#sys.exit(1)
		return {"status":"error"}
	print("result written csv")
	try:
		os.chdir('OpenVokaturi/examples')
		e_res = detect_emotion('../../'+ dir_name, wav_file_name, "emotion_results.csv")
		result_list.extend(e_res)
		os.chdir("../..")
	except Exception as e:
		print("Emotion detection did not work")
		print(e)
		return {"status":"error"}
	print("Emotion detection worked!!")
	print(os.getcwd())
	try:
		rsp_res = rsp.pitch_rate_amplitude(dir_name, 'pitch_results.csv')
		result_list.extend(rsp_res)
	except Exception as e:
		print("Could not execute pitch")
		print(e)
		return {"status":"error"}
	end = time.time()
	print('result list: ', result_list)
	os.chdir("..")
	result_list[0] = result_list[0].split('.')[0]+'_2'+'.mp4'
	
	rel_questions = result_list.pop(3)
	result_list.append(x)
	result_list.append(-1)
	result_list.append(rel_questions)
	result_list.pop(4)
	result_list[3] = int(result_list[3])
	'''json_res = {
	'questions':result_list[2],
	'relevant-questions':result_list[16],
	'laughter':result_list[3],
	'Neutral':result_list[4],
	'Happy':result_list[5],
	'Sad':result_list[6],
	'Angry':result_list[7],
	'Fear':result_list[8],
	'avg_speed':result_list[9],
	'avg_pitchrange': result_list[10],
	'amplitude1':result_list[12],
	'amplitude2':result_list[12],
	'amplitude3':result_list[13],
	'board_usage':result_list[14]
	}'''
	print(result_list)
	#print(json_res)
	#print("Total time of execution: ",end - start,"seconds")
	#return json_res
	try:
		final_score = mm.predict_value(result_list)
	except Exception as e:
		print("Could not find final score")
		print(e)
		return {"status":"error"}
	try:
		questions_score = qq.predict_value(result_list)
	except Exception as e:
		print("Could not find questions score")
		print(e)
		return {"status":"error"}
	try:
		ros_score = ros.predict_value(result_list)
	except Exception as e:
		print("Could not find rate of speech score")
		print(e)
		return {"status":"error"}
	try:
		amp_score = am.predict_value(result_list)
	except Exception as e:
		print("Could not find aplitude score")
		print(e)
		return {"status":"error"}
	try:
		pitch_score = pi.predict_value(result_list)
	except Exception as e:
		print("Could not find pitch score")
		print(e)
		return {"status":"error"}
	try:
		laughter_score = la.predict_value(result_list)
	except Exception as e:
		print("Could not find laughter score")
		print(e)
		return {"status":"error"}
	try:
		mood_score = mo.predict_value(result_list)
	except Exception as e:
		print("Could not find mood score")
		print(e)
		return {"status":"error"}
	try:
		board_score = mo.predict_value(result_list)
	except Exception as e:
		print("Could not find board score")
		print(e)
		return {"status":"error"}
	scores = [questions_score, laughter_score, mood_score, ros_score, pitch_score, amp_score, board_score]
	result_list[15] = final_score
	new_res_list = result_list[2:]
	print("SCORES: ", scores)
	print("FINAL LIST: ", new_res_list)
	try:
		sug = suggestion.scoresToText(new_res_list, scores)
	except Exception as e:
		print("Could not find suggestions")
		print(e)
		return {"status":"error"}

	print("SUGGESSIONS")
	print(sug)
	sug = json.loads(sug)
	json_res = {
	'questions':result_list[2],
	'relevantQuestions':result_list[16],
	'laughter':result_list[3],
	'Neutral':result_list[4],
	'Happy':result_list[5],
	'Sad':result_list[6],
	'Angry':result_list[7],
	'Fear':result_list[8],
	'avgSpeed':result_list[9],
	'avgPitchrange': result_list[10],
	'amplitude1':result_list[12],
	'amplitude2':result_list[12],
	'amplitude3':result_list[13],
	'boardUsage':result_list[14],
	'questionsScore':int(questions_score),
	'laughterScore': int(laughter_score),
	'moodScore': int(mood_score),
	'avgSpeedScore': int(ros_score),
	'pitchScore':int(pitch_score),
	'amplitudeScore':int(amp_score),
	'boardScore': int(board_score),
	'finalScore': int(final_score),
	'questionsSuggestion':sug['Questions'],
	'laughterSuggestion': sug['Laughter'],
	'moodSuggestion': sug['Mood'],
	'avgSpeedSuggestion': sug['Rateofspeech'],
	'pitchSuggestion':sug['Pitch'],
	'amplitudeSuggestion':sug['Amplitude'],
	'boardSuggestion':sug['Board'],
	
	}
	print("FINAL JSON")
	print(json_res)
	print("FINAL DIR: ", os.getcwd())
	new_file_name = file_name + '_json'
	final_json =  json.dumps(json_res)
	with open("result_jsons/"+new_file_name,"w+") as f:
		f.write(final_json)
		
	
	#f = open('result_json/'+new_file_name, 'w+')
	#f.write(final_json)
	print("Total time of execution: ",end - start,"seconds")
	return json_res
#main_function('.', "IMG_1342.mp4")
		
