# Instruction Detection using TabNet

This project implements an instruction detection system using TabNet, a deep learning architecture for tabular data. The system classifies instructions into different categories such as device control, queries, reminders, and more.

## 🎯 Features

- **TabNet Architecture**: Utilizes TabNet for interpretable deep learning on tabular features
- **Multiple Instruction Classes**: Supports 9 different instruction categories
- **Web Interface**: Interactive Streamlit app for real-time predictions
- **Comprehensive Evaluation**: Detailed metrics and visualization tools
- **Jupyter Notebooks**: Interactive exploration and experimentation

## 📁 Project Structure

```
.
├── data/
│   └── raw/
│       └── instructions.csv      # Training dataset
├── models/                        # Saved model weights
├── notebooks/                     # Jupyter notebooks for exploration
│   └── instruction_detection_exploration.ipynb
├── src/
│   ├── train.py                  # Model training script
│   ├── predict.py                # Prediction script
│   └── evaluate.py               # Model evaluation script
├── configs/
│   └── model_config.yaml         # Model configuration
├── results/                       # Evaluation results and plots
├── app.py                         # Streamlit web application
├── requirements.txt               # Python dependencies
└── README.md                      # This file
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

## 📦 Dependencies

Main dependencies:
- `pytorch-tabnet`: TabNet implementation
- `torch`: PyTorch deep learning framework
- `scikit-learn`: Machine learning utilities
- `pandas`: Data manipulation
- `streamlit`: Web interface
- `matplotlib/seaborn`: Visualization

## 🤝 Contributing

To extend this project:

1. Add more instruction classes to the dataset
2. Implement advanced feature extraction methods
3. Experiment with different model architectures
4. Add cross-validation for robust evaluation
5. Implement model explainability features

## 📄 License

[Specify your license here]

## 🙏 Acknowledgments

- TabNet paper: [TabNet: Attentive Interpretable Tabular Learning](https://arxiv.org/abs/1908.07442)
- PyTorch TabNet implementation: [dreamquark-ai/tabnet](https://github.com/dreamquark-ai/tabnet)
