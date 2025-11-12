from sklearn.linear_model import LinearRegression
import numpy as np
x=np.array([[1000,1500,2000,2500,3000]]).reshape(-1,1)
y=np.array([150,200,250,300,350])
print (x.shape)
print(y.shape)
model=LinearRegression()
model.fit(x,y)
print("slope(m):",model.coef_[0])
print("intercept(c):",model.intercept_)
print("prediction for 4000 sqft",model.predict([[4000]])[0])
