from joblib import load
import numpy as np
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, classification_report

clf=load("iris_model.joblib")

data=load_iris()
x=data.data
y=data.target

y_pred=clf.predict(x)
print("Accuracy:", accuracy_score(y, y_pred))
print("Classification Report:\n", classification_report(y,y_pred))

sample=x[0]
print("Sample", sample)
print("Predicted class: ", clf.predict([sample])[0])