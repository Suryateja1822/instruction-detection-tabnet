"""
Data Preprocessing Module for TabNet-IDS
Handles data loading, cleaning, feature engineering, and SMOTE oversampling
"""

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from typing import Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class IDSPreprocessor:
    """
    Preprocessor for network intrusion detection datasets
    Supports NSL-KDD, CIC-IDS2017, and CSE-CIC-IDS2018 formats
    """
    
    def __init__(self, dataset_type: str = 'NSL-KDD'):
        """
        Initialize preprocessor
        
        Args:
            dataset_type: Type of dataset ('NSL-KDD', 'CIC-IDS2017', 'CSE-CIC-IDS2018')
        """
        self.dataset_type = dataset_type
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = None
        self.categorical_features = []
        
    def load_nsl_kdd(self, train_path: str, test_path: Optional[str] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load NSL-KDD dataset
        
        Args:
            train_path: Path to training data
            test_path: Path to test data (optional)
            
        Returns:
            Training and test dataframes
        """
        # NSL-KDD column names
        columns = [
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
            'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
            'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
            'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
            'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
            'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
            'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
            'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
            'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
            'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'label', 'difficulty'
        ]
        
        train_df = pd.read_csv(train_path, names=columns)
        test_df = pd.read_csv(test_path, names=columns) if test_path else None
        
        # Remove difficulty level
        train_df = train_df.drop('difficulty', axis=1)
        if test_df is not None:
            test_df = test_df.drop('difficulty', axis=1)
        
        self.categorical_features = ['protocol_type', 'service', 'flag']
        
        return train_df, test_df
    
    def load_cic_ids(self, data_path: str) -> pd.DataFrame:
        """
        Load CIC-IDS2017 or CSE-CIC-IDS2018 dataset
        
        Args:
            data_path: Path to CSV file
            
        Returns:
            Dataframe with loaded data
        """
        df = pd.read_csv(data_path)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Handle common label column names
        label_cols = ['Label', 'label', 'Attack', 'attack']
        for col in label_cols:
            if col in df.columns:
                df = df.rename(columns={col: 'label'})
                break
        
        # Detect categorical columns automatically
        for col in df.columns:
            if col != 'label' and df[col].dtype == 'object':
                if col not in self.categorical_features:
                    self.categorical_features.append(col)
        
        # Remove infinite and NaN values
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna()
        
        return df
    
    def encode_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Encode categorical features using one-hot encoding
        
        Args:
            df: Input dataframe
            
        Returns:
            Dataframe with encoded features
        """
        if self.categorical_features:
            df = pd.get_dummies(df, columns=self.categorical_features, drop_first=True)
        
        return df
    
    def normalize_features(self, X_train: np.ndarray, X_test: Optional[np.ndarray] = None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Normalize features using StandardScaler
        
        Args:
            X_train: Training features
            X_test: Test features (optional)
            
        Returns:
            Normalized training and test features
        """
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test) if X_test is not None else None
        
        return X_train_scaled, X_test_scaled
    
    def encode_labels(self, y: pd.Series, binary: bool = False) -> np.ndarray:
        """
        Encode labels
        
        Args:
            y: Label series
            binary: If True, convert to binary (normal vs attack)
            
        Returns:
            Encoded labels
        """
        if binary:
            # Binary classification: normal (0) vs attack (1)
            y_binary = y.apply(lambda x: 0 if 'normal' in str(x).lower() else 1)
            return y_binary.values
        else:
            # Multi-class classification
            return self.label_encoder.fit_transform(y)
    
    def apply_smote(self, X: np.ndarray, y: np.ndarray, sampling_strategy: str = 'auto') -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply SMOTE oversampling for imbalanced data
        
        Args:
            X: Features
            y: Labels
            sampling_strategy: SMOTE sampling strategy
            
        Returns:
            Resampled features and labels
        """
        print(f"Original dataset shape: {X.shape}")
        print(f"Original class distribution: {np.bincount(y)}")
        
        smote = SMOTE(sampling_strategy=sampling_strategy, random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X, y)
        
        print(f"Resampled dataset shape: {X_resampled.shape}")
        print(f"Resampled class distribution: {np.bincount(y_resampled)}")
        
        return X_resampled, y_resampled
    
    def preprocess_pipeline(
        self,
        data_path: str,
        test_path: Optional[str] = None,
        test_size: float = 0.2,
        binary_classification: bool = False,
        apply_smote: bool = True,
        random_state: int = 42
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Complete preprocessing pipeline
        
        Args:
            data_path: Path to training data
            test_path: Path to test data (optional)
            test_size: Test split ratio if test_path is None
            binary_classification: Binary or multi-class classification
            apply_smote: Whether to apply SMOTE
            random_state: Random seed
            
        Returns:
            X_train, X_test, y_train, y_test
        """
        print(f"Loading {self.dataset_type} dataset...")
        
        # Load data
        if self.dataset_type == 'NSL-KDD':
            train_df, test_df = self.load_nsl_kdd(data_path, test_path)
        else:
            train_df = self.load_cic_ids(data_path)
            test_df = None
        
        # Separate features and labels
        X = train_df.drop('label', axis=1)
        y = train_df['label']
        
        # Encode categorical features
        X = self.encode_categorical(X)
        self.feature_names = X.columns.tolist()
        
        # Encode labels
        y = self.encode_labels(y, binary=binary_classification)
        
        # Split data if no separate test set
        if test_df is None:
            X_train, X_test, y_train, y_test = train_test_split(
                X.values, y, test_size=test_size, random_state=random_state, stratify=y
            )
        else:
            X_train = X.values
            y_train = y
            X_test = self.encode_categorical(test_df.drop('label', axis=1)).values
            y_test = self.encode_labels(test_df['label'], binary=binary_classification)
        
        # Normalize features
        X_train, X_test = self.normalize_features(X_train, X_test)
        
        # Apply SMOTE to training data
        if apply_smote:
            print("\nApplying SMOTE oversampling...")
            X_train, y_train = self.apply_smote(X_train, y_train)
        
        print(f"\nFinal shapes:")
        print(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
        print(f"X_test: {X_test.shape}, y_test: {y_test.shape}")
        print(f"Number of features: {X_train.shape[1]}")
        print(f"Number of classes: {len(np.unique(y_train))}")
        
        return X_train, X_test, y_train, y_test
    
    def get_class_names(self) -> list:
        """Get class names"""
        if hasattr(self.label_encoder, 'classes_'):
            return self.label_encoder.classes_.tolist()
        return []
    
    def get_feature_names(self) -> list:
        """Get feature names"""
        return self.feature_names if self.feature_names else []


def create_sample_dataset(output_path: str = 'data/raw/sample_network_data.csv', n_samples: int = 1000):
    """
    Create a sample network traffic dataset for testing
    
    Args:
        output_path: Output file path
        n_samples: Number of samples to generate
    """
    np.random.seed(42)
    
    # Generate synthetic network features
    data = {
        'duration': np.random.exponential(10, n_samples),
        'src_bytes': np.random.exponential(1000, n_samples),
        'dst_bytes': np.random.exponential(1000, n_samples),
        'wrong_fragment': np.random.poisson(0.1, n_samples),
        'urgent': np.random.poisson(0.05, n_samples),
        'hot': np.random.poisson(0.5, n_samples),
        'num_failed_logins': np.random.poisson(0.1, n_samples),
        'logged_in': np.random.binomial(1, 0.7, n_samples),
        'num_compromised': np.random.poisson(0.05, n_samples),
        'count': np.random.poisson(50, n_samples),
        'srv_count': np.random.poisson(30, n_samples),
        'serror_rate': np.random.beta(2, 5, n_samples),
        'srv_serror_rate': np.random.beta(2, 5, n_samples),
        'rerror_rate': np.random.beta(2, 5, n_samples),
        'same_srv_rate': np.random.beta(5, 2, n_samples),
        'diff_srv_rate': np.random.beta(2, 5, n_samples),
        'protocol_type': np.random.choice(['tcp', 'udp', 'icmp'], n_samples, p=[0.7, 0.2, 0.1]),
        'service': np.random.choice(['http', 'ftp', 'smtp', 'ssh', 'dns'], n_samples),
        'flag': np.random.choice(['SF', 'S0', 'REJ', 'RSTR'], n_samples, p=[0.6, 0.2, 0.1, 0.1])
    }
    
    # Generate labels (70% normal, 30% attacks)
    attack_types = ['normal', 'dos', 'probe', 'r2l', 'u2r']
    labels = np.random.choice(attack_types, n_samples, p=[0.7, 0.15, 0.08, 0.05, 0.02])
    data['label'] = labels
    
    # Create dataframe
    df = pd.DataFrame(data)
    
    # Save to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Sample dataset created: {output_path}")
    print(f"Shape: {df.shape}")
    print(f"Label distribution:\n{df['label'].value_counts()}")


if __name__ == "__main__":
    # Create sample dataset for testing
    create_sample_dataset()
    
    # Test preprocessing with proper categorical handling
    preprocessor = IDSPreprocessor(dataset_type='CIC-IDS2017')
    
    # Set categorical features for the sample dataset
    preprocessor.categorical_features = ['protocol_type', 'service', 'flag']
    
    X_train, X_test, y_train, y_test = preprocessor.preprocess_pipeline(
        data_path='data/raw/sample_network_data.csv',
        binary_classification=False,
        apply_smote=True
    )
    
    print("\nPreprocessing completed successfully!")
    print(f"Feature names: {len(preprocessor.get_feature_names())} features")
    print(f"Class names: {preprocessor.get_class_names()}")
