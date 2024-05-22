import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
data = pd.read_csv('Blood_samples_dataset_balanced_2(f).csv')

# Ensure column names are clean
data.columns = [col.strip().lower().replace(' ', '_') for col in data.columns]

# Verify the column names
print(data.columns)

# Define features and target
X = data.drop('disease', axis=1)
y = data['disease']
print(y.unique())

# # Split the data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # Train a machine learning model
# model = RandomForestClassifier(random_state=42)
# model.fit(X_train, y_train)
#
# # Evaluate the model
# predictions = model.predict(X_test)
# print(f'Accuracy: {accuracy_score(y_test, predictions)}')
#
# # Save the model and the column names
# joblib.dump(model, 'disease_prediction_model.pkl')
# joblib.dump(X.columns.tolist(), 'model_columns.pkl')
