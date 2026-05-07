import numpy as np

def fuse(clinical_score: float, xray_score: float = None, ecg_score: float = None) -> dict:
    base_weights = {"clinical": 0.50, "xray": 0.30, "ecg": 0.20}
    
    # Identify available modalities
    scores = {"clinical": clinical_score}
    if xray_score is not None:
        scores["xray"] = xray_score
    if ecg_score is not None:
        scores["ecg"] = ecg_score
        
    modalities_used = list(scores.keys())
    
    # Calculate total weight of available modalities
    total_available_weight = sum(base_weights[m] for m in modalities_used)
    
    # Redistribute weights
    weights_used = {m: base_weights[m] / total_available_weight for m in modalities_used}
    
    # Calculate final score
    final_score = sum(scores[m] * weights_used[m] for m in modalities_used)
    
    # Calculate risk category
    if final_score < 0.3:
        risk_category = "Low"
    elif final_score <= 0.7:
        risk_category = "Medium"
    else:
        risk_category = "High"
        
    # Calculate confidence
    num_modalities = len(modalities_used)
    if num_modalities == 1:
        confidence = 0.65
    elif num_modalities == 2:
        s1, s2 = list(scores.values())
        confidence = 0.75 + (1 - abs(s1 - s2)) * 0.15
    else:
        # 3 modalities
        std_dev = np.std(list(scores.values()))
        confidence = 0.80 + (1 - std_dev) * 0.15
        
    return {
        "final_score": float(final_score),
        "risk_category": risk_category,
        "confidence": float(confidence),
        "weights_used": weights_used,
        "modalities_used": modalities_used
    }