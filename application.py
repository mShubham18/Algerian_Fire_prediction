from flask import Flask,url_for,jsonify,render_template,request
import pandas as pd
import numpy as np
import pickle

scaler_model = pickle.load(open("models/scaler.pkl","rb"))
ridge_cv = pickle.load(open("models/ridgecv.pkl","rb"))


application = Flask(__name__)
app=application
@app.route("/",methods=["GET","POST"])
def predict_datapoint():
    if request.method == "POST":
        Temperature = int(request.form.get("Temperature"))
        RH = int(request.form.get("RH"))
        Ws = int(request.form.get("Ws"))
        Rain = float(request.form.get("Rain"))
        FFMC = float(request.form.get("FFMC"))
        DMC = float(request.form.get("DMC"))
        ISI = float(request.form.get("ISI"))
        Classes = int(request.form.get("Classes"))
        Region = int(request.form.get("Region"))

        scaled_data = scaler_model.transform([[Temperature,RH,Ws,Rain,FFMC,DMC,ISI,Classes,Region]])
        result = ridge_cv.predict(scaled_data)[0]
        return render_template("form.html",result=f"{result:.2f}")
    else:
        return render_template("form.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)