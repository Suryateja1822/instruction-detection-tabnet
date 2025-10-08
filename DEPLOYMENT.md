# Deployment Guide

## 🚀 Deploy to Streamlit Cloud (Recommended - FREE)

Streamlit Cloud is the easiest way to deploy your Streamlit app for free!

### Prerequisites
✅ GitHub repository (already done!)
✅ Streamlit app (`app.py`)
✅ `requirements.txt` file

### Step-by-Step Deployment

#### 1. Push Latest Changes to GitHub

```bash
git add .
git commit -m "Add deployment configuration"
git push
```

#### 2. Sign Up for Streamlit Cloud

1. Go to **https://share.streamlit.io/**
2. Click **"Sign up"** or **"Sign in with GitHub"**
3. Authorize Streamlit to access your GitHub repositories

#### 3. Deploy Your App

1. Click **"New app"** button
2. Fill in the deployment form:
   - **Repository**: `Suryateja1822/instruction-detection-tabnet`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom subdomain like `instruction-detection-tabnet`

3. Click **"Deploy!"**

#### 4. Wait for Deployment

- Streamlit Cloud will install dependencies from `requirements.txt`
- This may take 2-5 minutes
- You'll see logs showing the installation progress

#### 5. Access Your App

Once deployed, your app will be available at:
```
https://[your-app-name].streamlit.app
```

For example:
```
https://instruction-detection-tabnet.streamlit.app
```

---

## 🔧 Troubleshooting

### Issue: App Crashes on Startup

**Solution**: Check the logs in Streamlit Cloud dashboard. Common issues:
- Missing dependencies in `requirements.txt`
- Model file too large (>100MB)
- Memory issues

### Issue: Model File Not Found

**Solution**: Ensure `models/tabnet_instruction_model.zip` is committed to GitHub:
```bash
git add models/tabnet_instruction_model.zip
git commit -m "Add trained model"
git push
```

### Issue: Out of Memory

**Solution**: Streamlit Cloud free tier has 1GB RAM limit. If needed:
1. Reduce model size
2. Use model compression
3. Upgrade to Streamlit Cloud paid tier

---

## 🌐 Alternative Deployment Options

### Option 2: Hugging Face Spaces (FREE)

1. Create account at **https://huggingface.co/**
2. Create a new Space
3. Select **Streamlit** as the SDK
4. Upload your files or connect GitHub repo
5. Your app will be live at `https://huggingface.co/spaces/[username]/[space-name]`

**Advantages**:
- Free GPU option available
- Good for ML models
- Easy to share

### Option 3: Render (FREE tier available)

1. Sign up at **https://render.com/**
2. Create new **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Deploy!

### Option 4: Railway (FREE tier available)

1. Sign up at **https://railway.app/**
2. Create new project from GitHub repo
3. Add environment variables if needed
4. Deploy automatically

### Option 5: Heroku (Paid)

Note: Heroku removed free tier in November 2022.

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
3. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```
4. Deploy:
   ```bash
   heroku create
   git push heroku main
   ```

---

## 📊 Deployment Comparison

| Platform | Free Tier | RAM | Storage | Custom Domain | GPU |
|----------|-----------|-----|---------|---------------|-----|
| **Streamlit Cloud** | ✅ Yes | 1GB | Limited | ❌ No | ❌ No |
| **Hugging Face** | ✅ Yes | 16GB | 50GB | ✅ Yes | ✅ Yes (paid) |
| **Render** | ✅ Yes | 512MB | Limited | ✅ Yes | ❌ No |
| **Railway** | ✅ Limited | 512MB | 1GB | ✅ Yes | ❌ No |
| **Heroku** | ❌ No | Varies | Varies | ✅ Yes | ❌ No |

---

## 🔐 Environment Variables (If Needed)

If your app needs API keys or secrets:

### Streamlit Cloud:
1. Go to app settings
2. Click "Secrets"
3. Add your secrets in TOML format:
   ```toml
   API_KEY = "your-api-key"
   ```

### In Code:
```python
import streamlit as st

# Access secrets
api_key = st.secrets["API_KEY"]
```

---

## 📝 Post-Deployment Checklist

After deployment:

- [ ] Test all features of the app
- [ ] Verify model predictions work correctly
- [ ] Check app performance and loading time
- [ ] Share the link with others for testing
- [ ] Add app URL to GitHub repository description
- [ ] Update README.md with live demo link
- [ ] Monitor app usage and errors

---

## 🎯 Recommended: Streamlit Cloud

For this project, **Streamlit Cloud** is recommended because:
- ✅ **Free forever** for public repos
- ✅ **Easy setup** (3 clicks to deploy)
- ✅ **Auto-updates** when you push to GitHub
- ✅ **Built for Streamlit** apps
- ✅ **No configuration** needed
- ✅ **Good documentation** and support

---

## 📱 Sharing Your App

Once deployed, share your app:

1. **Add to README**: Update your GitHub README with:
   ```markdown
   ## 🌐 Live Demo
   
   Try the app: [Instruction Detection App](https://your-app.streamlit.app)
   ```

2. **Social Media**: Share on LinkedIn, Twitter, etc.

3. **Portfolio**: Add to your portfolio/resume

4. **GitHub Topics**: Add `deployed`, `live-demo` topics

---

## 🔄 Updating Your Deployed App

To update your deployed app:

```bash
# Make changes to your code
git add .
git commit -m "Update app features"
git push
```

Streamlit Cloud will automatically redeploy your app!

---

## 📞 Support

- **Streamlit Docs**: https://docs.streamlit.io/
- **Streamlit Forum**: https://discuss.streamlit.io/
- **GitHub Issues**: Report issues in your repo

---

## 🎉 Next Steps After Deployment

1. **Monitor Performance**: Check app analytics in Streamlit Cloud
2. **Gather Feedback**: Share with users and collect feedback
3. **Iterate**: Improve based on user feedback
4. **Scale**: If needed, upgrade to paid tier for more resources
5. **Add Features**: Continuous improvement!

Good luck with your deployment! 🚀
