import requests
import logging
# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
logging.basicConfig(filename='python_script.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
regressor=None
def trainModel():
    
    logging.info("Script started successfully")
    url = "https://api.example.com/data"
    dataset = call_external_service(url)
    
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values
    print(X)
    # Encoding categorical data
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder
    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [3])], remainder='passthrough')
    X = np.array(ct.fit_transform(X))
    print(X)
    # Splitting the dataset into the Training set and Test set
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

    # Training the Multiple Linear Regression model on the Training set
    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)


def call_external_service(url, params=None):
    try:
        logging.info("Script started successfully2")
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()  # Return the json-encoded content of a response, if any
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def getInstance():
    if regressor is None
        trainModel()
    
    return regressor
