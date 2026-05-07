"""
Script to fit and save a StandardScaler for clinical data.
Run this once to generate the scaler file.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from preprocessing import fit_clinical_scaler

if __name__ == "__main__":
    # Path to the clinical dataset
    csv_path = "../../data/patient_heart_parameters.csv"
    output_path = "clinical_scaler.pkl"
    
    if not os.path.exists(csv_path):
        print(f"Error: Dataset not found at {csv_path}")
        print("Please ensure the CSV file exists in the data directory.")
        sys.exit(1)
    
    print(f"Fitting scaler on {csv_path}...")
    scaler = fit_clinical_scaler(csv_path, output_path)
    
    # Test the scaler
    import joblib
    loaded_scaler = joblib.load(output_path)
    print(f"Scaler fitted successfully. Mean: {loaded_scaler.mean_.shape}, Scale: {loaded_scaler.scale_.shape}")
    print(f"Scaler saved to {os.path.abspath(output_path)}")