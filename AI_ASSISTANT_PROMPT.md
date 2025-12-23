# 🤖 AI Assistant Onboarding Prompt

Use this prompt when working with OTHER AI assistants (Claude, ChatGPT, etc.) on this project.

---

## Copy-Paste This to New AI Assistants:

```
I have a Python-based data pipeline project called "Data Factory" that scrapes websites, 
cleans data, slices content into blocks, tags them with roles, and generates Q&A training 
datasets using Groq API.

### Project Structure:

**Core Pipeline Scripts** (in `Claudedatasets/`):
1. `crawling.py` - Web scraper (Step 1)
2. `cleancrawling.py` - Data cleaner (Step 2)
3. `slicingdata.py` - Content slicer (Step 3)
4. `tag_sliced_blocks.py` - Role tagger (Step 3.5)
5. `generate_qa_dataset.py` - Q&A generator with Groq API (Step 4)
6. `pipeline.py` - Master orchestrator that runs all steps

**GUI**: `rungui.py` - Gradio web interface (port 7861)

**Outputs**: All saved to `AllDatasets/runs/run_YYYY-MM-DD_HH-MM-SS_xxxxx/`
- `crawl_raw.jsonl` - Raw scraped data
- `crawl_clean.jsonl` - Cleaned text
- `crawl_sliced.jsonl` - Text blocks (200-500 chars)
- `crawl_tagged.jsonl` - Blocks with role tags
- `qa_training.jsonl` - Q&A pairs for training

**Role Tags**: TRANSACTIONAL, TEMPORAL, PROCEDURAL, PROMOTIONAL, DESCRIPTIVE, 
POLICY_LEGAL, CONTACT, GENERAL

### Technical Details:

- **Python 3.11+** on Windows (encoding: UTF-8 fixes applied throughout)
- **Dependencies**: requests, beautifulsoup4, pandas, python-dotenv, tqdm, gradio, groq
- **API**: Groq API (llama-3.1-8b-instant) with key in `.env` file
- **File Format**: JSONL (JSON Lines) for all datasets
- **Path Management**: Uses `pathlib.Path`, no hardcoded paths
- **Error Handling**: UTF-8 encoding set for all subprocess calls

### Current Status:

✅ Pipeline is FULLY WORKING and tested
✅ GUI is operational with 5-step progress tracking
✅ All scripts use dynamic `run_dir` argument
✅ Windows encoding issues resolved
✅ GitHub repo ready for team collaboration
✅ Comprehensive documentation written

### Known Issues:

1. Tagging accuracy: 20-45% blocks tagged as "GENERAL" (rule-based, needs improvement)
2. Q&A quality: Generic LLM lacks domain expertise for medical/beauty topics
3. Data loss: Critical info (prices, measurements) sometimes filtered out
4. No multi-URL support yet

### Documentation Files:

- `README.md` - Main docs
- `QUICK_START.md` - Fast setup guide
- `CONTRIBUTING.md` - For team members
- `DATASET_QUALITY.md` - Dataset analysis and recommendations
- `WORK_SUMMARY.md` - Complete project overview
- `GUI_GUIDE.md` - GUI documentation

### What I Need Help With:

[Describe your specific task here]

### Important Context:

- I'm on Windows, use PowerShell
- Virtual env: `.\venv\Scripts\Activate.ps1`
- Project root: `C:\Users\Kash Supramos\Desktop\CreatingDatasets`
- GitHub repo: https://github.com/kashsupramos/data-factory

Please help me with [your specific request] while maintaining the existing code structure 
and following the patterns already established in the codebase.
```

---

## Example Use Cases:

### 1. Ask for Feature Implementation

```
[Use the prompt above, then add:]

I want to add role-based filtering to the Q&A generation. Specifically:
- Only generate Q&A from blocks tagged as: DESCRIPTIVE, PROCEDURAL, TEMPORAL, TRANSACTIONAL
- Skip GENERAL, PROMOTIONAL, POLICY_LEGAL blocks
- Update the GUI to show how many blocks were filtered out
- Preserve the existing code structure
```

### 2. Ask for Bug Fixes

```
[Use the prompt above, then add:]

I'm getting an error when running the pipeline:
[paste error message]

The error occurs in [filename] at line [X]. Can you help me fix it while maintaining 
compatibility with the rest of the pipeline?
```

### 3. Ask for Improvements

```
[Use the prompt above, then add:]

I want to improve the tagging accuracy. Currently, 45% of blocks are tagged as GENERAL. 
Can you suggest and implement a better tagging algorithm that:
- Uses more sophisticated keyword matching
- Maybe considers context (neighboring blocks)
- Still runs fast (no API calls)
```

### 4. Ask for New Features

```
[Use the prompt above, then add:]

I want to add multi-URL support to the pipeline. The user should be able to:
- Input multiple URLs in the GUI (one per line)
- Pipeline crawls each URL separately
- All results are combined into a single run directory
- Statistics show breakdown by source URL

Please implement this feature and update the GUI accordingly.
```

### 5. Ask for Documentation

```
[Use the prompt above, then add:]

Can you create a detailed technical architecture document explaining:
- How data flows through the pipeline
- Design patterns used
- API integration details
- Potential bottlenecks and scalability considerations
```

---

## Tips for Working with AI Assistants on This Project:

