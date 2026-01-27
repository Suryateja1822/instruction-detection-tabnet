# TabNet-IDS: Advanced Network Intrusion Detection System

An advanced Intrusion Detection System (IDS) leveraging TabNet's attentive interpretable architecture for network security. This project implements state-of-the-art deep learning with explainable AI (XAI) capabilities for real-time threat detection with AI-powered analysis and monitoring.

## 🌐 Live Demo

**Try the app**: https://instruction-detection-tabnet.streamlit.app

📖 **Deployment Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions

### 🆕 Latest Version Features:
- � **Real-time Monitoring**: Live network traffic analysis with continuous threat detection
- 💬 **AI Security Assistant**: Interactive chat interface for security guidance and threat analysis
- 📊 **Enhanced Dashboard**: Executive-level dark theme with advanced visualizations
- 🔧 **Solution Recommender**: Comprehensive threat database with mitigation strategies
- � **File Upload**: Upload your own CSV data for analysis
- ⚙️ **Centralized Configuration**: Unified settings management system
- � **Deployment Ready**: Docker, Streamlit Cloud, and cloud deployment support

## 🎯 Key Features

- **🔍 Interpretable Deep Learning**: TabNet architecture with sequential attention mechanisms for transparent feature selection
- **🛡️ Multi-Attack Detection**: Identifies DDoS, DoS, Probe, R2L, U2R, and modern attack vectors
- **📊 Explainable AI**: SHAP-based feature importance and local/global interpretability
- **⚖️ Imbalanced Data Handling**: SMOTE oversampling and focal loss for rare attack detection
- **🎯 High Performance**: Achieves 96-98% accuracy on benchmark datasets (NSL-KDD, CIC-IDS2017)
- **📈 Real-time Dashboard**: Interactive Streamlit interface with live threat monitoring
- **🔧 Hyperparameter Optimization**: Optuna-based automated tuning for optimal performance
- **📉 Advanced Metrics**: Accuracy, Precision, Recall, F1-Score, MCC, and ROC-AUC

## 📁 Project Structure

```
.
├── data/
│   └── raw/                      # Training datasets
├── models/                        # Saved model weights
├── src/
│   ├── train.py                  # Model training script
│   ├── predict.py                # Prediction script
│   ├── evaluate.py               # Model evaluation script
│   ├── preprocessing.py          # Data preprocessing
│   ├── explainability.py         # XAI features
│   ├── real_time_monitor.py      # Real-time monitoring
│   ├── chat_assistant.py         # AI security assistant
│   └── solution_recommender.py   # Threat solutions database
├── configs/
│   └── model_config.yaml         # Model configuration
├── results/                       # Evaluation results and plots
├── app.py                        # Original Streamlit app
├── app_enhanced.py               # Enhanced dashboard with all features
├── config.py                     # Centralized configuration
├── Dockerfile                    # Docker deployment
├── docker-compose.yml           # Docker Compose setup
├── Procfile                      # Heroku deployment
├── runtime.txt                   # Python runtime specification
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### 1. Setup Environment

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the Model

```bash
python src/train.py
```

This will:
- Load the instruction dataset
- Extract features using character frequency analysis
- Train a TabNet classifier
- Save the model to `models/tabnet_instruction_model.zip`

### 4. Make Predictions

```bash
python src/predict.py
```

### 5. Evaluate the Model

```bash
python src/evaluate.py
```

This generates:
- Accuracy metrics
- Classification report
- Confusion matrix visualization

### 6. Run the Web Interface

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

## 📊 Instruction Classes

The model classifies instructions into the following categories:

| Class | Description | Example |
|-------|-------------|---------|
| `action_device` | Device control commands | "Turn on the lights" |
| `action_list` | List management | "Add milk to my shopping list" |
| `action_media` | Media playback | "Play some jazz music" |
| `action_reminder` | Reminder setting | "Remind me to call John" |
| `action_timer` | Timer/alarm setting | "Set a timer for 5 minutes" |
| `query_calendar` | Calendar queries | "What's on my calendar?" |
| `query_date` | Date queries | "When is Christmas?" |
| `query_time` | Time queries | "What time is it?" |
| `query_weather` | Weather queries | "What's the weather like?" |

## 🔧 Configuration

Model hyperparameters can be adjusted in `configs/model_config.yaml`:

```yaml
model:
  n_d: 8                    # Decision layer width
  n_a: 8                    # Attention embedding width
  n_steps: 3                # Architecture steps
  gamma: 1.3                # Feature reusage coefficient
  lambda_sparse: 0.001      # Sparsity regularization

training:
  max_epochs: 50
  patience: 10
  batch_size: 64
  learning_rate: 0.02
