import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from pytorch_tabnet.tab_model import TabNetClassifier
import torch

def load_data(data_path):
    """
    Load and preprocess the instruction dataset
    """
    # TODO: Replace with your actual data loading logic
    # This is a placeholder example
    data = pd.read_csv(data_path)
    
    # Assuming the data has 'text' and 'label' columns
    X = data['text'].values
    y = data['label'].values
    
    return X, y

def preprocess_text(texts, max_length=100):
    """
    Simple text preprocessing
    """
    # TODO: Implement your text preprocessing here
    # This is a placeholder - you might want to use more sophisticated preprocessing
    processed_texts = [str(text).lower() for text in texts]
    return processed_texts

def train():
    # Set random seed for reproducibility
    np.random.seed(42)
    torch.manual_seed(42)
    
    # Load and preprocess data
    data_path = "data/raw/instructions.csv"  # Update this path
    print(f"Loading data from {data_path}...")
    X, y = load_data(data_path)
    print(f"Loaded {len(X)} samples")
    print(f"Unique classes: {np.unique(y)}")
    
    # Preprocess text
    X_processed = preprocess_text(X)
    
    # Split data (adjust test_size for small datasets)
    test_size = 0.2 if len(X) > 20 else 0.1
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=test_size, random_state=42, stratify=y if len(np.unique(y)) > 1 else None
    )
    print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")
    
    # TODO: Implement feature extraction for TabNet
    # For now, we'll use a simple character-level encoding as an example
    # In practice, you might want to use word embeddings or other features
    
    # Example: Simple character frequency features
    def get_char_frequencies(texts):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789 ,.!?'
        char_to_idx = {c: i for i, c in enumerate(chars)}
        
        features = np.zeros((len(texts), len(chars)))
        
        for i, text in enumerate(texts):
            for c in str(text).lower():
                if c in char_to_idx:
                    features[i, char_to_idx[c]] += 1
            
            # Normalize by text length
            if len(text) > 0:
                features[i] /= len(text)
                
        return features
    
    print("Extracting features...")
    X_train_feat = get_char_frequencies(X_train)
    X_test_feat = get_char_frequencies(X_test)
    print(f"Feature shape: {X_train_feat.shape}")
    
    # Initialize TabNet model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    tabnet_params = {
        'n_d': 8,
        'n_a': 8,
        'n_steps': 3,
        'gamma': 1.3,
        'lambda_sparse': 1e-3,
        'optimizer_fn': torch.optim.Adam,
        'optimizer_params': {'lr': 2e-2},
        'scheduler_params': {'step_size': 10, 'gamma': 0.9},
        'scheduler_fn': torch.optim.lr_scheduler.StepLR,
        'mask_type': 'entmax',
        'device_name': device
    }
    
    clf = TabNetClassifier(**tabnet_params)
    
    # Train the model
    print("\nStarting training...")
    batch_size = min(64, len(X_train))  # Adjust batch size for small datasets
    clf.fit(
        X_train_feat, y_train,
        eval_set=[(X_test_feat, y_test)],
        eval_name=['valid'],
        eval_metric=['accuracy'],
        max_epochs=50,
        patience=10,
        batch_size=batch_size,
        virtual_batch_size=min(32, batch_size),
        num_workers=0,
        drop_last=False
    )
    
    # Evaluate
    print("\nEvaluating model...")
    y_pred = clf.predict(X_test_feat)
    print("\nTest Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Save the model
    os.makedirs('models', exist_ok=True)
    model_path = 'models/tabnet_instruction_model'
    clf.save_model(model_path)
    print(f"\nModel saved to {model_path}.zip")
    print("Training complete!")

if __name__ == "__main__":
    train()
