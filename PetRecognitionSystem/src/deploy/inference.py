import torch
from PIL import Image
from src.data.transforms import get_val_transforms
from src.models.net import get_model
import os

class Predictor:
    def __init__(self, config, model_path, device):
        self.device = device
        self.config = config
        
        # Load Model Architecture
        self.model = get_model(config)
        
        # Load Weights
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=device))
        else:
            raise FileNotFoundError(f"Model checkpoint not found at {model_path}")
            
        self.model.to(device)
        self.model.eval()
        
        # Preprocessing
        self.transform = get_val_transforms(config['image_size'])
        self.classes = ['Cat', 'Dog'] # Assuming 0=Cat, 1=Dog based on folder sort order in loader.py

    def predict(self, image_path):
        if not os.path.exists(image_path):
            return {"error": f"Image not found: {image_path}"}
            
        try:
            image = Image.open(image_path).convert('RGB')
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                outputs = self.model(input_tensor)
                # Apply Softmax to get probabilities (0-1)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted_class = torch.max(probabilities, 1)

            result = {
                'class': self.classes[predicted_class.item()],
                'confidence': confidence.item(),
                'probabilities': {
                    'Cat': probabilities[0][0].item(),
                    'Dog': probabilities[0][1].item()
                }
            }
            return result
        except Exception as e:
            return {"error": str(e)}
