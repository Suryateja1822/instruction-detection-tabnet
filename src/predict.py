import os
import numpy as np
import pandas as pd
from pytorch_tabnet.tab_model import TabNetClassifier
import torch

def preprocess_text(texts, max_length=100):
    """
    Preprocess text input for prediction
    """
    # This should match the preprocessing used during training
    return [str(text).lower() for text in texts]

def get_char_frequencies(texts):
    """
    Extract character frequency features
    This should match the feature extraction used during training
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789 ,.!?'
    char_to_idx = {c: i for i, c in enumerate(chars)}
    
    features = np.zeros((len(texts), len(chars)))
    
    for i, text in enumerate(texts):
        for c in str(text).lower():
            if c in char_to_idx:
                features[i, char_to_idx[c]] += 1
        
        # Normalize by text length
        if len(str(text)) > 0:
            features[i] /= len(str(text))
            
    return features

class InstructionDetector:
    def __init__(self, model_path):
        """
        Initialize the instruction detector with a pre-trained TabNet model
        """
        self.model = TabNetClassifier()
        # Add .zip extension if not present
        if not model_path.endswith('.zip'):
            model_path = model_path + '.zip'
        self.model.load_model(model_path)
        self.classes_ = self.model.classes_ if hasattr(self.model, 'classes_') else None
    
    def predict(self, texts):
        """
        Predict the class of instruction texts
        
        Args:
            texts: List of instruction texts to classify
            
        Returns:
            List of predicted class labels
        """
        # Preprocess and extract features
        processed_texts = preprocess_text(texts)
        features = get_char_frequencies(processed_texts)
        
        # Make predictions
        predictions = self.model.predict(features)
        
        # If we have class labels, map predictions back to them
        if self.classes_ is not None:
            return [self.classes_[i] for i in predictions]
        return predictions

def main():
    # Example usage
    model_path = "models/tabnet_instruction_model"
    
    if not os.path.exists(model_path + ".zip"):
        print(f"Error: Model not found at {model_path}")
        print("Please train the model first using train.py")
        return
    
    # Initialize the detector
    detector = InstructionDetector(model_path)
    
    # Example instructions to classify
    example_instructions = [
        "Please turn on the lights",
        "What's the weather like today?",
        "Set a timer for 5 minutes",
        "Play some jazz music"
    ]
    
    # Get predictions
    predictions = detector.predict(example_instructions)
    
    # Print results
    print("Instruction Detection Results:")
    print("-" * 50)
    for instr, pred in zip(example_instructions, predictions):
        print(f"Instruction: {instr}")
        print(f"Predicted class: {pred}\n")

if __name__ == "__main__":
    main()
