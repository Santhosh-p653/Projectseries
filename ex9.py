import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import mlflow
import mlflow.xgboost

# 1. Set up MLflow Experiment
mlflow.set_experiment("XGBoost_Wine_Quality")

def main():
    # 2. Load Data directly from raw GitHub URL
    # Using the Wine Quality dataset (Red Wine)
    data_url = "https://raw.githubusercontent.com/mlflow/mlflow/master/tests/datasets/winequality-red.csv"
    
    print("Downloading data...")
    df = pd.read_csv(data_url, sep=";")
    
    # Split features and target (quality)
    X = df.drop(["quality"], axis=1)
    y = df["quality"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Define Model Parameters
    params = {
        "max_depth": 5,
        "learning_rate": 0.1,
        "n_estimators": 100,
        "objective": "reg:squarederror",
        "random_state": 42
    }
    
    # 4. Start MLflow Run
    with mlflow.start_run(run_name="xgboost_base_run"):
        print("Training model...")
        
        # Initialize and train XGBoost Regressor
        model = xgb.XGBRegressor(**params)
        model.fit(X_train, y_train)
        
        # Predictions
        predictions = model.fit(X_train, y_train).predict(X_test)
        
        # 5. Evaluate Metrics
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)
        
        print(block_txt := f"Metrics - RMSE: {rmse:.4f}, R2: {r2:.4f}")
        
        # 6. Log Parameters and Metrics to MLflow
        mlflow.log_params(params)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        
        # 7. Create and Log Matplotlib Plot
        plt.figure(figsize=(8, 6))
        plt.scatter(y_test, predictions, alpha=0.5, color='crimson')
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
        plt.xlabel('Actual Quality')
        plt.ylabel('Predicted Quality')
        plt.title('Actual vs Predicted Wine Quality')
        
        # Save plot locally first
        plot_path = "residuals_plot.png"
        plt.savefig(plot_path)
        plt.close()
        
        # Log the plot as an artifact
        mlflow.log_artifact(plot_path)
        
        # Clean up local plot file
        if os.path.exists(plot_path):
            os.remove(plot_path)
            
        # 8. Log the Trained Model
        mlflow.xgboost.log_model(model, artifact_path="models")
        
        print("Run successfully logged to MLflow!")

if __name__ == "__main__":
    main()