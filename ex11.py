import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import xgboost as xgb
import mlflow

# 1. Enable MLflow Autologging (tracks parameters, metrics, and models automatically)
mlflow.autolog()

# 2. Set the experiment name
mlflow.set_experiment("XGBoost_Wine_With_Plots")

def main():
    # 3. Load the built-in Wine Dataset
    print("Loading Wine dataset...")
    wine = load_wine()
    
    X = pd.DataFrame(wine.data, columns=wine.feature_names)
    y = wine.target  # 3 classes of wine
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # 4. Create a Pipeline with Scaling and XGBoost
    # Note: multi:softprob is used by default by XGBClassifier for multi-class tasks
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', xgb.XGBClassifier(
            max_depth=3,
            learning_rate=0.1,
            n_estimators=100,
            eval_metric='mlogloss',
            random_state=42
        ))
    ])
    
    # 5. Start MLflow run
    with mlflow.start_run(run_name="xgboost_pipeline_run") as run:
        print("Training XGBoost Pipeline...")
        pipeline.fit(X_train, y_train)
        
        # Evaluate performance
        test_accuracy = pipeline.score(X_test, y_test)
        print(f"Model Test Accuracy: {test_accuracy:.4f}")
        
        # 6. Use Matplotlib to plot Feature Importance
        print("Generating feature importance plot...")
        model = pipeline.named_steps['classifier']
        
        # Get importance weights and map them to the original feature names
        importances = pd.Series(model.feature_importances_, index=wine.feature_names)
        importances = importances.sort_values(ascending=True)
        
        plt.figure(figsize=(10, 6))
        importances.plot(kind='barh', color='skyblue')
        plt.title('XGBoost - Feature Importances (Wine Dataset)')
        plt.xlabel('Relative Importance')
        plt.tight_layout()
        
        # Save the plot locally
        plot_path = "feature_importance.png"
        plt.savefig(plot_path)
        plt.close() # Close the figure to free up memory
        
        # Log the matplotlib figure manually into MLflow artifacts
        mlflow.log_artifact(plot_path)
        print(f"Saved and logged plot to MLflow: {plot_path}")
        
        print("\nAll done! Run 'mlflow ui' in your terminal to see the results.")

if __name__ == "__main__":
    main()