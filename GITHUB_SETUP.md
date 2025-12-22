# 🚀 GitHub Setup Guide - Step by Step

## What You Need to Do on GitHub (5 minutes)

### Step 1: Create a New Repository on GitHub

1. Go to [github.com](https://github.com) and log in
2. Click the **"+"** button in the top right → **"New repository"**
3. Fill in the details:
   - **Repository name:** `data-factory` (or whatever you want)
   - **Description:** "Automated training dataset generator from web content"
   - **Visibility:** Choose **Public** (so your team can see it) or **Private**
   - **DO NOT** check "Initialize with README" (we already have one!)
   - **DO NOT** add .gitignore or license (we have those too!)
4. Click **"Create repository"**

### Step 2: Copy the Repository URL

After creating, GitHub will show you a page with commands. Look for the URL that looks like:
```
https://github.com/YOUR_USERNAME/data-factory.git
```

**COPY THIS URL!** You'll need it in Step 3.

---

## What to Run on Your Computer (2 minutes)

### Step 3: Initialize Git and Push

Open PowerShell in your project folder and run these commands **ONE BY ONE**:

```powershell
# Navigate to your project
cd "C:\Users\Kash Supramos\Desktop\CreatingDatasets"

# Initialize git (creates .git folder)
git init

# Add all files (respects .gitignore)
git add .

# Create first commit
git commit -m "Initial commit: Working pipeline with crawl, clean, slice, and QA generation"

# Set main branch name
git branch -M main

# Connect to GitHub (REPLACE with YOUR URL from Step 2!)
git remote add origin https://github.com/YOUR_USERNAME/data-factory.git

# Push to GitHub!
git push -u origin main
```

**That's it!** Your code is now on GitHub! 🎉

---

## Share with Your Team

Send them this link:
```
https://github.com/YOUR_USERNAME/data-factory
```

They can clone it with:
```bash
git clone https://github.com/YOUR_USERNAME/data-factory.git
```

---

## What's Included in the Repo?

✅ **Included:**
- All your Python scripts (Claudedatasets/)
- README with setup instructions
- requirements.txt for dependencies
- .gitignore (protects secrets)
- CONTRIBUTING guide
- Empty runs/ folder structure

❌ **Excluded (by .gitignore):**
- Your `.env` file (keeps API key safe!)
- `venv/` folder (too big, everyone creates their own)
- `crawl4ai/` folder (separate project)
- All your test runs in `AllDatasets/runs/`
- Any old CSV/JSONL files

---

## Troubleshooting

### "git: command not found"
You need to install Git first:
1. Download from [git-scm.com](https://git-scm.com/download/win)
2. Install with default settings
3. Restart PowerShell
4. Try again

### "Permission denied (publickey)"
Use HTTPS URL instead of SSH:
```
https://github.com/YOUR_USERNAME/data-factory.git
```

### "Updates were rejected"
If the repo already has commits:
```bash
git pull origin main --rebase
git push origin main
```

---

## Next Steps After Pushing

1. ✅ Add a nice description on GitHub
2. ✅ Add topics/tags: `machine-learning`, `dataset-generation`, `web-scraping`, `llm`
3. ✅ Invite your team as collaborators (Settings → Collaborators)
4. ✅ Create your first issue: "Add GUI interface"
5. ✅ Let your team start contributing!

---

**Need help?** Ask me or check the GitHub docs!

