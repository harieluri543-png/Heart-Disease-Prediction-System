import random

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


# 1. load the dataset
df = pd.read_csv("dataset/heart.csv")

# 2. display the first five rows of the dataset
print("\nfirst 5 rows of the dataset:")
print(df.head())

# 3. display the last five rows of the dataset
print("\nlast 5 rows of the dataset:")
print(df.tail())

# 4. display the shape of the dataset
print("\nshape of the dataset :")
print(df.shape)

# 5. display the column names of the dataset
print("\ncolumn names of the dataset :")
print(df.columns) 

# 6. display the information about the dataset
print("\ninformation about the dataset :")
print(df.info())

# 7. check for missing values in the dataset
print("\nmissing values in the dataset :")
print(df.isnull().sum())

# 8. display the statistical summary of the dataset
print("\nstatistical summary of the dataset :")
print(df.describe())

# 9. count the target values in the dataset
print("\ncount of target values in the dataset :")
print(df["target"].value_counts())

# 10. train-test split
#input features(drops the target column not row)
x = df.drop("target", axis = 1)

#11. target(output) saves the target column in a variable 
y = df["target"]


x_train, x_test, y_train, y_test = train_test_split(x,
                                                    y,
                                                    test_size = 0.2, 
                                                    random_state = 42,
                                                    stratify=y)
print("\n shape of x_train :")
print("x-train shape :",x_train.shape)
print("x_test shape :",x_test.shape)

print("\n y_train shape :",y_train.shape)
print("y_test shape :",y_test.shape)


# Logistic Regression
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(x_train, y_train)
lr_pred = lr_model.predict(x_test)
lr_accuracy = accuracy_score(y_test, lr_pred)

# Decision Tree
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(x_train, y_train)
dt_pred = dt_model.predict(x_test)
dt_accuracy = accuracy_score(y_test, dt_pred)

# Random Forest
rf_model = RandomForestClassifier(random_state=42,
                                n_estimators=300,
                                max_depth=8,
                                )
rf_model.fit(x_train, y_train)
rf_pred = rf_model.predict(x_test)
rf_accuracy = accuracy_score(y_test, rf_pred)

from sklearn.metrics import confusion_matrix, classification_report

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, rf_pred))

print("\nClassification Report:")
print(classification_report(y_test, rf_pred))

print("================== Model Comparison ==================")
print("Logistic Regression Accuracy :", lr_accuracy)
print("Decision Tree Accuracy       :", dt_accuracy)
print("Random Forest Accuracy       :", rf_accuracy)

# Automatically choose and save the best model


joblib.dump(rf_model, "model/heart_model.pkl")

print("Random Forest model saved.")

print("\nModel Used: Random Forest")
print(f"Accuracy: {rf_accuracy:.4f}")
print("Model saved successfully!")







