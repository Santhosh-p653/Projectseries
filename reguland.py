import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score

# Set page layout
st.set_page_config(page_title="ReguLand Dashboard", layout="wide")

st.title("🏡 ReguLand: Interactive Real Estate Price Predictor")
st.markdown("""
This app demonstrates the impact of **L1 (Lasso)** and **L2 (Ridge)** regularization on a housing dataset stored locally inside the project.
Regularization helps prevent overfitting by penalizing large coefficients.
""")

# 1. Fetch data from your local data/ folder
@st.cache_data
def load_local_data():
    local_path = os.path.join("data", "AmesHousing.csv")
    if not os.path.exists(local_path):
        st.error(f"Could not find '{local_path}'. Please run your 'download_data.py' script first!")
        st.stop()
        
    df = pd.read_csv(local_path)
    return df

df_raw = load_local_data()

# --- Sidebar Controls ---
st.sidebar.header("🔧 Model Configurations")

target_col = "SalePrice"
# Features matched exactly to the official Inria dataset schema
num_features = ["GrLivArea", "GarageArea", "TotalBsmtSF", "1stFlrSF", "YearBuilt"]
cat_features = ["MSZoning", "HouseStyle"]

st.sidebar.subheader("1. Hyperparameters")
alpha = st.sidebar.slider("Regularization Strength (Alpha)", min_value=0.01, max_value=500.0, value=1.0, step=0.5)
model_type = st.sidebar.radio("Select Model Type", ("Ridge (L2)", "Lasso (L1)"))

# Filter down to selected features and drop target row nulls
df = df_raw[num_features + cat_features + [target_col]].dropna(subset=[target_col])

X = df[num_features + cat_features]
y = df[target_col]

# --- 2. Preprocessing Pipeline with sklearn ---
num_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

cat_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', num_transformer, num_features),
    ('cat', cat_transformer, cat_features)
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 3. Model Training ---
if model_type == "Ridge (L2)":
    model = Ridge(alpha=alpha)
else:
    model = Lasso(alpha=alpha, max_iter=10000)

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', model)
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

# Metrics evaluation
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# --- 4. Streamlit Dashboard Layout ---
col1, col2, col3 = st.columns(3)
col1.metric(label="Selected Model", value=model_type.split()[0])
col2.metric(label="R² Score (Test)", value=f"{r2:.4f}")
col3.metric(label="RMSE", value=f"${rmse:,.2f}")

st.write("---")

plot_col1, plot_col2 = st.columns(2)

with plot_col1:
    st.subheader("📊 Actual vs. Predicted Prices")
    fig, ax = plt.subplots(figsize=(6, 4.5))
    
    # Pure matplotlib scatter plot
    ax.scatter(y_test, y_pred, alpha=0.5, color="#1f77b4", edgecolors='none', s=25)
    
    # Ideal prediction line
    ideal_line = [y_test.min(), y_test.max()]
    ax.plot(ideal_line, ideal_line, color='red', linestyle='--', linewidth=2)
    
    ax.set_xlabel("Actual Price ($)")
    ax.set_ylabel("Predicted Price ($)")
    ax.grid(True, linestyle=':', alpha=0.6)
    st.pyplot(fig)

with plot_col2:
    st.subheader("📉 Feature Coefficients / Weights")
    
    # Extract structural feature names from transformers
    cat_encoder = pipeline.named_steps['preprocessor'].named_transformers_['cat'].named_steps['onehot']
    encoded_cat_features = list(cat_encoder.get_feature_names_out(cat_features))
    all_features = num_features + encoded_cat_features
    
    coefficients = pipeline.named_steps['regressor'].coef_
    
    # Organize data using pandas
    coef_df = pd.DataFrame({
        'Feature': all_features,
        'Coefficient': coefficients
    })
    
    # Sort by absolute impact value but keep original signs for plotting direction
    coef_df['abs_coef'] = coef_df['Coefficient'].abs()
    coef_df = coef_df.sort_values(by='abs_coef', ascending=True).tail(12)  # get top 12
    
    fig2, ax2 = plt.subplots(figsize=(6, 4.5))
    
    # Map colors dynamically based on positive/negative impact values
    colors = ['#d9534f' if c < 0 else '#5cb85c' for c in coef_df['Coefficient']]
    
    # Pure matplotlib horizontal bar chart
    ax2.barh(coef_df['Feature'], coef_df['Coefficient'], color=colors, edgecolor='none')
    
    ax2.axvline(x=0, color='black', linewidth=0.8, linestyle='-')
    ax2.set_xlabel("Weight Value")
    ax2.grid(True, axis='x', linestyle=':', alpha=0.6)
    
    # Layout adjustment to make room for feature labels
    plt.tight_layout()
    st.pyplot(fig2)

with st.expander("🔍 Inspect Processed Data Snippet"):
    st.dataframe(df.head(10))