# ⚡ Quick Start - For Your Team

## For Team Members Cloning the Repo

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/data-factory.git
cd data-factory
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Get API Key
1. Go to [console.groq.com](https://console.groq.com/)
2. Sign up (it's free!)
3. Create an API key
4. Copy `.env.example` to `.env`
5. Paste your API key in `.env`

### 4. Run the Pipeline!
```bash
cd Claudedatasets
python pipeline.py https://example.com --max-pages 20
```

### 5. Check Your Output
Look in: `AllDatasets/runs/run_YYYY-MM-DD_HH-MM-SS_XXXXXX/`

You'll find:
- `crawl_raw.jsonl` - Raw scraped data
- `crawl_clean.jsonl` - Cleaned documents  
- `crawl_sliced.jsonl` - Sliced blocks
- `qa_training.jsonl` - **Ready for training!**

---

## Common Commands

### Run with custom settings:
```bash
python pipeline.py https://example.com --max-pages 50 --delay 2.0
```

### Run in interactive mode:
```bash
python pipeline.py
# It will ask you for the URL
```

### Check what's installed:
```bash
pip list
```

### Update dependencies:
```bash
pip install -r requirements.txt --upgrade
```

---

## Working on Features

### Create a new branch:
```bash
git checkout -b feature/my-cool-feature
```

### Make changes, then:
```bash
git add .
git commit -m "Add: description of changes"
git push origin feature/my-cool-feature
```

### Then open a Pull Request on GitHub!

---

## Need Help?

- Check the main [README.md](README.md)
- Read [CONTRIBUTING.md](CONTRIBUTING.md)
- Open an issue on GitHub
- Ask in the team chat!

---

**Happy coding!** 🚀

