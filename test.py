import json
import numpy as np
import pandas as pd
from flask import Flask,jsonify
from flask_cors import CORS

df_1 = pd.read_csv(r"D:\fakeReviewProject2\1_dataset.csv")

df_1 = df_1.dropna()

df_1.loc[(df_1['Annotation'] == 1) & (df_1['Actual_True'] == 1), 'Outcome'] = 'TP'
df_1.loc[(df_1['Annotation'] == 1) & (df_1['Actual_True'] == 0), 'Outcome'] = 'FP'
df_1.loc[(df_1['Annotation'] == 0) & (df_1['Actual_True'] == 1), 'Outcome'] = 'FN'
df_1.loc[(df_1['Annotation'] == 0) & (df_1['Actual_True'] == 0), 'Outcome'] = 'TN'

df_1['Outcome'].value_counts()

total = len(df_1)
a = (df_1.loc[df_1.Outcome == 'FN', 'Outcome'].count()/total)*100
b = (df_1.loc[df_1.Outcome == 'TN', 'Outcome'].count()/total)*100
c = (df_1.loc[df_1.Outcome == 'FP', 'Outcome'].count()/total)*100
d = (df_1.loc[df_1.Outcome == 'TP', 'Outcome'].count()/total)*100
print(a, b, c, d)

up_num = b + d  # = TN + TP
down_den = a + b + c + d  # = FN + TN + FP + TP
accuracy = up_num / down_den  # = (TN + TP) / (FN + TN + FP + TP) 
print(accuracy * 100)
precision = d /(c + d) # TP / (FP + TP)
print(precision*100)
recall = d / (c + a) # TP / (FN + TP)
print(recall*100)
f1 = 2/((1/precision)+(1/recall))
print(f1*100)

apijs = df_1.to_json(orient="records")
product = json.loads(apijs)

app = Flask(__name__)
CORS(app)
@app.route("/", methods=['GET'])
def get():
	return jsonify(product)

@app.route('/product/<task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in product if task['productId'] == task_id]
    if len(task) == 0:
        return "Not Available"
    return jsonify(task)

if __name__ == "__main__":
	app.run(debug=True)