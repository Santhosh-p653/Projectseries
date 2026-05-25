import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,accuracy_score
from sklearn.preprocessing import StandardScaler


raw_url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
cols=['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigree','Age','Outcome']
df =pd.read_csv(raw_url,names=cols)
print(df.head())



zero_cols=['Glucose','BloodPressure','SkinThickness','Insulin','BMI']
for col in zero_cols:
	df[col]=df[col].replace(0,np.nan)
df.fillna(df.median(),inplace=True)
print("Missing values handled")



X=df.drop('Outcome',axis=1)
y=df['Outcome']


X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
print(f"Training Dataset size:{X_train.shape}")
print (f"Testing Dataset size:{X_test.shape}")



model=RandomForestClassifier(n_estimators=200,random_state=50)
model.fit(X_train,y_train)


predictions=model.predict(X_test)
acc=accuracy_score(y_test,predictions)
print(f"Diabetes Prediction Accuracy:{acc*100:.2f}%\n")
print ("Full Performance Report")
print(classification_report(y_test,predictions))



scaler=StandardScaler()
X_train_scaled=scaler.fit_transform(X_train)
X_test_scaled=scaler.fit_transform(X_test)


optimized_model=RandomForestClassifier(n_estimators=300,max_depth=8,class_weight="balanced",random_state=42)

predictions=optimized_model.fit(X_train_scaled,y_train)
predictions=optimized_model.predict(X_test_scaled)

acc=accuracy_score(y_test,predictions)
print(f"Optimized Model Accuracy:{acc*100:.2f}%\n")

