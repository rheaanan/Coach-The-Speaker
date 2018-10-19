import cv2
import os
import shutil
def get_shots(vid_name):
	#dir_name=vid_name+"_dir"
	vidcap = cv2.VideoCapture(vid_name);
	no_of_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
	chunklength = no_of_frames//10
	success,image = vidcap.read()
	count = 0
	success = True
	#folder = 'shots2/'+dir_name
	folder = 'shots2'
	if os.path.exists('shots2'):
		shutil.rmtree(dir_name, ignore_errors=True)
	os.makedirs('shots2')
	while success:
		success,image = vidcap.read()
		#print('read a new frame:',success)
		if count%chunklength == 0 :
			print("count: ",count)
			cv2.imwrite(folder+'/frame'+str(count//chunklength)+'.png',image)
			#print('success')
		count+=1
		#if count==600:
		#break
	

#get_shots('test-2.mp4')  
