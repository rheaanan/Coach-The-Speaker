import csv
def clean(in_file, out_file):
	res = []
	with open(in_file) as f:
		for line in f:
			#print(line)
			line = line.strip('\n')
			line = line.split(',')
			#print(line)
			line[0] = line[0].split('.')[0]+'_1'+'.mp4'
			res.append(line)
	print(res)
	with open(out_file, 'a') as csvfile:
    	# creating a csv writer object
		csvwriter = csv.writer(csvfile)
		csvwriter.writerows(res)
clean("combined_results.csv", "combined_results_part1.csv")
