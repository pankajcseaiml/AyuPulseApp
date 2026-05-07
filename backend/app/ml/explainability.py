def generate_explanation(clinical_data: dict, shap_values: dict, fusion_result: dict) -> dict:
    # 1. shap_features
    display_names = {
        "gender": "Gender",
        "age": "Age",
        "currentSmoker": "Current Smoker",
        "cigsPerDay": "Cigarettes/Day",
        "BPMeds": "BP Medication",
        "prevalentStroke": "History of Stroke",
        "prevalentHyp": "Hypertension",
        "diabetes": "Diabetes",
        "totChol": "Total Cholesterol",
        "sysBP": "Systolic BP",
        "diaBP": "Diastolic BP",
        "BMI": "BMI",
        "heartRate": "Heart Rate",
        "glucose": "Blood Glucose",
        "CP": "Chest Pain Type"
    }

    # Calculate total absolute shap sum for contribution percentage
    total_abs_shap = sum(abs(v) for v in shap_values.values())
    
    shap_features = []
    for name, shap_val in shap_values.items():
        val = clinical_data.get(name)
        contribution_pct = (abs(shap_val) / total_abs_shap * 100) if total_abs_shap > 0 else 0
        direction = "positive" if shap_val > 0 else "negative"
        
        shap_features.append({
            "name": name,
            "display_name": display_names.get(name, name),
            "value": val,
            "shap_value": float(shap_val),
            "contribution_pct": float(contribution_pct),
            "direction": direction
        })
        
    shap_features.sort(key=lambda x: abs(x["shap_value"]), reverse=True)

    # 2. clinical_reference_ranges
    ranges_config = {
        "sysBP": {"min": 90, "max": 120, "unit": "mmHg"},
        "diaBP": {"min": 60, "max": 80, "unit": "mmHg"},
        "totChol": {"min": 0, "max": 200, "unit": "mg/dL"}, # normal < 200
        "BMI": {"min": 18.5, "max": 24.9, "unit": "kg/m²"},
        "glucose": {"min": 70, "max": 100, "unit": "mg/dL"},
        "heartRate": {"min": 60, "max": 100, "unit": "bpm"},
        "age": {"min": 18, "max": 65, "unit": "years"},
        "cigsPerDay": {"min": 0, "max": 0, "unit": "cigs/day"},
        # Categorical
        "gender": {"min": 0, "max": 1, "unit": ""},
        "currentSmoker": {"min": 0, "max": 0, "unit": ""},
        "BPMeds": {"min": 0, "max": 0, "unit": ""},
        "prevalentStroke": {"min": 0, "max": 0, "unit": ""},
        "prevalentHyp": {"min": 0, "max": 0, "unit": ""},
        "diabetes": {"min": 0, "max": 0, "unit": ""},
        "CP": {"min": 0, "max": 0, "unit": ""}
    }

    clinical_reference_ranges = {}
    for param, config in ranges_config.items():
        val = clinical_data.get(param, 0)
        
        status = "normal"
        if param in ["sysBP"]:
            if val > 140: status = "high"
            elif val > 120: status = "borderline"
            elif val < 90: status = "low"
        elif param in ["diaBP"]:
            if val > 90: status = "high"
            elif val > 80: status = "borderline"
            elif val < 60: status = "low"
        elif param == "totChol":
            if val > 240: status = "high"
            elif val >= 200: status = "borderline"
        elif param == "BMI":
            if val >= 30: status = "high"
            elif val >= 25: status = "borderline"
            elif val < 18.5: status = "low"
        elif param == "glucose":
            if val > 126: status = "high"
            elif val > 100: status = "borderline"
            elif val < 70: status = "low"
        elif param == "heartRate":
            if val > 100: status = "high"
            elif val < 60: status = "low"
        elif param in ["currentSmoker", "diabetes", "prevalentStroke", "prevalentHyp", "BPMeds"]:
            if val == 1: status = "high"
        
        clinical_reference_ranges[param] = {
            "normal_min": config["min"],
            "normal_max": config["max"],
            "patient_value": val,
            "unit": config["unit"],
            "status": status
        }

    # 3, 4, 5. Explanation, Risk Factors, Recommendations
    risk_factors = []
    recommendations = []
    
    # Analyze elevated factors based on status
    for param, data in clinical_reference_ranges.items():
        if data["status"] in ["high", "borderline"] and param not in ["gender", "age"]:
            display_name = display_names.get(param, param)
            val = data["patient_value"]
            unit = data["unit"]
            risk_factors.append(f"Elevated {display_name} ({val} {unit})")
            
            # Generate specific recommendation
            if param == "sysBP":
                recommendations.append(f"Monitor blood pressure; target {display_name} below 130 mmHg.")
            elif param == "totChol":
                recommendations.append("Consider lifestyle changes or lipid-lowering therapy to manage cholesterol.")
            elif param == "BMI":
                recommendations.append("Aim for a healthy weight through balanced diet and regular physical activity.")
            elif param == "glucose":
                recommendations.append("Monitor blood glucose levels and limit intake of refined sugars.")
            elif param == "currentSmoker":
                recommendations.append("Smoking cessation is highly recommended to reduce cardiovascular risk.")
            elif param == "diabetes":
                recommendations.append("Ensure optimal glycemic control in consultation with your healthcare provider.")
                
    if not recommendations:
        recommendations.append("Maintain current healthy lifestyle habits.")
        recommendations.append("Schedule regular check-ups to monitor cardiovascular health.")
        
    if not risk_factors:
        risk_factors.append("No major elevated clinical risk factors identified.")

    # Top 3 factors based on SHAP
    top_3 = [f["display_name"] for f in shap_features[:3] if f["direction"] == "positive"]
    top_3_str = ", ".join(top_3) if top_3 else "your overall profile"

    risk_cat = fusion_result["risk_category"]
    
    explanation_text = (
        f"Based on your clinical profile, the key factors contributing to your risk assessment are {top_3_str}. "
    )
    
    if "sysBP" in clinical_reference_ranges:
        sys_bp_data = clinical_reference_ranges["sysBP"]
        val = sys_bp_data["patient_value"]
        status = sys_bp_data["status"]
        if status == "normal":
            explanation_text += f"Your Systolic BP of {val} mmHg is within the normal range. "
        else:
            explanation_text += f"Your Systolic BP of {val} mmHg is above the normal range of 90-120 mmHg. "

    explanation_text += f"Overall, the AI models classify your profile as {risk_cat} Risk. "
    
    if recommendations:
        explanation_text += f"It is recommended to {recommendations[0].lower()}"

    return {
        "shap_features": shap_features[:15],
        "clinical_reference_ranges": clinical_reference_ranges,
        "explanation_text": explanation_text,
        "risk_factors": risk_factors,
        "recommendations": recommendations
    }