### 1. Always Provide Context

- **Good**: "I want to add a feature to `tag_sliced_blocks.py` that counts keyword frequency"
- **Bad**: "Make the tagger better"

### 2. Reference Existing Patterns

- **Good**: "Add this the same way `crawl_sliced.jsonl` is handled in `pipeline.py`"
- **Bad**: "Just add it somewhere"

### 3. Specify Constraints

- **Good**: "Don't use external libraries, keep it with existing dependencies"
- **Bad**: "Add whatever libraries you need"

### 4. Ask for Explanation

- **Good**: "Can you explain why you chose this approach over [alternative]?"
- **Great**: AI learns your preferences and makes better suggestions next time

### 5. Test Incrementally

- **Good**: "Let's test just the tagging changes before modifying the GUI"
- **Bad**: "Change everything at once"

---

## What NOT to Ask AI Assistants:

❌ **"Rewrite the entire codebase"** - You'll lose your working code  
❌ **"Make it perfect"** - Too vague, AI will guess  
❌ **"Add [feature] without understanding current code"** - Will break things  
❌ **"Change all file paths"** - Already fixed, don't redo  
❌ **"Switch to a different framework"** - Unnecessary work  

---

## What TO Ask AI Assistants:

✅ **"Add [specific feature] to [specific file]"**  
✅ **"Improve [specific function] to handle [edge case]"**  
✅ **"Debug this error: [error message]"**  
✅ **"Explain how [component] works"**  
✅ **"Optimize [function] for performance"**  
✅ **"Add error handling for [scenario]"**  
✅ **"Write tests for [feature]"**  

---

## Quick Reference Commands (for AI to suggest):

### Run Pipeline
```bash
cd "C:\Users\Kash Supramos\Desktop\CreatingDatasets"
.\venv\Scripts\Activate.ps1
cd Claudedatasets
python pipeline.py "https://example.com" --max-pages 50
```

### Run GUI
```bash
cd "C:\Users\Kash Supramos\Desktop\CreatingDatasets"
.\venv\Scripts\Activate.ps1
python rungui.py
```

### Test Single Script
```bash
cd "C:\Users\Kash Supramos\Desktop\CreatingDatasets"
.\venv\Scripts\Activate.ps1
cd Claudedatasets
python tag_sliced_blocks.py "../AllDatasets/runs/run_XXX"
```

### Git Commands
```bash
git status
git add .
git commit -m "Description"
git push origin main
```

---

## File Structure Quick Reference

```
Claudedatasets/
├── crawling.py          # Input: URL → Output: crawl_raw.jsonl
├── cleancrawling.py     # Input: crawl_raw.jsonl → Output: crawl_clean.jsonl
├── slicingdata.py       # Input: crawl_clean.jsonl → Output: crawl_sliced.jsonl
├── tag_sliced_blocks.py # Input: crawl_sliced.jsonl → Output: crawl_tagged.jsonl
├── generate_qa_dataset.py # Input: crawl_sliced.jsonl → Output: qa_training.jsonl
└── pipeline.py          # Runs all of the above in sequence

rungui.py                # Web interface that calls pipeline.py
```

---

## Common Scenarios & Solutions

### Scenario 1: "The tagging is not accurate"

**Solution**: Modify the `ROLES` list in `tag_sliced_blocks.py`:
```python
ROLES = [
    ("ROLE_NAME", ["keyword1", "keyword2", ...]),
    ...
]
```

### Scenario 2: "I want to change the Q&A generation prompt"

**Solution**: Modify `SYSTEM_PROMPT` in `generate_qa_dataset.py` (around line 70)

### Scenario 3: "I want to add a new GUI option"

**Solution**: Add a new Gradio component in `rungui.py` (around line 320-340), 
then pass it as an input to `run_pipeline()`

### Scenario 4: "I want to change the LLM model"

**Solution**: Change `GROQ_MODEL` in `generate_qa_dataset.py` (line 38)

### Scenario 5: "Pipeline fails at a specific step"

**Solution**: Run that script standalone to see detailed error:
```bash
python [script_name].py [arguments]
```

---

## Important Reminders for AI Assistants:

1. **This is Windows**: Use `.\venv\Scripts\Activate.ps1`, not `source venv/bin/activate`
2. **UTF-8 Everywhere**: All files should have the encoding fix at the top
3. **Use pathlib**: Don't use string concatenation for paths
4. **JSONL Format**: One JSON object per line, no commas between objects
5. **Dynamic Paths**: Never hardcode paths, always use `run_dir` argument
6. **Error Handling**: Use `try-except` blocks for file operations and API calls
7. **Progress Tracking**: Print clear status messages for user feedback

---

## Version History (for AI context):

- **v1.0** (Initial): Basic pipeline without tagging
- **v2.0** (Current): Added role tagging, improved GUI, comprehensive docs
- **v2.1** (Future): Role-based Q&A filtering, multi-URL support

---

## Contact & Resources:

- **GitHub**: https://github.com/kashsupramos/data-factory
- **Groq API Docs**: https://console.groq.com/docs
- **Gradio Docs**: https://gradio.app/docs

---

**Last Updated**: December 23, 2025  
**For**: AI Assistant onboarding  
**Project**: Data Factory Pipeline v2.0

