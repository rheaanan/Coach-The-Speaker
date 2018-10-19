import os
import moviepy.editor as mp



def start(folder_name, exp_len1):
	videos = os.listdir(folder_name)
	c1 = 0
	t = len(videos)
	os.chdir(folder_name)
	for video in videos:
		clip = mp.VideoFileClip(video)
		dur = clip.duration
		#print(dur)
		if dur > exp_len1:
			c1 += 1
	print("No of vidoes with len more than ", exp_len1, ':', c1)
start('/home/shreyasi/8thSem/integration/downloaded_videos',1240)
