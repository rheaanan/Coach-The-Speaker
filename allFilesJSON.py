from flask import Flask
from flask import render_template, abort, jsonify, request,redirect, json, make_response
import questions_laugh_mood_pitch_board as inte
from werkzeug import secure_filename
app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
obj = {"pitchSuggestion": "Inconsistent", "avgSpeed": 0, "amplitudeScore": 0, "laughter": 0, "boardSuggestion": "Inconsistent", "boardUsage": 0, "amplitudeSuggestion": "Inconsistent", "questionsSuggestion": "Inconsistent", "laughterScore": 0, "Fear": 0, "avgPitchrange": 0, "Happy": 0, "amplitude2": 0, "laughterSuggestion": "Inconsistent", "boardScore": 0, "amplitude3": 0, "avgSpeedScore": 0, "Angry": 0, "pitchScore": 0, "questions": 0, "Sad": 0, "moodScore": 0, "Neutral": 0, "avgSpeedSuggestion": "Inconsistent", "questionsScore": 0, "moodSuggestion": "Inconsistent", "relevantQuestions": 0, "amplitude1": 0, "finalScore": 0};
res_data = json.dumps(obj)

@app.route('/index.html')
def index():
    return render_template('lumino/index.html')

@app.route('/charts.html')
def charts():
    return render_template('lumino/charts.html',res_data=res_data) 


@app.route('/elements.html')
def elements():
    return render_template('lumino/elements.html') 

@app.route('/login.html')
def login():
    return render_template('lumino/login.html') 

@app.route('/panels.html')
def panels():
    return render_template('lumino/panels.html') 

@app.route('/widgets.html')
def widgets():
	print(res_data)
	return render_template('lumino/widgets.html',res_data=res_data)
 
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		print("File upload successful")
	try:
		file_name = secure_filename(f.filename)
		print(file_name)
		#res = inte.main_function('.', file_name)
		res = {'boardScore': 5, 'questionsSuggestion': 'We detected that you asked about 4 questions, out of which 50 % were relevant. Interaction wise, your lecture scored a 4 on 5... Great work! You definitely keep your audience on its toes with the number of questions you ask!', 'laughterScore': 4, 'amplitude3': 20904.25, 'avgPitchrange': 5.11, 'avgSpeedScore': 4, 'amplitudeSuggestion': 'The audio was split into three temporal chunks - beginning, middle and end. Each chunk is roughly one-third of the total audio length.You maintained a consistent level of loudness during the lecture. Well done!', 'Angry': 0.951, 'Fear': 0.0, 'avgSpeedSuggestion': 'Inconsistent', 'amplitude1': 20714.75, 'questionsScore': 4, 'boardUsage': 0.4892430362122942, 'relevantQuestions': 2, 'amplitudeScore': 4, 'avgSpeed': 3.6, 'finalScore': 4, 'boardSuggestion': 'Our analysis showed that your board usage was approximately 48.92430362122942 during the lecture.Good work on board usage! You are scoring above average according to our data so far.', 'Happy': 0.047, 'pitchSuggestion': 'Inconsistent', 'questions': 4, 'moodSuggestion': 'Our model scored your mood during the lecture a 5 out of 5... You stayed neutral for about 0.1  of the time.Analysis indicates that you were happy about 4.7 of the time.The lecture had high energy for about 95.1 of the time.', 'laughterSuggestion': 'We detected signs of laughter about 10 times during the lecture. Our model scored it a 4 out of 5... Great work! You definitely keep your audience amused!', 'Sad': 0.001, 'amplitude2': 20714.75, 'laughter': 10, 'Neutral': 0.001, 'moodScore': 5, 'pitchScore': 5}
		#res_data = make_response(jsonify({"status": "ok", "data": res}), 201)
		#res = {"abc":3, "dj": 38}"
	except ValueError:
		return jsonify("Please enter filename.")
	global res_data
	res_data = json.dumps(res)	
	return render_template('lumino/charts.html',res_data=res_data)

@app.route("/predict", methods=['POST'])
def predict():
	if request.method == 'POST':
		try:
			data = request.get_json()
			print(data)
			file_name = data['filename']
			print(file_name)
			res = inte.main_function('.', file_name)
		except ValueError:
			return jsonify("Please enter filename.")

		return jsonify(res)


if __name__ == '__main__':
    app.run()
