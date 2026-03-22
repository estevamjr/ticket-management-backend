import joblib
import os
import numpy as np

class AndonPredictor:
    def __init__(self):
        # Localiza o arquivo .pkl dentro da pasta ml_logic
        base_path = os.path.dirname(__file__)
        model_path = os.path.join(base_path, 'modelo_andon.pkl')
        
        try:
            self.model = joblib.load(model_path)
            print("✨ AI Model 'modelo_andon.pkl' loaded successfully!")
        except Exception as e:
            print(f"⚠️ Error loading AI Model: {e}")
            self.model = None

    def predict(self, cpu, ram, threats, untrusted):
        if self.model is None:
            return None
        
        # Formata os dados para o padrão que o Scikit-Learn espera (Matriz 1x4)
        features = np.array([[cpu, ram, threats, untrusted]])
        prediction = self.model.predict(features)
        
        return int(prediction[0])