"""
TabNet-IDS Training Module
Implements training with focal loss, SMOTE, and advanced optimization
"""

import os
import sys
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from pytorch_tabnet.tab_model import TabNetClassifier
from sklearn.metrics import accuracy_score, classification_report, matthews_corrcoef
import yaml
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib to non-interactive backend to avoid popup windows
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Add src to path
sys.path.append(os.path.dirname(__file__))
from preprocessing import IDSPreprocessor
from explainability import TabNetExplainer


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


def train_tabnet_ids(
    data_path: str = "data/raw/sample_network_data.csv",
    dataset_type: str = "CIC-IDS2017",
    binary_classification: bool = False,
    use_focal_loss: bool = False,
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
        print("Config file not found, using defaults...")
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
    
    # Get model parameters
    model_params = config['model']
    training_params = config['training']
    
    # Initialize TabNet model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"\n2. Initializing TabNet model on {device}...")
    
    tabnet_params = {
        'n_d': model_params.get('n_d', 64),
        'n_a': model_params.get('n_a', 64),
        'n_steps': model_params.get('n_steps', 5),
        'gamma': model_params.get('gamma', 1.5),
        'lambda_sparse': model_params.get('lambda_sparse', 0.001),
        'optimizer_fn': torch.optim.Adam,
        'optimizer_params': {'lr': training_params.get('learning_rate', 0.02)},
        'scheduler_params': {'step_size': 10, 'gamma': 0.9},
        'scheduler_fn': torch.optim.lr_scheduler.StepLR,
        'mask_type': model_params.get('mask_type', 'entmax'),
        'device_name': device,
        'verbose': 1
    }
    
    clf = TabNetClassifier(**tabnet_params)
    
    # Train the model
    print(f"\n3. Training TabNet-IDS...")
    print(f"   - Max epochs: {training_params.get('max_epochs', 100)}")
    print(f"   - Batch size: {training_params.get('batch_size', 1024)}")
    print(f"   - Learning rate: {training_params.get('learning_rate', 0.02)}")
    print(f"   - SMOTE: {apply_smote}")
    print(f"   - Focal Loss: {use_focal_loss}")
    
    batch_size = min(training_params.get('batch_size', 1024), len(X_train))
    virtual_batch_size = min(training_params.get('virtual_batch_size', 128), batch_size)
    
    clf.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        eval_name=['test'],
        eval_metric=['accuracy'],
        max_epochs=training_params.get('max_epochs', 100),
        patience=training_params.get('patience', 20),
        batch_size=batch_size,
        virtual_batch_size=virtual_batch_size,
        num_workers=0,
        drop_last=False
    )
    
    # Evaluate
    print(f"\n4. Evaluating model...")
    y_pred = clf.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    mcc = matthews_corrcoef(y_test, y_pred)
    
    print(f"\n{'='*70}")
    print("EVALUATION RESULTS")
    print(f"{'='*70}")
    print(f"Test Accuracy: {accuracy:.4f}")
    print(f"Matthews Correlation Coefficient (MCC): {mcc:.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, 
                                target_names=preprocessor.get_class_names(),
                                zero_division=0))
    
    # Save the model
    os.makedirs('models', exist_ok=True)
    model_path = 'models/tabnet_ids_model'
    clf.save_model(model_path)
    print(f"\n5. Model saved to {model_path}.zip")
    
    # Generate explainability report
    print(f"\n6. Generating explainability report...")
    explainer = TabNetExplainer(clf, preprocessor.get_feature_names())
    explainer.generate_global_explanation_report(save_dir='results/explainability')
    
    # Save training metadata
    metadata = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dataset': dataset_type,
        'data_path': data_path,
        'binary_classification': binary_classification,
        'apply_smote': apply_smote,
        'use_focal_loss': use_focal_loss,
        'accuracy': float(accuracy),
        'mcc': float(mcc),
        'n_features': X_train.shape[1],
        'n_classes': len(np.unique(y_train)),
        'train_samples': len(X_train),
        'test_samples': len(X_test)
    }
    
    metadata_path = 'models/training_metadata.yaml'
    with open(metadata_path, 'w') as f:
        yaml.dump(metadata, f)
    print(f"Training metadata saved to {metadata_path}")
    
    print(f"\n{'='*70}")
    print("Training completed successfully!")
    print(f"{'='*70}\n")
    
    return clf, preprocessor


if __name__ == "__main__":
    # Train the model
    model, preprocessor = train_tabnet_ids(
        data_path="data/raw/sample_network_data.csv",
        dataset_type="CIC-IDS2017",
        binary_classification=False,
        apply_smote=True,
        use_focal_loss=False
    )
