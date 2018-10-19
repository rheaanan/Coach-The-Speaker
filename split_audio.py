import os
from pydub import AudioSegment
import shutil

def split(in_file, out_dir_name):
	if os.path.exists(out_dir_name):
		shutil.rmtree(out_dir_name, ignore_errors=True)
	
	os.makedirs(out_dir_name)
	
	song = AudioSegment.from_wav(in_file)
	os.chdir(out_dir_name)
	start = 0
	end = len(song)
	c = 1
	#print(len(song))
	for i in range(start,end,10000):
		chunk = song[i:i+10000]
		file_name = "chunk-"+str(c)+".wav"
		chunk.export(file_name, format="wav")
		print("Chunk no: "+str(c)+" completed!!")
		c = c + 1
	print("File: ", in_file,"completed.")	
	os.chdir("..")
		
#split("test.wav", "test_final")

