import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import xgboost as xgb
import mlflow

# 1. Start MLflow Autologging
mlflow.autolog()

# 2. Set the active experiment name
mlflow.set_experiment("XGBoost_Autolog_Diabetes")

def main():
    # 3. Load Data from a reliable raw GitHub URL (Standard Pima Indians Diabetes Dataset)
    data_url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    
    # Define explicit column names since this standard file doesn't have a header row
    column_names = [
        "Pregnancies", "Glucose", "BloodPressure", "SkinThickness", 
        "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"
    ]
    
    print("Downloading Diabetes data...")
    df = pd.read_csv(data_url, names=column_names)
    
    # Features (X) and Target variable (y - 'Outcome')
    X = df.drop(["Outcome"], axis=1)
    y = df["Outcome"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Build a Scikit-Learn Pipeline combining Scaling and XGBoost
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', xgb.XGBClassifier(
            max_depth=4, 
            learning_rate=0.05, 
            n_estimators=150, 
            eval_metric='logloss',
            random_state=42
        ))
    ])
    
    # 5. Start a run and train the model
    with mlflow.start_run(run_name="pipeline_autolog_run"):
        print("Training Scikit-Learn Pipeline with XGBoost...")
        pipeline.fit(X_train, y_train)
        
        # Evaluate model performance
        score = pipeline.score(X_test, y_test)
        print(f"Model Test Accuracy: {score:.4f}")
        print("Done! Check your browser dashboard by running 'mlflow ui' in your terminal.")

if __name__ == "__main__":
    main()