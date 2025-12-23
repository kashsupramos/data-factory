# 🏭 Data Factory - Automated Training Dataset Generator

> **"Paste URL → Configure → Run → Get Training Data"**

A controlled pipeline for generating high-quality, versioned training datasets from web content. Built for teams who need traceable, auditable data for LLM fine-tuning.

## ✨ Features

- 🕷️ **Smart Web Crawling** - Configurable page limits and delays
- 🧹 **Intelligent Cleaning** - Removes boilerplate while preserving critical data (prices, measurements)
- ✂️ **Context-Aware Slicing** - Breaks content into optimal chunks without splitting important information
- 🤖 **AI-Powered Q&A Generation** - Uses Groq API to create training pairs
- 📦 **Versioned Outputs** - Every run creates a new timestamped dataset (never overwrites)
- 🔍 **Fully Traceable** - Track URLs, configs, and stats for every dataset

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Groq API key ([get one free at groq.com](https://console.groq.com/))

### Installation

1. **Clone the repo:**
```bash
git clone https://github.com/yourusername/data-factory.git
cd data-factory
```

2. **Create virtual environment:**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file in project root:**
```env
GROQ_API_KEY=your_api_key_here
```

### Run the Pipeline

**Option 1: GUI (Recommended for beginners)**
```bash
python gui.py
```
Then open your browser to http://127.0.0.1:7860 and use the web interface!

**Option 2: Command Line**
```bash
cd Claudedatasets
python pipeline.py https://example.com --max-pages 50
```

**That's it!** Your dataset will be in `AllDatasets/runs/run_YYYY-MM-DD_HH-MM-SS_XXXXXX/`

## 📖 Usage Examples

### Basic crawl (default 100 pages):
```bash
python pipeline.py https://example.com
```

### Crawl with custom limits:
```bash
python pipeline.py https://example.com --max-pages 50 --delay 2.0
```

### Interactive mode (prompts for URL):
```bash
python pipeline.py
```

## 📁 Output Structure

Each run creates a timestamped folder with 4 files:

```
AllDatasets/runs/run_2025-12-23_08-05-26_983378/
├── crawl_raw.jsonl      # Raw scraped data
├── crawl_clean.jsonl    # Cleaned documents
├── crawl_sliced.jsonl   # Sliced into training blocks
└── qa_training.jsonl    # Question-answer pairs (ready for training!)
```

### Output Format

**qa_training.jsonl** - Ready for LLM fine-tuning:
```json
{"source_url": "https://example.com", "page_type": "product", "question": "What is...", "answer": "..."}
{"source_url": "https://example.com", "page_type": "faq", "question": "How to...", "answer": "..."}
```

## 🛠️ Current Features

- ✅ **Beautiful Web GUI** (no command line needed!)
- ✅ Automated 4-step pipeline (Crawl → Clean → Slice → Generate Q&A)
- ✅ Real-time progress tracking
- ✅ One-click downloads
- ✅ Groq API integration (llama-3.1-8b-instant)
- ✅ Configurable crawl limits and delays
- ✅ Smart content slicing (preserves prices, measurements, percentages)
- ✅ Versioned outputs (never overwrites previous runs)
- ✅ Windows/Mac/Linux compatible
- ✅ UTF-8 emoji support

## 🚧 Roadmap (Help Wanted!)

We're actively looking for contributors! Here's what we're planning:

### High Priority
- [ ] **GUI Interface** (Gradio/Streamlit) - drag & drop URLs, configure settings
- [ ] **Multiple LLM Providers** (OpenAI, Claude, local models via LM Studio)
- [ ] **Strictness Modes** (Conservative/Balanced/Aggressive Q&A generation)

### Medium Priority
- [ ] **robots.txt Compliance** - respect crawl rules automatically
- [ ] **Crawl Depth Controls** - limit how deep to follow links
- [ ] **Domain-Specific Rules** - custom filtering per project
- [ ] **Audit Dashboard** - review stats, sample outputs before export

### Nice to Have
- [ ] **Batch URL Processing** - upload CSV of URLs
- [ ] **Resume Failed Runs** - continue from where it crashed
- [ ] **Export Formats** - CSV, Parquet, HuggingFace datasets
- [ ] **Quality Metrics** - automatic scoring of Q&A pairs

## 🤝 Contributing

We'd love your help! Here's how to contribute:

1. **Fork the repo**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test it works** (run the pipeline on a test URL)
5. **Commit** (`git commit -m 'Add amazing feature'`)
6. **Push** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

### Good First Issues
- Add support for more LLM providers
- Improve error handling
- Add unit tests
- Create example notebooks
- Improve documentation

## 📝 Project Structure

```
data-factory/
├── Claudedatasets/              # Main pipeline scripts
│   ├── pipeline.py              # Master orchestrator
│   ├── crawling.py              # Web scraper
│   ├── cleancrawling.py         # Data cleaner
│   ├── slicingdata.py           # Content slicer
│   └── generate_qa_dataset.py   # Q&A generator
├── AllDatasets/
│   └── runs/                    # Output datasets (timestamped)
├── .env                         # API keys (not in repo - you create this)
├── .gitignore                   # Files to ignore
├── requirements.txt             # Python dependencies
└── README.md                    # This file!
```

## 🔧 Configuration

### Environment Variables (.env)
```env
GROQ_API_KEY=your_groq_api_key_here
```

### Pipeline Options
- `--max-pages`: Maximum pages to crawl (default: 100)
- `--delay`: Delay between requests in seconds (default: 1.0)

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'bs4'"
Make sure you activated the virtual environment and installed dependencies:
```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### "GROQ_API_KEY not found"
Create a `.env` file in the project root with your API key:
```env
GROQ_API_KEY=your_key_here
```

### Unicode/Emoji Errors on Windows
This should be fixed! But if you see encoding errors, the scripts auto-detect Windows and set UTF-8.

## 📄 License

MIT License - feel free to use for your projects!

## 🙏 Acknowledgments

Built with ❤️ for the open-source ML community during the holidays!

Special thanks to:
- Groq for fast inference
- BeautifulSoup for web scraping
- The Python community

---

**Questions?** Open an issue or reach out to the team!

**Want to chat?** Join our discussions tab!

