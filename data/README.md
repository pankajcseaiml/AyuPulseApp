# Data Directory

This directory contains sample data for the AyuPulseApp project.

## Structure

- `patient_heart_parameters.csv` - Clinical data for patients
- `ecg/` - ECG image datasets
  - `train/` - Training ECG images
    - `ECG Images of Myocardial Infarction Patients (240x12=2880)/` - MI patient ECG images
    - `Normal Person ECG Images (284x12=3408)/` - Normal ECG images
  - `test/` - Test ECG images
- `xray/` - Chest X-ray images
  - `false/` - Non-cardiac condition X-rays
  - `true/` - Cardiac condition X-rays

## Usage

These datasets are used for:
1. Demo/testing of the ML pipeline
2. Training dummy models (in current implementation)
3. Providing sample data for prediction endpoints

## Notes

- The current ML models are dummy implementations that don't actually use this data
- For production, trained models would be stored separately
- File paths with parentheses are from the original dataset sources