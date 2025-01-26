import sklearn
import pandas as pd 
from sklearn import ensemble
from sklearn.metrics import mean_squared_error
import joblib
import numpy as np
import bentoml
from bentoml.io import NumpyNdarray

#print(joblib.__version__)

X_train = pd.read_csv('./data/processed/X_train_scaled.csv')
X_test = pd.read_csv('./data/processed/X_test_scaled.csv')
y_train = pd.read_csv('./data/processed/y_train.csv')
y_test = pd.read_csv('./data/processed/y_test.csv')
y_train = np.ravel(y_train)
y_test = np.ravel(y_test)

rf_regressor = ensemble.RandomForestRegressor(n_jobs = -1)

#--Train the model
rf_regressor.fit(X_train, y_train)

#--Test the model
y_predict = rf_regressor.predict(X_test)

#--Get the model accuracy
# accuracy = rf_regressor.score(X_test, y_test)
mse_test = mean_squared_error(y_test, y_predict)
print(f"MSE on test data: {mse_test}")

y_predict = rf_regressor.predict(X_train)
mse_train = mean_squared_error(y_train, y_predict)
print(f"MSE on train data: {mse_train}")
# test the model on a single observation
test_data = X_test.iloc[[0]]

# save test data to a txt file
test_data.to_csv('./models/test_data.txt', sep = ',', index = False)
# print the actual label
print(f"Actual label: {y_test[0]}")
# print the predicted label
print(f"Predicted label: {rf_regressor.predict(test_data)[0]}")

#--Save the trained model to a file
model_filename = './models/trained_model.joblib'
joblib.dump(rf_regressor, model_filename)
print("Model trained and saved successfully.")

# Save the model in BentoML's Model Store
model_ref = bentoml.sklearn.save_model("exam_rf", rf_regressor)
print(f"Model saved as: {model_ref}")
