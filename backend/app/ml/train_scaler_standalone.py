"""
Standalone script to fit and save a StandardScaler for clinical data.
Does not depend on cv2 or other image processing libraries.
"""
import os
import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

def fit_clinical_scaler(csv_path: str, output_path: str) -> StandardScaler:
    """
    Fit a StandardScaler on the clinical dataset and save it.
    """
    df = pd.read_csv(csv_path)
    # Use only the feature columns (exclude target TenYearCHD)
    feature_cols = [c for c in df.columns if c != "TenYearCHD"]
    X = df[feature_cols].values
    
    scaler = StandardScaler()
    scaler.fit(X)
    
    joblib.dump(scaler, output_path)
    print(f"Scaler saved to {output_path}")
    return scaler

if __name__ == "__main__":
    # Path to the clinical dataset (from workspace root: data/patient_heart_parameters.csv)
    # From backend/app/ml, we need to go up three levels
    csv_path = "../../../data/patient_heart_parameters.csv"
    output_path = "clinical_scaler.pkl"
    
    if not os.path.exists(csv_path):
        print(f"Error: Dataset not found at {csv_path}")
        print("Please ensure the CSV file exists in the data directory.")
        sys.exit(1)
    
    print(f"Fitting scaler on {csv_path}...")
    scaler = fit_clinical_scaler(csv_path, output_path)
    
    # Test the scaler
    loaded_scaler = joblib.load(output_path)
    print(f"Scaler fitted successfully. Mean shape: {loaded_scaler.mean_.shape}, Scale shape: {loaded_scaler.scale_.shape}")
    print(f"Scaler saved to {os.path.abspath(output_path)}")
    
    # Show sample transformation
    sample = df.iloc[0][feature_cols].values.reshape(1, -1)
    transformed = loaded_scaler.transform(sample)
    print(f"\nSample row (original): {sample[0]}")
    print(f"Sample row (scaled): {transformed[0]}")