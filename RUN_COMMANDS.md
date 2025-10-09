# TabNet-IDS - Run Commands

## ✅ Correct Commands to Use

### 1. Test Preprocessing
```powershell
python src/preprocessing.py
```

### 2. Train the IDS Model
```powershell
python src/train_ids.py
```

### 3. Run Streamlit Dashboard (Use python -m)
```powershell
python -m streamlit run app.py
```

## 🔧 Troubleshooting

### Issue: "streamlit is not recognized"
**Solution:** Use `python -m streamlit` instead of just `streamlit`

### Issue: "could not convert string to float: 'tcp'"
**Solution:** Fixed! Categorical features are now automatically detected and encoded

### Issue: "NameError: name 'load_data' is not defined"
**Solution:** Use the new `train_ids.py` file instead of `train.py`

## 📊 Expected Output

### After preprocessing:
- Sample dataset created with 1000 samples
- Features encoded (categorical → one-hot)
- SMOTE applied for class balance
- ~40-50 features after encoding

### After training:
- Model trains for up to 100 epochs
- Early stopping with patience=20
- Accuracy: 85-95% (on sample data)
- Model saved to `models/tabnet_ids_model.zip`
- Explainability report in `results/explainability/`

## 🚀 Quick Start (Full Pipeline)

```powershell
# Step 1: Create sample data and test preprocessing
python src/preprocessing.py

# Step 2: Train the model
python src/train_ids.py

# Step 3: Run dashboard (after model is trained)
python -m streamlit run app.py
```

## 📝 Notes

- The sample dataset has 5 classes: normal, dos, probe, r2l, u2r
- Training takes 2-5 minutes on CPU
- GPU training is 5-10x faster if available
- Streamlit dashboard requires trained model in `models/` directory
