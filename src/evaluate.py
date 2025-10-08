import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from pytorch_tabnet.tab_model import TabNetClassifier
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(data_path):
    """Load and preprocess the instruction dataset"""
    data = pd.read_csv(data_path)
    X = data['text'].values
    y = data['label'].values
    return X, y

def preprocess_text(texts):
    """Simple text preprocessing"""
    return [str(text).lower() for text in texts]

def get_char_frequencies(texts):
    """Extract character frequency features"""
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789 ,.!?'
    char_to_idx = {c: i for i, c in enumerate(chars)}
    
    features = np.zeros((len(texts), len(chars)))
    
    for i, text in enumerate(texts):
        for c in str(text).lower():
            if c in char_to_idx:
                features[i, char_to_idx[c]] += 1
        
        if len(text) > 0:
            features[i] /= len(text)
            
    return features

def evaluate_model():
    """Evaluate the trained TabNet model"""
    
    # Load data
    data_path = "data/raw/instructions.csv"
    print(f"Loading data from {data_path}...")
    X, y = load_data(data_path)
    
    # Preprocess
    X_processed = preprocess_text(X)
    
    # Split data
    test_size = 0.2 if len(X) > 20 else 0.1
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=test_size, random_state=42, 
        stratify=y if len(np.unique(y)) > 1 else None
    )
    
    # Extract features
    X_test_feat = get_char_frequencies(X_test)
    
    # Load model
    model_path = "models/tabnet_instruction_model.zip"
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        print("Please train the model first using train.py")
        return
    
    print("Loading model...")
    clf = TabNetClassifier()
    clf.load_model(model_path)
    
    # Make predictions
    print("Making predictions...")
    y_pred = clf.predict(X_test_feat)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n" + "="*60)
    print("MODEL EVALUATION RESULTS")
    print("="*60)
    print(f"\nTest Accuracy: {accuracy:.4f}")
    print(f"Number of test samples: {len(y_test)}")
    print(f"Number of classes: {len(np.unique(y))}")
    
    print("\n" + "-"*60)
    print("CLASSIFICATION REPORT")
    print("-"*60)
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Confusion matrix
    print("\n" + "-"*60)
    print("CONFUSION MATRIX")
    print("-"*60)
    cm = confusion_matrix(y_test, y_pred)
    
    # Get unique labels
    labels = np.unique(np.concatenate([y_test, y_pred]))
    
    # Create confusion matrix plot
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    # Save plot
    os.makedirs('results', exist_ok=True)
    plot_path = 'results/confusion_matrix.png'
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\nConfusion matrix saved to {plot_path}")
    
    # Show some example predictions
    print("\n" + "-"*60)
    print("EXAMPLE PREDICTIONS")
    print("-"*60)
    for i in range(min(5, len(X_test))):
        print(f"\nText: {X_test[i]}")
        print(f"True label: {y_test[i]}")
        print(f"Predicted: {y_pred[i]}")
        print(f"Correct: {'✓' if y_test[i] == y_pred[i] else '✗'}")

if __name__ == "__main__":
    evaluate_model()
