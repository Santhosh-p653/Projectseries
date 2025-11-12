import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,classification_report
df=pd.read_csv(r"E:\programs\ml\data\iris.csv")
print(df.head())
print(df.shape)
print(df.info())
print(df['species'].value_counts())
x=df.drop('species',axis=1)
y=df['species']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
model=LogisticRegression(max_iter=200)
model.fit(x_train,y_train)
y_pred=model.predict(x_test)
print ("accuracy",accuracy_score(y_test,y_pred))
print(classification_report(y_test,y_pred))
for rs in [1,5,10,21,42,100]:
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=rs)
    model.fit(x_train,y_train)
    print(f"Random state{rs}->accuracy:{model.score(x_test,y_test):.2f}")
