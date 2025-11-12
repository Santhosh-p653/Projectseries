from turtle import color
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error,r2_score

df=pd.read_csv(r"E:\programs\ml\data\iris.csv")
print(df.head())

x=df[['sepal_length','sepal_width','petal_width']]
y=df['petal_length']
x_test,x_train,y_test,y_train=train_test_split(x,y,test_size=0.30,random_state=39)

model=LinearRegression()
model.fit(x_train,y_train)
y_pred=model.predict(x_test)

print(model.intercept_)
print(model.coef_)
print(mean_squared_error(y_test,y_pred))
print(r2_score(y_test,y_pred))

plt.scatter(y_test,y_pred,color='blue',label='prediced vs  actual ')
plt.plot([y_test.min(),y_test.max()],[y_test.min(),y_test.max()],'r--',label='ideal fit line')

plt.xlabel("actual")
plt.ylabel("predicted")
plt.legend()
plt.show()