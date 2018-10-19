#gives laughter result
def remove_space(dir_name, input_file, video_file_name):
	res_file = open("laughter_results.csv", "a")
	with open(dir_name+"/"+input_file) as f:
		lines = f.read().splitlines()
		#print(lines)
		line = lines[0]
		a = ','.join(line.split())
		r = [a.split(",")[1]]
		d = video_file_name+","+a.split(",")[1]+"\n"
		res_file.write(d)
		res_file.close()
		#print(d)
		return r

#remove_space("file_1.mp4_dir/laugh_result")
