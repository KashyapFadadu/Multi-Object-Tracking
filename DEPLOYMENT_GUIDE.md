# 🚀 Multi Object Tracking - Deployment Guide

This guide helps you deploy the project to Streamlit Cloud using the current repository structure.

## Recommended Platform: Streamlit Cloud ⭐

Streamlit Cloud is a solid free option for this project because:

- ✅ Auto-deploys directly from GitHub
- ✅ Supports Python and Streamlit apps
- ✅ Gives you a live shareable link
- ✅ Easy to update by pushing commits

---

## Step 1: Prepare Your GitHub Repository

### 1.1 Create a GitHub Account

- Go to https://github.com/signup
- Create a GitHub account if you don't have one

### 1.2 Create a Public Repository

1. Go to https://github.com/new
2. Name the repo `Multi-Object-Tracking` or another name you prefer
3. Make it **Public**
4. Click **Create repository**

### 1.3 Push Your Code

Open PowerShell in the project folder and run:

```powershell
# Initialize git if needed
git init
git add .
git commit -m "Initial commit: Multi Object Tracking"
git branch -M main
git remote add origin https://github.com/KashyapFadadu/Multi-Object-Tracking.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Step 2: Verify Project Files

Your repo should include the files below:

- `app.py` — Main Streamlit application
- `centroid_tracker.py` — Tracking algorithm
- `requirements.txt` — Dependencies for deployment
- `.streamlit/config.toml` — Streamlit settings
- `README.md` — Project documentation
- `DEPLOYMENT_GUIDE.md` — Deployment instructions
- `.gitignore` — Files to ignore in Git
- `yolov5s.pt` — YOLOv5 weights file

### 2.1 Keep `yolov5s.pt` in the repository

Because `app.py` loads `yolov5s.pt` directly, the model weights must be present during deployment. Do not ignore this file in `.gitignore`.

### 2.2 Update `.gitignore`

A good `.gitignore` for this project includes:

```gitignore
.git/
.gitignore

# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
env/
.venv/
*.egg-info/
build/
dist/
.downloads/
.DS_Store
Thumbs.db
*.lnk
*.log
.streamlit/secrets.toml
```

> Important: Do not ignore `yolov5s.pt` if you depend on the local weights file.

---

## Step 3: Check Dependencies

Make sure `requirements.txt` includes the packages needed by your app:

- `streamlit`
- `opencv-python-headless`
- `numpy`
- `torch`
- `torchvision`
- `yolov5`
- `scipy`
- `Pillow`

If you added extra packages, include them here too.

---

## Step 4: Deploy to Streamlit Cloud

### 4.1 Sign in to Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Authorize Streamlit to access your repos

### 4.2 Create the app

1. Click **Create app**
2. Select your GitHub repository
3. Choose branch `main`
4. Set the main file path to `app.py`
5. Click **Deploy**

### 4.3 Live app URL

After deployment, your app will be available at:

```
https://YOUR_USERNAME-multi-object-tracking.streamlit.app
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Step 5: Run Locally First

Before deploying, test locally:

```powershell
cd "f:\Project\Multi Object Tracking"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py --logger.level=error
```

This ensures the app works before you deploy.

---

## Step 6: Share Your Project

### Resume example

```
Live Demo: https://YOUR_USERNAME-multi-object-tracking.streamlit.app
GitHub: https://github.com/YOUR_USERNAME/Multi-Object-Tracking
```

### LinkedIn example

> Check out my Multi Object Tracking app built with YOLOv5 and Streamlit. Upload a video, watch live tracking, and download processed output.

---

## Troubleshooting

### ❌ `ModuleNotFoundError`

- Confirm the package names in `requirements_deploy.txt`
- Check file names and imports

### ❌ `yolov5s.pt not found`

- Make sure `yolov5s.pt` is committed to GitHub
- If the file is not in the repo, update `app.py` to load a remote weights path instead

### ❌ App is slow or times out

- Use shorter videos
- Use lower-resolution inputs
- Streamlit Cloud free tier has limited CPU and memory

---

## Notes

- The app displays live tracking frames while processing
- The app saves an annotated output video for download
- The app counts unique tracked objects by class

**You're ready to deploy.**
