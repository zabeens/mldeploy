import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [x for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    prob = model.predict_proba(final_features)
    term_output='{0:.{1}f}'.format(prob[0][1], 2)
    retent_output='{0:.{1}f}'.format(prob[0][0], 2)

    if term_output>str(0.5):
        return render_template('index.html',prediction_text='Status of Employee is "1" - Means Employee has more chances to attrite and Attrition probability is  {}'.format(term_output))
    else:
        return render_template('index.html',prediction_text='Status of Employee is "0" -Means Employee has more chances to retain and Retention probability is  {}'.format(retent_output))
    

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True,port=12345)
