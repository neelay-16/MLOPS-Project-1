import joblib
import numpy as np
from config.paths_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template, request

app = Flask(__name__)

loaded_model = joblib.load(MODEL_OUTPUT_PATH)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        lead_time = int(request.form["lead_time"])
        no_of_special_request = int(request.form["no_of_special_request"])
        avg_price_per_room = float(request.form["avg_price_per_room"])
        arrival_month = int(request.form["arrival_month"])
        # This is known as typecasting. Which means that we are taking data as string
        # in index.html and to process it we convert it to integer
        arrival_date = int(request.form["arrival_date"])
        market_segment_type = int(request.form["market_segment_type"])
        no_of_week_nights = int(request.form["no_of_week_nights"])
        no_of_weekend_nights = int(request.form["no_of_weekend_nights"])
        type_of_meal_plan = int(request.form["type_of_meal_plan"])
        room_type_reserved = int(request.form["room_type_reserved"])

        features = np.array([[lead_time, no_of_special_request, avg_price_per_room, arrival_month, arrival_date, market_segment_type, no_of_week_nights, no_of_weekend_nights, type_of_meal_plan, room_type_reserved]])
        # Here, we are converting the input data into a numpy array to feed into the model using the double dimension.

        prediction =  loaded_model.predict(features)

        return render_template('index.html', prediction=prediction[0])
        #Here, render_template will just show the results on the html page
        #flask will automatically detect the templates folder and the index.html file in it
        #predictions[0] means that if we see the jupyter notebook prediction, it shows something like this
        #array([1]). So to avoid that array thing and directly fetching the value from that list we write it as 
        #prediction[0]
    return render_template('index.html')  #thisis the else part.
                                          #basically if something is wrong with the data or no data is passed
                                          #our index.html should keep running but with no predictions

if __name__=="__main__":
    app.run(host='0.0.0.0' , port=5000)
    