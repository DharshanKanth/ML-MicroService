from joblib import dump
from sklearn.datasets import load_iris
from sklearn.ensemble  import RandomForestClassifier
from sklearn.model_selection import train_test_split

data=load_iris()
x=data.data
y=data.target

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

clf=RandomForestClassifier(n_estimators=100,random_state=42)

clf.fit(x_train,y_train)

dump(clf,'app/models/v2.joblib')

print("Model trained and saved to app/models/v2.joblib!")