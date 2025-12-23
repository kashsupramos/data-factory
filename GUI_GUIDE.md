# 🎨 GUI Guide - Using the Data Factory Interface

## 🚀 Quick Start

### 1. Install Gradio (if you haven't already)
```bash
pip install gradio
```

### 2. Run the GUI
```bash
python rungui.py
```

### 3. Open Your Browser
The GUI will automatically open at: **http://127.0.0.1:7860**

If it doesn't open automatically, just copy that URL into your browser!

---

## 🎯 How to Use

### Step 1: Enter URL
Type or paste the website URL you want to scrape.
- Must start with `http://` or `https://`
- Example: `https://example.com`

### Step 2: Adjust Settings (Optional)
- **Max Pages**: How many pages to crawl (default: 50)
  - Start with 20-50 for testing
  - Increase for larger datasets
  
- **Delay**: Seconds between requests (default: 1.0)
  - Use 1-2s to be respectful to servers
  - Increase if you get rate limited

### Step 3: Start Pipeline
Click the big **"🚀 Start Pipeline"** button!

### Step 4: Watch Progress
- Status box shows current step
- Progress bar shows completion
- Open "Live Logs" accordion to see terminal output

### Step 5: Download Results
When complete:
- View statistics
- Download any of the 4 output files
- Preview sample Q&A pairs

---

## 📊 Understanding the Output

### Files You Get:

1. **crawl_raw.jsonl**
   - Raw scraped HTML data
   - Includes all metadata
   - Largest file

2. **crawl_clean.jsonl**
   - Cleaned and filtered text
   - Boilerplate removed
   - Ready for processing

3. **crawl_sliced.jsonl**
   - Split into training blocks
   - Optimized chunk sizes
   - Preserves context

4. **qa_training.jsonl** ⭐
   - **This is what you want for training!**
   - Question-answer pairs
   - Ready for LLM fine-tuning

---

## 🎨 Features

### ✅ What's Included:
- Real-time progress tracking
- Step-by-step status updates
- Live terminal logs (for debugging)
- Statistics display
- Sample Q&A preview
- One-click downloads
- Clean, simple interface

### 🌓 Dark/Light Mode:
Click the theme toggle in the top-right corner!

### 📝 Logs & Debugging:
- Expand "Live Logs & Terminal Output" to see everything
- Copy logs with one click
- Perfect for troubleshooting

---

## 💡 Tips & Tricks

### For Testing:
```
URL: https://example.com
Max Pages: 20
Delay: 1.0s
```

### For Production:
```
URL: https://your-target-site.com
Max Pages: 100-200
Delay: 1.5-2.0s
```

### If You Get Errors:
1. Check the logs (expand the accordion)
2. Make sure your `.env` file has `GROQ_API_KEY`
3. Verify the URL is accessible
4. Try reducing max pages
5. Increase delay if rate limited

---

## 🔧 Advanced Usage

### Running on a Server:
Edit `rungui.py` line with `demo.launch()`:
```python
demo.launch(
    server_name="0.0.0.0",  # Allow external access
    server_port=7860,
    share=True  # Create public Gradio link
)
```

### Custom Port:
```python
demo.launch(server_port=8080)  # Use port 8080 instead
```

### Share with Team (Temporary Link):
```python
demo.launch(share=True)  # Creates a public link for 72 hours
```

---

## 🐛 Troubleshooting

### "Module 'gradio' not found"
```bash
pip install gradio
```

### "Pipeline failed"
- Check if you're in the right directory
- Make sure `Claudedatasets/` folder exists
- Verify your `.env` file has the API key

### "Can't connect to http://127.0.0.1:7860"
- Make sure the script is running
- Try a different port
- Check if another app is using port 7860

### GUI is slow/freezing
- This is normal during pipeline execution
- The pipeline takes time (especially Q&A generation)
- Don't close the browser tab!

---

## 🎉 What's Next?

Now that you have a GUI:
1. Share it with your team!
2. Let them test different websites
3. Collect feedback on features
4. Add more LLM providers
5. Improve the UI based on usage

---

**Enjoy your new GUI!** 🚀

Questions? Open an issue on GitHub!

