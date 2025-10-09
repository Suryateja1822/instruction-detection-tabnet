# 🚀 START HERE - TabNet-IDS Executive Dashboard

## ⚡ 2 Commands to Launch

---

## 1️⃣ First Time? Train the Model

```powershell
python src/train_ids.py
```

⏱️ **Takes:** 2-5 minutes  
✅ **Creates:** Model file + Sample data  
📁 **Saves to:** `models/tabnet_ids_model.zip`

**Run this ONCE!**

---

## 2️⃣ Launch the Dashboard

```powershell
python -m streamlit run app_executive.py
```

🌐 **Opens:** `http://localhost:8501`  
⚡ **Instantly:** Browser opens automatically  
🎨 **Shows:** Premium dark theme dashboard

---

## 🎮 In the Dashboard

### **Click ▶️ START** (in left sidebar)

That's it! Watch real-time threats appear! 🔥

---

## 📊 What You'll See

```
┌─────────────────────────────────────────┐
│  🛡️ TABNET-IDS EXECUTIVE SOC           │
├─────────────────────────────────────────┤
│  [🎯 LIVE] [🚨 ALERTS] [🔒 IPs]        │
├─────────────────────────────────────────┤
│                                         │
│  🔴 💥 DoS Attack    98% Confidence    │
│     192.168.1.100 → 10.0.1.50          │
│                                         │
│  🟡 🔍 Network Probe  87% Confidence   │
│     192.168.1.55 → 10.0.1.100          │
│                                         │
│  🟢 ✅ Normal Traffic 95% Confidence   │
│     192.168.1.200 → 10.0.1.25          │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎯 Quick Actions

### **Block an IP:**
1. Go to **🚨 ACTIVE ALERTS** tab
2. Click **🚫 BLOCK** on any alert
3. Done! IP is blocked

### **View Analytics:**
1. Go to **📈 ANALYTICS** tab
2. See pie charts and graphs
3. Hover for details

### **Reset Everything:**
1. Click **🔄 RESET** in sidebar
2. All data cleared
3. Start fresh!

---

## 🔧 If Something Goes Wrong

### ❌ "Model not found"
```powershell
python src/train_ids.py
```

### ❌ "streamlit is not recognized"
```powershell
python -m streamlit run app_executive.py
```

### ❌ Dashboard not styled properly
- Use **Chrome or Edge** browser
- Press **Ctrl + R** to refresh

---

## 💡 Pro Tips

- Press **F11** for full screen
- Set speed to **2-3 seconds** for smooth demo
- Let it run **30 seconds** to collect data
- Then check **Analytics** tab for charts

---

## 📚 More Help?

- **HOW_TO_USE.md** - Complete guide
- **QUICK_START.md** - 3-step start
- **EXECUTIVE_DASHBOARD_GUIDE.md** - All features

---

## 🎊 Ready? Let's Go!

```powershell
# Step 1: Train (first time only)
python src/train_ids.py

# Step 2: Launch
python -m streamlit run app_executive.py

# Step 3: Click START in sidebar

# Step 4: Enjoy! 🎉
```

---

**Your executive-level intrusion detection system is ready! 🛡️✨**
