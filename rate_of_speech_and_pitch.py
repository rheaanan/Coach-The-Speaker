import os
import wave
import contextlib
import math 
import csv
import librosa
import librosa.display 
import numpy as np 
import pandas as pd
from decimal import Decimal

#dir_list = os.listdir('complete')
#print(len(dir_list))
#print(dir_list)
i = 1
#chunk-01.wav response
def pitch_rate_amplitude(chunk_folder, result_csv):
	
	with open(chunk_folder+'/'+result_csv, 'a') as csvfile:
		fieldnames = ['file_name', 'avg_speed','avg_pitchrange','amplitude1','amplitude2','amplitude3']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		#os.chdir('complete')	
		try:
			os.chdir(chunk_folder)
			#print(chunk_folder.split('.')[0]+'.mp4.mp3.wav')
			name = chunk_folder.split('.')[0]
			spf = wave.open(name+'.mp4.mp3.wav')

			#Extract Raw Audio from Wav File
			signal = spf.readframes(-1)
			signal = np.fromstring(signal, 'Int16')
			fs = spf.getframerate()
			#times = np.arange(len(signal))/float(fs)
			total_time=len(signal)/fs
			peak_values = [] 
			#print(times[0],times[-1])
			#lform = list(times)
			count=1
			first_idx1 = 0
			first_idx2 = 384000
			difference= first_idx2-first_idx1
			#print('the value you need',first_idx1,first_idx2,difference)
			for i in range(int(0),int(total_time)-12,12):
				#print("i",i)
				if i==0:
					idx1 = first_idx1
					idx2 = first_idx2
				else :
					idx1 = idx2+1
					idx2 = idx1+difference
				#print(idx1,"   dhg ",idx2)	
				#print("peak in 12sec gap number",count,np.amax(signal[idx1:idx2]))
				peak_values.append(np.amax(signal[idx1:idx2]))
				#lform=lform[i+12:]
				count +=1  
			how_many_together = math.floor(count/3) 
			#print(how_many_together) 
			#print(peak_values)
			amplitude =[]
			count_parts=0
			last_index=0
			for i in range(0,len(peak_values)-how_many_together,how_many_together):
				#print(peak_values[i:i+how_many_together])
				peaks_for_avg = peak_values[i:i+how_many_together]
				#print(sum(peaks_for_avg /len(peaks_for_avg ))) 
				amplitude.append(sum(peaks_for_avg )/len(peaks_for_avg ))  
				last_index=i+how_many_together
				count_parts+=1
			if count_parts!=3:
				i= last_index
				left_overs = peak_values[i:]
				#print(sum(left_overs/len(left_overs))) 
				amplitude.append(sum(left_overs)/len(left_overs)) 
				 	   
			os.chdir(name+'.mp4_chunks')
			f = open("res_file_question.csv", "r")
			lines = f.readlines()
			f.close()
			#new_file = open(res_file"_labeled.txt", "a")
			pitchrange_in_chunks=[]
			pitchrange_sum=0
			number_of_chunks = 0 
			speed_sum = 0
			for line in lines:
				line = line.strip()
				#print(line)
				d = line.split(",")
				if len(d[0])!=0:
					#print(d[1].split(' ')[0],"hi")
				
					#print(d[1].split(' ')[0])
					if(len(d) >= 2):
						data = d[0]
						#print(data)
					
						if(data ==' None'):
							#do nothing
							print("none") 
						else:
							words = len(data.split())
							with contextlib.closing(wave.open(d[1].split(' ')[0],'r')) as f:
								frames = f.getnframes()
								rate = f.getframerate()
								duration = frames / float(rate)
								#print("words:",words)
								#print("duration:",duration)
								speed = math.ceil(words/duration)
								#print("speed:",speed)
								speed_sum+=speed
								number_of_chunks+=1
							y, sr = librosa.load(d[1].split(' ')[0],duration=1.0)
							librosa.feature.chroma_stft(y=y, sr=sr)
							#print(len(y))


							# Use a pre-computed power spectrogram with a larger frame
							#while finding the distance we nee to find the cyclically nearest pitch 
							S = np.abs(librosa.stft(y, n_fft=4096))**2
							chroma = librosa.feature.chroma_stft(S=S, sr=sr)
							m,n = chroma.shape
							#print(m,n)
							secs_required_for_a_word = 1/float(speed)
							#print(secs_required_for_a_word)
							idx1 = 0
							idx2 = math.floor(n/speed)
							#print(idx1,idx2)
							pitch_values_in_secs_req=[]
							for i in range(idx1,idx2):
								pitch_value = list((chroma[:,i])).index(1)+1
								pitch_values_in_secs_req.append(pitch_value)
							pitch_range = abs(min(pitch_values_in_secs_req)-max(pitch_values_in_secs_req))
							pitchrange_in_chunks.append(pitch_range)	
							pitchrange_sum+=pitch_range
							#print(pitch_range)
							'''
							++++++++++++ for plotting ++++++++++++
							import matplotlib.pyplot as plt
							plt.figure(figsize=(10, 4))
							librosa.display.specshow(chroma, y_axis='chroma', x_axis='time')
							plt.colorbar()
							plt.title('Chromagram')
							plt.tight_layout()
							plt.show()
							'''
			avg_pitchrange = pitchrange_sum/number_of_chunks
			avg_speed=(speed_sum/number_of_chunks)
			#print("average speed in number of words per second",avg_speed)
			#print("average pitch range in all chunks",avg_pitchrange)
			d = [round(avg_speed,2), round(avg_pitchrange,2), round(amplitude[0],2), round(amplitude[1],2), round(amplitude[2],2)]
			writer.writerow({'file_name': chunk_folder[:-4], 'avg_speed': round(avg_speed,2),'avg_pitchrange': round(avg_pitchrange,2),'amplitude1':round(amplitude[0],2),'amplitude2':round(amplitude[1],2),'amplitude3':round(amplitude[2],2)})
			print("Success")
			os.chdir('..')
			return d
		except Exception as e:
			os.chdir('..')
			print(os.getcwd())
			print("FAILED: ", chunk_folder)
			print("REASON: ", e)
			return -1
#pitch_rate_amplitude('file_1.mp4_dir','pitch_results.csv')

