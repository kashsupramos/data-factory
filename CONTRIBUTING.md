# Contributing to Data Factory

Thanks for your interest in contributing! 🎉

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/data-factory.git
   cd data-factory
   ```
3. **Set up your environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
4. **Create a `.env` file** with your Groq API key

## Making Changes

1. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** - edit the code

3. **Test your changes** - run the pipeline to make sure it works:
   ```bash
   cd Claudedatasets
   python pipeline.py https://example.com --max-pages 10
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

## What to Contribute

### High Priority
- GUI interface (Gradio/Streamlit)
- Additional LLM providers (OpenAI, Claude, local models)
- Strictness modes for Q&A generation
- robots.txt compliance
- Unit tests

### Always Welcome
- Bug fixes
- Documentation improvements
- Example notebooks
- Performance optimizations
- Better error messages

## Code Style

- Follow PEP 8 for Python code
- Add docstrings to functions
- Keep functions focused and small
- Comment complex logic
- Use meaningful variable names

## Questions?

Open an issue or start a discussion! We're friendly and happy to help! 😊

