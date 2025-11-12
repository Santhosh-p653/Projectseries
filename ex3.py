from statistics import LinearRegression
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score
df=pd.read_csv(r"E:\programs\ml\data\iris.csv")
x=df[['sepal_width','petal_length','petal_width']]
y=df['sepal_length']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
model=LinearRegression()
model.fit(x_train,y_train)
y_pred=model.predict(x_test)
print(model.intercept_)
print(model.coef_)
print(mean_squared_error(y_test,y_pred))
print(r2_score(y_test,y_pred))



