# Streamlit Cloud Deployment Guide

## 1. Create Streamlit Cloud Account
- Go to https://share.streamlit.io
- Sign in with GitHub

## 2. Deploy Your App
1. Click "Create app"
2. Select repository: `Upwork-API-Technical-Support-Bot`
3. Select branch: `main`
4. Set main file path: `app.py`
5. Click "Deploy"

## 3. Add Secrets
Once deployed, add your secrets in the app dashboard:

1. Click the menu (≡) in the top right
2. Select "Settings"
3. Go to "Secrets"
4. Add this to secrets:

```
DEEPINFRA_API_KEY = "your_actual_api_key_here"
```

## 4. Troubleshooting

### If build fails:
- Check GitHub for any uncommitted changes
- Verify requirements.txt has no syntax errors
- Clear app cache: In app menu → Manage app → Reboot app

### If app runs but shows errors:
- Check terminal logs in Manage app
- Verify DEEPINFRA_API_KEY is set correctly in secrets
- Try asking a question about OAuth (definitely in docs)

## 5. Test Questions
- "What is OAuth 2.0?" ✅ Should answer
- "How do I set up API authentication?" ✅ Should answer
- "What is the rate limit?" ❌ Should say "I'm sorry..."
