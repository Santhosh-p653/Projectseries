import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
df=pd.read_csv(r"E:\programs\ml\data\iris.csv")
print(df.head())
df['is_setosa']=(df['species']=='setosa').astype(int)
x=df[['sepal_length','sepal_width','petal_length','petal_width']]
y=df['is_setosa']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
model=LogisticRegression(max_iter=200)
model.fit(x_train,y_train)
y_pred=model.predict(x_test)
print(accuracy_score(y_test,y_pred))
print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))