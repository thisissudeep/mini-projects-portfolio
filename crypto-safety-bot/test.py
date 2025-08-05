import pandas as pd
import joblib

raw_data = {
    "length": [2],
    "weight": [0.25],
    "count": [1],
    "looped": [0],
    "neighbors": [2],
    "income": [87411400000],
}


new_data = pd.DataFrame(raw_data)
# print("New Transaction Data:\n", new_data)

scaler = joblib.load("scaler.pkl")
new_data_scaled = scaler.transform(new_data)
new_data_scaled = pd.DataFrame(new_data_scaled, columns=new_data.columns)

# print("Standardized Data:\n", new_data_scaled)

model = joblib.load("model.pkl")
prediction = model.predict(new_data_scaled)
print("Prediction:", prediction)
if prediction[0] == 1:
    print("Fraud Detected!\n")
else:
    print("Non-Fraud\n")
probabilities = model.predict_proba(new_data_scaled)
print("Prediction Probabilities (Non-Fraud, Fraud):", probabilities)


"""
Fraud Test Cases:

raw_data = {
    'length': [144],
    'weight': [0.099877597],
    'count': [8120],
    'looped': [0],
    'neighbors': [1],
    'income': [50057953]
}

raw_data = {
    "length": [18],
    "weight": [0.008333333],
    "count": [1],
    "looped": [0],
    "neighbors": [2],
    "income": [100050000],
}

raw_data = {
    "length": [18],
    "weight": [0.125],
    "count": [1],
    "looped": [0],
    "neighbors": [2],
    "income": [1.00e08],
}



"""


"""
Non-Fraud / White Test Cases:

raw_data = {
    "length": [0],
    "weight": [0.5],
    "count": [1],
    "looped": [0],
    "neighbors": [1],
    "income": [410000000],
}

raw_data = {
    'length': [2],
    'weight': [0.25],
    'count': [1],
    'looped': [0],
    'neighbors': [2],
    'income': [87411400000]
}

raw_data = {
    "length": [4],
    "weight": [0.5],
    "count": [1],
    "looped": [0],
    "neighbors": [1],
    "income": [3.00e07],
}

"""
