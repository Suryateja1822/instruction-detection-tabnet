"""
TabNet-IDS Training Module
Implements training with focal loss, SMOTE, and advanced optimization
"""

import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from pytorch_tabnet.tab_model import TabNetClassifier
from sklearn.metrics import accuracy_score, classification_report, matthews_corrcoef
from preprocessing import IDSPreprocessor
from explainability import TabNetExplainer
import yaml
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class FocalLoss(nn.Module):
    """
    Focal Loss for handling class imbalance
    Focuses on hard-to-classify examples
    """
    def __init__(self, alpha=1, gamma=2):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        
    def forward(self, inputs, targets):
        ce_loss = nn.CrossEntropyLoss(reduction='none')(inputs, targets)
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        return focal_loss.mean()

def train(
    data_path: str = "data/raw/sample_network_data.csv",
    dataset_type: str = "CIC-IDS2017",
    binary_classification: bool = False,
    use_focal_loss: bool = True,
    apply_smote: bool = True,
    config_path: str = "configs/model_config.yaml"
):
    """
    Train TabNet-IDS model
    
    Args:
        data_path: Path to training data
        dataset_type: Type of dataset
        binary_classification: Binary or multi-class
        use_focal_loss: Use focal loss for imbalanced data
        apply_smote: Apply SMOTE oversampling
        config_path: Path to configuration file
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    torch.manual_seed(42)
    
    print("="*70)
    print("TabNet-IDS Training")
    print("="*70)
    
    # Load configuration
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {
            'model': {
                'n_d': 64,
                'n_a': 64,
                'n_steps': 5,
                'gamma': 1.5,
                'lambda_sparse': 0.001,
                'mask_type': 'entmax'
            },
            'training': {
                'max_epochs': 100,
                'patience': 20,
                'batch_size': 1024,
                'virtual_batch_size': 128,
                'learning_rate': 0.02
            }
        }
    
    # Initialize preprocessor
    print(f"\n1. Preprocessing {dataset_type} dataset...")
    preprocessor = IDSPreprocessor(dataset_type=dataset_type)
    
    # Preprocess data
    X_train, X_test, y_train, y_test = preprocessor.preprocess_pipeline(
        data_path=data_path,
        binary_classification=binary_classification,
        apply_smote=apply_smote
    )
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
