from flask import Flask
from flask import render_template, abort, jsonify, request,redirect, json
import questions_laugh_mood_pitch_board as inte
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

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
