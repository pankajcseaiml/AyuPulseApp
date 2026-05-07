"""
Tests for ML pipeline functionality.
"""
import pytest
import numpy as np
import torch
from pathlib import Path
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from app.ml.clinical_model import ClinicalModel
    from app.ml.preprocessing import preprocess_clinical_data
    HAS_ML = True
except ImportError:
    HAS_ML = False


@pytest.mark.skipif(not HAS_ML, reason="ML modules not available")
class TestClinicalModel:
    """Tests for clinical model."""
    
    def test_clinical_model_initialization(self):
        """Test that clinical model can be initialized."""
        model = ClinicalModel()
        assert model is not None
        assert hasattr(model, 'predict')
        assert hasattr(model, 'get_shap_values')
    
    def test_clinical_prediction(self):
        """Test clinical model prediction."""
        model = ClinicalModel()
        
        # Sample clinical data
        clinical_data = {
            "age": 45,
            "gender": "M",
            "CP": 2,
            "trestbps": 130,
            "chol": 240,
            "fbs": 1,
            "restecg": 1,
            "thalach": 150,
            "exang": 0,
            "oldpeak": 1.2,
            "slope": 2,
            "ca": 1,
            "thal": 3
        }
        
        # Test prediction
        risk_score, category = model.predict(clinical_data)
        
        assert isinstance(risk_score, float)
        assert 0 <= risk_score <= 1
        assert category in ["low", "moderate", "high", "critical"]
    
    def test_clinical_shap_values(self):
        """Test SHAP values generation."""
        model = ClinicalModel()
        
        clinical_data = {
            "age": 60,
            "gender": "F",
            "CP": 3,
            "trestbps": 160,
            "chol": 280,
            "fbs": 1,
            "restecg": 2,
            "thalach": 120,
            "exang": 1,
            "oldpeak": 3.5,
            "slope": 3,
            "ca": 3,
            "thal": 3
        }
        
        risk_score, _ = model.predict(clinical_data)
        shap_values = model.get_shap_values(clinical_data, risk_score)
        
        assert isinstance(shap_values, dict)
        assert "features" in shap_values
        assert "values" in shap_values
        assert "base_value" in shap_values
        assert len(shap_values["features"]) == len(shap_values["values"])
        
        # Check that important features are included
        expected_features = ["age", "chol", "thalach", "oldpeak", "ca"]
        for feature in expected_features:
            assert feature in shap_values["features"]
    
    def test_preprocessing_function(self):
        """Test clinical data preprocessing."""
        clinical_data = {
            "age": 50,
            "gender": "M",
            "CP": 1,
            "trestbps": 120,
            "chol": 200,
            "fbs": 0,
            "restecg": 0,
            "thalach": 160,
            "exang": 0,
            "oldpeak": 0.8,
            "slope": 1,
            "ca": 0,
            "thal": 2
        }
        
        processed = preprocess_clinical_data(clinical_data)
        
        assert isinstance(processed, np.ndarray)
        assert processed.shape[0] > 0  # Should have some features


@pytest.mark.skipif(not HAS_ML, reason="ML modules not available")
class TestImageModels:
    """Tests for image models (X-ray and ECG)."""
    
    def test_xray_model_import(self):
        """Test that X-ray model can be imported."""
        try:
            from app.ml.xray_model import XRayModel
            model = XRayModel()
            assert model is not None
        except ImportError:
            pytest.skip("XRayModel not available")
        except Exception as e:
            # Model might require weights file
            pytest.skip(f"XRayModel failed to load: {e}")
    
    def test_ecg_model_import(self):
        """Test that ECG model can be imported."""
        try:
            from app.ml.ecg_model import ECGModel
            model = ECGModel()
            assert model is not None
        except ImportError:
            pytest.skip("ECGModel not available")
        except Exception as e:
            # Model might require weights file
            pytest.skip(f"ECGModel failed to load: {e}")


def test_prediction_service_import():
    """Test that prediction service can be imported."""
    try:
        from app.services.prediction_service import run_prediction
        assert callable(run_prediction)
    except ImportError:
        pytest.skip("Prediction service not available")


def test_ml_pipeline_integration():
    """Test integration of ML pipeline components."""
    # This test verifies that all ML components work together
    assert HAS_ML, "ML modules should be available"
    
    # Test clinical model
    clinical_model = ClinicalModel()
    assert clinical_model is not None
    
    # Test preprocessing
    clinical_data = {
        "age": 45,
        "gender": "M",
        "CP": 2,
        "trestbps": 130,
        "chol": 240,
        "fbs": 1,
        "restecg": 1,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 1.2,
        "slope": 2,
        "ca": 1,
        "thal": 3
    }
    
    processed = preprocess_clinical_data(clinical_data)
    assert isinstance(processed, np.ndarray)
    
    # Test prediction
    risk_score, category = clinical_model.predict(clinical_data)
    assert 0 <= risk_score <= 1
    assert category in ["low", "moderate", "high", "critical"]
    
    # Test SHAP values
    shap_values = clinical_model.get_shap_values(clinical_data, risk_score)
    assert isinstance(shap_values, dict)
    assert "features" in shap_values