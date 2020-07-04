import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS,cross_origin
import joblib

app = Flask(__name__)
model = joblib.load(open('joblib_catboost_bikes.pkl', 'rb'))


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if (request.method == 'POST'):

        choosen_season = request.form['choosen_season']
        if (choosen_season == 'Spring'):
            choosen_season = 0
        elif (choosen_season == 'Summer'):
            choosen_season = 1
        elif (choosen_season == 'Rainy'):
            choosen_season = 2
        else:
            choosen_season = 3

        choosen_govt_holiday = request.form['choosen_govt_holiday']
        if (choosen_govt_holiday == 'Yes'):
            choosen_govt_holiday = 1
        else:
            choosen_govt_holiday = 0

        choosen_workingday = request.form['choosen_workingday']
        if (choosen_workingday == 'Yes'):
            choosen_workingday = 1
        else:
            choosen_workingday = 0

        choosen_weather = request.form['choosen_weather']
        if (choosen_weather == 'Clear'):
            choosen_weather = 0
        elif (choosen_weather == 'Cloudy'):
            choosen_weather = 1
        elif (choosen_weather == 'Rainy'):
            choosen_weather = 2
        else:
            choosen_weather = 3

        choosen_hour = request.form['choosen_hour']
        if (choosen_hour == '0'):
            choosen_hour = 0
        elif (choosen_hour == '1'):
            choosen_hour = 1
        elif (choosen_hour == '2'):
            choosen_hour = 2
        else:
            choosen_hour = 3

        temperature = int(request.form['temperature'])
        felttemp = int(request.form['felttemp'])
        humidity = int(request.form['humidity'])
        windspeed = int(request.form['windspeed'])

        int_features = [choosen_season, choosen_govt_holiday, choosen_workingday, choosen_weather, temperature, felttemp,
              humidity, windspeed, choosen_hour]
        print(int_features)
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)
        print(prediction)
        output = round(prediction[0])
        return render_template('result.html', prediction_text='No of required Bikes are {}'.format(output))
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)