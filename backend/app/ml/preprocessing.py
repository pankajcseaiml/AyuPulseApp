import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms

# Hardcoded means and stds for the 15 clinical parameters
# Feature order: [gender, age, currentSmoker, cigsPerDay, BPMeds, prevalentStroke,
#                 prevalentHyp, diabetes, totChol, sysBP, diaBP, BMI, heartRate, glucose, CP]
CLINICAL_MEANS = np.array([0.43, 49.58, 0.49, 9.0, 0.03, 0.01, 0.31, 0.03, 236.7, 132.35, 82.89, 25.8, 75.87, 81.96, 0.5])
CLINICAL_STDS = np.array([0.49, 8.57, 0.5, 11.92, 0.17, 0.07, 0.46, 0.16, 44.59, 22.03, 11.91, 4.08, 12.02, 23.95, 0.8])

def preprocess_clinical_data(clinical_dict: dict) -> np.ndarray:
    """
    Validates and preprocesses clinical data.
    """
    # Define expected order
    features = [
        "gender", "age", "currentSmoker", "cigsPerDay", "BPMeds", 
        "prevalentStroke", "prevalentHyp", "diabetes", "totChol", 
        "sysBP", "diaBP", "BMI", "heartRate", "glucose", "CP"
    ]
    
    # Range validation
    validations = {
        "age": (1, 120),
        "sysBP": (60, 250),
        "diaBP": (30, 150),
        "totChol": (100, 600),
        "BMI": (10, 60),
        "heartRate": (30, 200),
        "glucose": (40, 400),
    }
    
    for key, (min_val, max_val) in validations.items():
        val = clinical_dict.get(key)
        if val is not None:
            if not (min_val <= val <= max_val):
                raise ValueError(f"Value for {key} ({val}) is out of reasonable range ({min_val}-{max_val})")
    
    # Extract values in correct order
    try:
        raw_values = [float(clinical_dict[f]) for f in features]
    except KeyError as e:
        raise ValueError(f"Missing clinical parameter: {e}")
        
    raw_array = np.array(raw_values)
    
    # Normalize
    normalized = (raw_array - CLINICAL_MEANS) / (CLINICAL_STDS + 1e-8)
    
    # Return shape (1, 15)
    return normalized.reshape(1, 15)

def preprocess_image(image_path: str) -> torch.Tensor:
    """
    Loads, resizes, and normalizes an image for the CNN models.
    """
    image = Image.open(image_path).convert('RGB')
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    tensor = transform(image)
    return tensor.unsqueeze(0)  # Shape (1, 3, 224, 224)