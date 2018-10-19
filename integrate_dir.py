import questions_laugh_mood_pitch as qlmp
import os
def start(folder_name, res_file):
	videos = os.listdir(folder_name)
	c = 1
	t = len(videos)
	for video in videos:
		try: 
			qlmp.main_function(folder_name, video, res_file)
		except Exception as e:
			print("Could not covert: ", video)
			print(e)
		print("Completed video: ", c, '/', t)
		c = c + 1

start('/home/shreyasi/8thSem/integration/downloaded_videos', 'combined_results_part2.csv')