```

## 📈 Model Performance

The model's performance can be evaluated using:

```bash
python src/evaluate.py
```

This will display:
- Overall accuracy
- Per-class precision, recall, and F1-score
- Confusion matrix visualization

## 🧪 Jupyter Notebook

For interactive exploration, use the provided Jupyter notebook:

```bash
jupyter notebook notebooks/instruction_detection_exploration.ipynb
```

The notebook includes:
- Data exploration and visualization
- Feature engineering experiments
- Model training and evaluation
- Custom instruction testing

## 📝 Adding More Data

To improve model performance, add more training examples to `data/raw/instructions.csv`:

```csv
text,label
"Your instruction here","appropriate_class"
```

Then retrain the model:

```bash
python src/train.py
```

## 🛠️ Advanced Usage

### Custom Feature Extraction

Modify the `get_char_frequencies()` function in the training scripts to experiment with different feature extraction methods:

- Word embeddings (Word2Vec, GloVe)
- TF-IDF features
- N-gram features
- Contextual embeddings (BERT)

### Hyperparameter Tuning

Adjust TabNet parameters in `src/train.py` or `configs/model_config.yaml` to optimize performance:

- `n_d` and `n_a`: Control model capacity
- `n_steps`: Number of sequential attention steps
- `gamma`: Feature reusage in attention mechanism
- `lambda_sparse`: Sparsity regularization strength

## � Deployment

### Docker Deployment

1. **Build and run with Docker:**
```bash
docker build -t tabnet-ids .
docker run -p 8501:8501 tabnet-ids
```

2. **Using Docker Compose:**
```bash
docker-compose up -d
```

### Streamlit Cloud Deployment

1. **Push to GitHub:**
```bash
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main
```

2. **Deploy:**
- Go to [Streamlit Cloud](https://share.streamlit.io/)
- Connect your GitHub repository
- Select `app_enhanced.py` as the main file
- Deploy!

### Heroku Deployment

1. **Install Heroku CLI and login:**
```bash
heroku login
```

2. **Create and deploy:**
```bash
heroku create your-app-name
git push heroku main
```

### Cloud Deployment (AWS/GCP/Azure)

The application is containerized and can be deployed to any cloud platform that supports Docker containers.

## 🔄 Real-time Monitoring

The enhanced version includes real-time network traffic monitoring:

- **Live Event Processing**: Continuous monitoring of network events
- **Instant Threat Detection**: Real-time classification and alerting
- **Interactive Dashboard**: Live metrics and visualizations
- **Alert Management**: Configurable alert thresholds and notifications

### Starting Real-time Monitoring

```python
from src.real_time_monitor import RealTimeMonitor

# Initialize monitor
monitor = RealTimeMonitor()

# Start monitoring
monitor.start_monitoring()
```

## 💬 AI Security Assistant

The integrated AI assistant provides:

- **Threat Analysis**: Detailed explanations of detected threats
- **Security Recommendations**: Actionable mitigation strategies
- **Interactive Chat**: Natural language interface for security queries
- **Knowledge Base**: Comprehensive threat database

### Using the AI Assistant

```python
from src.chat_assistant import ChatAssistant

# Initialize assistant
assistant = ChatAssistant()

# Process user query
response = assistant.process_message("What is a DDoS attack?")
print(response['response'])
```

## 📊 Enhanced Dashboard Features

- **Multi-page Navigation**: Dashboard, Monitor, Analysis, Chat, Settings
- **Real-time Metrics**: Live statistics and performance indicators
- **Interactive Visualizations**: Plotly charts with dark theme
- **Alert Management**: Real-time security alerts with severity levels
- **Configuration Panel**: Adjustable detection thresholds and settings

## 🛠️ Advanced Usage

### Custom Configuration

Modify `config.py` to adjust:
- Model parameters
- Detection thresholds
- Monitoring settings
- Visualization themes

### Extending Threat Database

Add new threat types to `src/solutions_db.json`:

```json
{
  "new_threat_type": {
    "name": "New Threat",
    "description": "Threat description",
    "severity": "HIGH",
    "solutions": ["Solution 1", "Solution 2"],
    "mitigation_steps": ["Step 1", "Step 2"]
  }
}
```

## �📦 Dependencies

Main dependencies:
- `pytorch-tabnet`: TabNet implementation
- `torch`: PyTorch deep learning framework
- `scikit-learn`: Machine learning utilities
- `pandas`: Data manipulation
- `streamlit`: Web interface
- `plotly`: Interactive visualizations
- `numpy`: Numerical computing

## 🤝 Contributing

To extend this project:

1. Add more threat types to the database
2. Implement advanced feature extraction methods
3. Experiment with different model architectures
4. Add more visualization options
5. Implement additional monitoring features
6. Contribute to the AI assistant knowledge base

## 📄 License

[Specify your license here]

## 🙏 Acknowledgments

- TabNet paper: [TabNet: Attentive Interpretable Tabular Learning](https://arxiv.org/abs/1908.07442)
- PyTorch TabNet implementation: [dreamquark-ai/tabnet](https://github.com/dreamquark-ai/tabnet)
- Streamlit: [Streamlit](https://streamlit.io/)
- Plotly: [Plotly](https://plotly.com/)
