"""
Configuration file for TabNet-IDS
Centralized settings for threat detection, monitoring, and system parameters
"""

import os
from pathlib import Path
from typing import Dict, List, Any
import json

class Config:
    """Configuration class for TabNet-IDS"""
    
    # System paths
    BASE_DIR = Path(__file__).parent
    MODELS_DIR = BASE_DIR / "models"
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    UPLOADS_DIR = BASE_DIR / "uploads"
    
    # Model configuration
    MODEL_CONFIG = {
        "n_d": 64,
        "n_a": 64,
        "n_steps": 5,
        "gamma": 1.5,
        "n_independent": 2,
        "n_shared": 2,
        "lambda_sparse": 1e-4,
        "optimizer_params": {"lr": 2e-2},
        "scheduler_params": {"step_size": 20, "gamma": 0.9},
        "mask_type": "entmax",
        "device_name": "cuda" if os.system("nvidia-smi > /dev/null 2>&1") == 0 else "cpu"
    }
    
    # Training parameters
    TRAINING_CONFIG = {
        "max_epochs": 100,
        "patience": 10,
        "batch_size": 1024,
        "virtual_batch_size": 128,
        "num_workers": 0,
        "drop_last": False,
        "pin_memory": True,
        "seed": 42
    }
    
    # Feature configuration
    NUMERIC_FEATURES = [
        'duration', 'src_bytes', 'dst_bytes', 'wrong_fragment', 'urgent',
        'hot', 'num_failed_logins', 'logged_in', 'num_compromised',
        'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
        'rerror_rate', 'same_srv_rate', 'diff_srv_rate'
    ]
    
    CATEGORICAL_FEATURES = {
        'protocol_type': ['tcp', 'udp', 'icmp'],
        'service': ['http', 'smtp', 'ftp', 'ssh', 'dns', 'telnet', 'finger', 'domain', 'auth'],
        'flag': ['SF', 'S0', 'REJ', 'RSTR', 'RSTO', 'SH', 'RSTOS0']
    }
    
    # Attack type definitions
    ATTACK_TYPES = {
        'dos': {
            'name': 'Denial of Service',
            'severity': 'CRITICAL',
            'icon': '💥',
            'color': '#ef4444',
            'description': 'Attempts to make a computer or network resource unavailable'
        },
        'probe': {
            'name': 'Network Probe',
            'severity': 'MEDIUM',
            'icon': '🔍',
            'color': '#fbbf24',
            'description': 'Scanning or probing activities to gather information'
        },
        'r2l': {
            'name': 'Remote to Local',
            'severity': 'HIGH',
            'icon': '🚨',
            'color': '#ef4444',
            'description': 'Unauthorized access from remote machine to local machine'
        },
        'u2r': {
            'name': 'User to Root',
            'severity': 'CRITICAL',
            'icon': '⚠️',
            'color': '#ef4444',
            'description': 'Unauthorized access to local superuser privileges'
        },
        'normal': {
            'name': 'Normal Traffic',
            'severity': 'INFO',
            'icon': '✅',
            'color': '#10b981',
            'description': 'Legitimate network traffic'
        }
    }
    
    # Threat detection thresholds
    DETECTION_THRESHOLDS = {
        'confidence_threshold': 0.7,
        'high_risk_threshold': 0.9,
        'medium_risk_threshold': 0.7,
        'low_risk_threshold': 0.5,
        'alert_cooldown_minutes': 5,
        'max_alerts_per_minute': 10
    }
    
    # Real-time monitoring settings
    MONITORING_CONFIG = {
        'buffer_size': 1000,
        'update_interval': 1.0,  # seconds
        'max_events_per_second': 100,
        'alert_retention_hours': 24,
        'statistics_window_minutes': 5
    }
    
    # Data preprocessing settings
    PREPROCESSING_CONFIG = {
        'target_features': 25,
        'scaler_type': 'robust',  # 'standard', 'minmax', 'robust'
        'handle_outliers': True,
        'outlier_threshold': 3.0,
        'missing_value_strategy': 'median'  # 'mean', 'median', 'mode', 'drop'
    }
    
    # Visualization settings
    VIZ_CONFIG = {
        'color_palette': {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#10b981',
            'warning': '#fbbf24',
            'danger': '#ef4444',
            'info': '#3b82f6'
        },
        'chart_theme': 'plotly_dark',
        'animation_duration': 500,
        'max_data_points': 1000
    }
    
    # Security settings
    SECURITY_CONFIG = {
        'max_file_size_mb': 100,
        'allowed_file_types': ['.csv', '.txt', '.json'],
        'enable_file_validation': True,
        'sanitize_user_input': True,
        'max_upload_per_hour': 10
    }
    
    # Logging configuration
    LOGGING_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file_handler': True,
        'console_handler': True,
        'max_file_size_mb': 10,
        'backup_count': 5
    }
    
    # API configuration (if needed)
    API_CONFIG = {
        'enable_api': False,
        'api_key_required': False,
        'rate_limit_per_minute': 60,
        'cors_origins': ['http://localhost:3000']
    }
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.MODELS_DIR,
            cls.DATA_DIR,
            cls.LOGS_DIR,
            cls.UPLOADS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
    @classmethod
    def save_config(cls, filepath: str):
        """Save configuration to JSON file"""
        config_dict = {
            'model_config': cls.MODEL_CONFIG,
            'training_config': cls.TRAINING_CONFIG,
            'numeric_features': cls.NUMERIC_FEATURES,
            'categorical_features': cls.CATEGORICAL_FEATURES,
            'attack_types': cls.ATTACK_TYPES,
            'detection_thresholds': cls.DETECTION_THRESHOLDS,
            'monitoring_config': cls.MONITORING_CONFIG,
            'preprocessing_config': cls.PREPROCESSING_CONFIG,
            'viz_config': cls.VIZ_CONFIG,
            'security_config': cls.SECURITY_CONFIG,
            'logging_config': cls.LOGGING_CONFIG,
            'api_config': cls.API_CONFIG
        }
        
        with open(filepath, 'w') as f:
            json.dump(config_dict, f, indent=2)
            
    @classmethod
    def load_config(cls, filepath: str):
        """Load configuration from JSON file"""
        try:
            with open(filepath, 'r') as f:
                config_dict = json.load(f)
                
            # Update class attributes
            for key, value in config_dict.items():
                if hasattr(cls, key.upper()):
                    setattr(cls, key.upper(), value)
                    
        except FileNotFoundError:
            print(f"Config file {filepath} not found. Using default values.")
        except json.JSONDecodeError as e:
            print(f"Error parsing config file: {e}. Using default values.")
            
    @classmethod
    def get_attack_info(cls, attack_type: str) -> Dict[str, Any]:
        """Get attack type information"""
        return cls.ATTACK_TYPES.get(attack_type, cls.ATTACK_TYPES.get('normal', {}))
        
    @classmethod
    def get_severity_color(cls, severity: str) -> str:
        """Get color for severity level"""
        color_map = {
            'CRITICAL': '#ef4444',
            'HIGH': '#f97316',
            'MEDIUM': '#fbbf24',
            'LOW': '#10b981',
            'INFO': '#3b82f6'
        }
        return color_map.get(severity.upper(), '#6b7280')
        
    @classmethod
    def validate_file(cls, filename: str, file_size: int) -> tuple[bool, str]:
        """
        Validate uploaded file
        
        Returns:
            tuple: (is_valid, error_message)
        """
        # Check file extension
        file_ext = Path(filename).suffix.lower()
        if file_ext not in cls.SECURITY_CONFIG['allowed_file_types']:
            return False, f"File type {file_ext} not allowed. Allowed types: {cls.SECURITY_CONFIG['allowed_file_types']}"
            
        # Check file size
        max_size = cls.SECURITY_CONFIG['max_file_size_mb'] * 1024 * 1024
        if file_size > max_size:
            return False, f"File size exceeds maximum allowed size of {cls.SECURITY_CONFIG['max_file_size_mb']}MB"
            
        return True, ""

# Initialize configuration
Config.create_directories()

# Global configuration instance
config = Config()
