#!/usr/bin/env python3
"""
Test script to verify the ML pipeline is working correctly.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend/app'))

from ml.preprocessing import preprocess_clinical_data
from ml.clinical_model import clinical_model_instance
from ml.fusion_model import fuse
from ml.explainability import generate_explanation

def test_ml_pipeline():
    print("Testing ML pipeline...")
    
    # 1. Test clinical data preprocessing
    clinical_data = {
        "gender": 1,
        "age": 55,
        "currentSmoker": 0,
        "cigsPerDay": 0,
        "BPMeds": 0,
        "prevalentStroke": 0,
        "prevalentHyp": 1,
        "diabetes": 0,
        "totChol": 220,
        "sysBP": 140,
        "diaBP": 90,
        "BMI": 28,
        "heartRate": 75,
        "glucose": 110,
        "CP": 0
    }
    
    try:
        preprocessed = preprocess_clinical_data(clinical_data)
        print("[OK] Clinical data preprocessing successful")
        print(f"  Shape: {preprocessed.shape}")
    except Exception as e:
        print(f"[ERROR] Clinical data preprocessing failed: {e}")
        return False
    
    # 2. Test clinical model
    try:
        clinical_score, feature_importances = clinical_model_instance.predict(clinical_data)
        print(f"[OK] Clinical model prediction successful")
        print(f"  Clinical score: {clinical_score:.3f}")
        print(f"  Feature importances: {len(feature_importances)} features")
    except Exception as e:
        print(f"[ERROR] Clinical model failed: {e}")
        return False
    
    # 3. Test fusion model
    try:
        xray_score = 0.35  # dummy values
        ecg_score = 0.25   # dummy values
        fusion_result = fuse(clinical_score, xray_score, ecg_score)
        print(f"[OK] Fusion model successful")
        print(f"  Final score: {fusion_result['final_score']:.3f}")
        print(f"  Risk category: {fusion_result['risk_category']}")
        print(f"  Confidence: {fusion_result['confidence']:.3f}")
    except Exception as e:
        print(f"[ERROR] Fusion model failed: {e}")
        return False
    
    # 4. Test explainability
    try:
        shap_values = clinical_model_instance.get_shap_values(clinical_data, clinical_score)
        explanation_dict = generate_explanation(clinical_data, shap_values, fusion_result)
        print(f"[OK] Explainability module successful")
        print(f"  Explanation text: {explanation_dict['explanation_text'][:100]}...")
        print(f"  Risk factors: {len(explanation_dict['risk_factors'])} factors")
        print(f"  Recommendations: {len(explanation_dict['recommendations'])} recommendations")
        print(f"  Clinical reference ranges: {type(explanation_dict['clinical_reference_ranges'])}")
    except Exception as e:
        print(f"[ERROR] Explainability failed: {e}")
        return False
    
    print("\n[SUCCESS] All ML pipeline components are working correctly!")
    return True

if __name__ == "__main__":
    success = test_ml_pipeline()
    sys.exit(0 if success else 1)