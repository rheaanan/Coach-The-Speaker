from flask import Flask
from flask import render_template, abort, jsonify, request,redirect, json
import questions_laugh_mood_pitch_board as inte
from werkzeug import secure_filename
app = Flask(__name__)
app.debug = True

@app.route('/index.html')
def index():
    return render_template('lumino/index.html')

@app.route('/charts.html')
def charts():
    return render_template('lumino/charts.html') 

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
    return render_template('lumino/widgets.html')
 
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		print("File upload successful")
	try:
		file_name = secure_filename(f.filename)
		print(file_name)
		res = inte.main_function('.', file_name)
	except ValueError:
		return jsonify("Please enter filename.")
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
