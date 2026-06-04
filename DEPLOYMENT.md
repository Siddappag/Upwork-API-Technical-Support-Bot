# Streamlit Cloud Deployment Guide

## ✅ Quick Deploy

### 1. Create Streamlit Cloud Account
- Go to https://share.streamlit.io
- Sign in with GitHub

### 2. Deploy App
1. Click **"Create app"**
2. Select your repo: `Siddappag/Upwork-API-Technical-Support-Bot`
3. Select branch: `main`
4. Set main file: `app.py`
5. Click **"Deploy"**

### 3. Add Secrets ⚠️ IMPORTANT
After deployment starts, click the **menu (≡)** in the top right:
1. Select **"Settings"**
2. Go to **"Secrets"**
3. Copy-paste the following and replace with your actual key:

```
DEEPINFRA_API_KEY = "your_actual_deepinfra_api_key"
```

4. Save & app will auto-refresh

---

## 🎯 What's Included
- ✅ **Vector Database**: Pre-embedded (363 MB uploaded)
- ✅ **PDF**: Upwork API documentation included
- ✅ **Configuration**: `.streamlit/config.toml` optimized
- ✅ **Error Handling**: Graceful error messages

---

## 🧪 Test Questions
After deployment, try these:

| Question | Expected | Status |
|----------|----------|--------|
| "What is OAuth 2.0?" | Should answer | ✅ |
| "How do I authenticate?" | Should answer | ✅ |
| "What is the rate limit?" | "I'm sorry..." | ✅ |

---

## 🔧 Troubleshooting

### App won't start ("Oh no. Error running app")
1. Check **Manage app** → **Logs**
2. Likely causes:
   - DEEPINFRA_API_KEY not set in Secrets → Add it now
   - typo in Secrets key → Must be exact: `DEEPINFRA_API_KEY`

### API key error when asking questions
- Go to Secrets and verify key is correct
- Copy from DeepInfra dashboard
- No spaces before/after value

### "Vector database not found"
- Shouldn't happen - it's pre-included
- If error: Click Manage app → Reboot

---

## 📊 Deployment Checklist
- ✅ Fork/Clone repository
- ✅ Vector database included (363 MB)
- ✅ PDF documentation included
- ✅ Requirements.txt compatible
- ✅ .python-version set to 3.11
- ✅ Secrets template provided

**Status: Ready to Deploy** 🚀

