import numpy as np

class ClinicalModel:
    def __init__(self):
        self.feature_names = [
            "gender", "age", "currentSmoker", "cigsPerDay", "BPMeds", 
            "prevalentStroke", "prevalentHyp", "diabetes", "totChol", 
            "sysBP", "diaBP", "BMI", "heartRate", "glucose", "CP"
        ]
        
    def _calculate_score(self, clinical_data: dict) -> float:
        """Enhanced deterministic scoring function with more realistic risk assessment."""
        # Base risk from Framingham-like factors
        base_risk = 0.15
        
        # Age contribution (non-linear)
        age = clinical_data.get("age", 50)
        age_risk = min(0.4, (max(age, 30) - 30) * 0.01)
        
        # Blood pressure contribution
        sysBP = clinical_data.get("sysBP", 120)
        bp_risk = 0.0
        if sysBP > 180:
            bp_risk = 0.25
        elif sysBP > 160:
            bp_risk = 0.15
        elif sysBP > 140:
            bp_risk = 0.08
        elif sysBP > 130:
            bp_risk = 0.03
            
        # Cholesterol contribution
        totChol = clinical_data.get("totChol", 200)
        chol_risk = 0.0
        if totChol > 280:
            chol_risk = 0.20
        elif totChol > 240:
            chol_risk = 0.10
        elif totChol > 200:
            chol_risk = 0.05
            
        # Diabetes (major risk factor)
        diabetes = clinical_data.get("diabetes", 0)
        diabetes_risk = 0.15 if diabetes == 1 else 0.0
        
        # Smoking
        smoker = clinical_data.get("currentSmoker", 0)
        smoking_risk = 0.12 if smoker == 1 else 0.0
        
        # Hypertension history
        prevalentHyp = clinical_data.get("prevalentHyp", 0)
        hyp_risk = 0.08 if prevalentHyp == 1 else 0.0
        
        # Stroke history
        prevalentStroke = clinical_data.get("prevalentStroke", 0)
        stroke_risk = 0.10 if prevalentStroke == 1 else 0.0
        
        # BMI
        bmi = clinical_data.get("BMI", 25)
        bmi_risk = 0.0
        if bmi >= 35:
            bmi_risk = 0.08
        elif bmi >= 30:
            bmi_risk = 0.05
        elif bmi >= 25:
            bmi_risk = 0.02
            
        # Glucose
        glucose = clinical_data.get("glucose", 100)
        glucose_risk = 0.0
        if glucose > 200:
            glucose_risk = 0.10
        elif glucose > 126:
            glucose_risk = 0.06
        elif glucose > 100:
            glucose_risk = 0.02
            
        # Chest pain
        cp = clinical_data.get("CP", 0)
        cp_risk = 0.04 if cp > 0 else 0.0
        
        # Calculate total risk
        total_risk = base_risk + age_risk + bp_risk + chol_risk + diabetes_risk + \
                    smoking_risk + hyp_risk + stroke_risk + bmi_risk + glucose_risk + cp_risk
        
        # Add interaction effects
        if diabetes == 1 and sysBP > 140:
            total_risk += 0.05  # Diabetes + hypertension synergy
        if smoker == 1 and totChol > 240:
            total_risk += 0.04  # Smoking + high cholesterol synergy
            
        # Normalize to 0-1 range with sigmoid-like transformation
        normalized_risk = 1 / (1 + np.exp(-3 * (total_risk - 0.5)))
        
        # Add deterministic noise based on patient data for realism
        # Use patient data as seed for reproducibility
        seed_val = int(age * 100 + sysBP + totChol)
        np.random.seed(seed_val)
        noise = np.random.normal(0, 0.03)
        
        final_score = np.clip(normalized_risk + noise, 0.01, 0.99)
        return float(final_score)

    def predict(self, clinical_data: dict):
        """Returns (risk_score: float, feature_importances: dict)"""
        score = self._calculate_score(clinical_data)
        
        # Calculate realistic feature importances based on actual contributions
        age = clinical_data.get("age", 50)
        sysBP = clinical_data.get("sysBP", 120)
        totChol = clinical_data.get("totChol", 200)
        diabetes = clinical_data.get("diabetes", 0)
        smoker = clinical_data.get("currentSmoker", 0)
        prevalentHyp = clinical_data.get("prevalentHyp", 0)
        prevalentStroke = clinical_data.get("prevalentStroke", 0)
        bmi = clinical_data.get("BMI", 25)
        glucose = clinical_data.get("glucose", 100)
        cp = clinical_data.get("CP", 0)
        
        # Base importances that sum to 1
        importances = {
            "age": min(0.25, 0.05 + (max(age, 30) - 30) * 0.002),
            "sysBP": 0.12 if sysBP > 140 else (0.08 if sysBP > 130 else 0.05),
            "totChol": 0.10 if totChol > 240 else (0.06 if totChol > 200 else 0.03),
            "diabetes": 0.15 if diabetes == 1 else 0.02,
            "currentSmoker": 0.12 if smoker == 1 else 0.02,
            "prevalentHyp": 0.08 if prevalentHyp == 1 else 0.02,
            "prevalentStroke": 0.10 if prevalentStroke == 1 else 0.01,
            "BMI": 0.06 if bmi >= 30 else (0.03 if bmi >= 25 else 0.01),
            "glucose": 0.08 if glucose > 126 else (0.04 if glucose > 100 else 0.02),
            "CP": 0.04 if cp > 0 else 0.01,
            "diaBP": 0.03,
            "heartRate": 0.02,
            "cigsPerDay": 0.02 if smoker == 1 else 0.01,
            "BPMeds": 0.03,
            "gender": 0.02
        }
        
        # Normalize to sum to 1
        total = sum(importances.values())
        if total > 0:
            importances = {k: v/total for k, v in importances.items()}
        
        return score, importances

    def get_shap_values(self, clinical_data: dict, score: float) -> dict:
        """Returns dict mapping feature name -> shap_value"""
        # We simulate SHAP values by distributing the difference between 
        # the base value (e.g., 0.15) and the predicted score
        # proportionally to the feature's deviation from normal.
        
        base_value = 0.15
        diff = score - base_value
        
        # Simple heuristic to assign SHAP values
        shap_values = {}
        total_abs_weight = 0
        
        # Temporary weights for distribution
        weights = {}
        for feature in self.feature_names:
            val = clinical_data.get(feature, 0)
            # Create a mock deviation metric
            if feature == "age": weight = (val - 50) / 30
            elif feature == "sysBP": weight = (val - 120) / 40
            elif feature == "totChol": weight = (val - 200) / 50
            elif feature == "BMI": weight = (val - 25) / 10
            elif feature == "glucose": weight = (val - 100) / 30
            elif feature in ["diabetes", "currentSmoker", "prevalentHyp", "prevalentStroke"]: 
                weight = 1.0 if val == 1 else -0.2
            else: weight = np.random.normal(0, 0.1)
            
            weights[feature] = weight
            total_abs_weight += abs(weight)
            
        for feature in self.feature_names:
            if total_abs_weight > 0:
                # Distribute the diff
                shap_values[feature] = (weights[feature] / total_abs_weight) * diff
            else:
                shap_values[feature] = 0.0
                
        return shap_values

# Singleton instance
clinical_model_instance = ClinicalModel()