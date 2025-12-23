"""
Data Factory GUI - Beautiful web interface for the pipeline
Run with: python rungui.py
"""

import gradio as gr
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import json
import os

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.resolve()
CLAUDEDATASETS_DIR = PROJECT_ROOT / "Claudedatasets"
RUNS_DIR = PROJECT_ROOT / "AllDatasets" / "runs"


def run_pipeline(url, max_pages, delay, progress=gr.Progress()):
    """Run the complete pipeline with progress tracking"""
    
    if not url or not url.startswith(('http://', 'https://')):
        return {
            status_box: "❌ Error: Please enter a valid URL (must start with http:// or https://)",
            logs_box: "",
            stats_box: "",
            download_section: gr.update(visible=False),
            download_raw: None,
            download_clean: None,
            download_sliced: None,
            download_tagged: None,
            download_qa: None
        }
    
    # Update status
    progress(0, desc="🚀 Starting pipeline...")
    
    # Prepare command
    cmd = [
        sys.executable,
        str(CLAUDEDATASETS_DIR / "pipeline.py"),
        url,
        "--max-pages", str(int(max_pages)),
        "--delay", str(delay)
    ]
    
    # Run the pipeline
    try:
        progress(0.1, desc="🕷️ Step 1/4: Crawling website...")
        
        # Set UTF-8 encoding for subprocess on Windows
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',  # Replace problematic characters instead of crashing
            bufsize=1,
            universal_newlines=True,
            cwd=str(CLAUDEDATASETS_DIR),
            env=env
        )
        
        # Collect output
        output_lines = []
        current_step = 1
        
        for line in process.stdout:
            output_lines.append(line.rstrip())
            
            # Update progress based on pipeline steps
            if "STEP 1: Crawling" in line:
                progress(0.08, desc="🕷️ Step 1/5: Crawling website...")
                current_step = 1
            elif "STEP 2: Cleaning" in line:
                progress(0.28, desc="🧹 Step 2/5: Cleaning data...")
                current_step = 2
            elif "STEP 3: Slicing" in line:
                progress(0.48, desc="✂️ Step 3/5: Slicing data...")
                current_step = 3
            elif "STEP 3.5: Tagging" in line:
                progress(0.62, desc="🏷️ Step 4/5: Tagging blocks...")
                current_step = 4
            elif "STEP 4: Generating QA" in line:
                progress(0.78, desc="🤖 Step 5/5: Generating Q&A pairs...")
                current_step = 5
            elif "PIPELINE COMPLETE" in line:
                progress(1.0, desc="✅ Complete!")
        
        process.wait()
        
        full_output = "\n".join(output_lines)
        
        # Check if successful
        if process.returncode == 0 and "PIPELINE COMPLETE" in full_output:
            # Extract run directory from output
            run_dir = None
            for line in output_lines:
                if "Run directory:" in line:
                    run_dir = line.split("Run directory:")[-1].strip()
                    break
            
            # Parse stats from output
            stats = parse_pipeline_stats(full_output, run_dir)
            
            # Get file paths for download
            files = get_download_files(run_dir)
            
            return {
                status_box: "✅ Pipeline completed successfully!",
                logs_box: full_output,
                stats_box: stats,
                download_section: gr.update(visible=True),
                download_raw: files['raw'],
                download_clean: files['clean'],
                download_sliced: files['sliced'],
                download_tagged: files['tagged'],
                download_qa: files['qa'],
                run_dir_state: run_dir
            }
        else:
            return {
                status_box: f"❌ Pipeline failed (exit code: {process.returncode})",
                logs_box: full_output,
                stats_box: "Pipeline did not complete successfully. Check logs for details.",
                download_section: gr.update(visible=False),
                download_raw: None,
                download_clean: None,
                download_sliced: None,
                download_tagged: None,
                download_qa: None
            }
            
    except Exception as e:
        return {
            status_box: f"❌ Error: {str(e)}",
            logs_box: f"Exception occurred:\n{str(e)}",
            stats_box: "",
            download_section: gr.update(visible=False),
            download_raw: None,
            download_clean: None,
            download_sliced: None,
            download_tagged: None,
            download_qa: None
        }


def get_download_files(run_dir):
    """Get file paths for download"""
    files = {
        'raw': None,
        'clean': None,
        'sliced': None,
        'tagged': None,
        'qa': None
    }
    
    if not run_dir:
        return files
    
    run_path = Path(run_dir)
    if not run_path.exists():
        return files
    
    file_mapping = {
        'raw': 'crawl_raw.jsonl',
        'clean': 'crawl_clean.jsonl',
        'sliced': 'crawl_sliced.jsonl',
        'tagged': 'crawl_tagged.jsonl',
        'qa': 'qa_training.jsonl'
    }
    
    for key, filename in file_mapping.items():
        file_path = run_path / filename
        if file_path.exists():
            files[key] = str(file_path)
    
    return files


def parse_pipeline_stats(output, run_dir):
    """Parse statistics from pipeline output"""
    stats = []
    
    # Extract key metrics
    lines = output.split('\n')
    
    stats.append("## 📊 Pipeline Statistics\n")
    
    pages_crawled = "N/A"
    docs_cleaned = "N/A"
    blocks_created = "N/A"
    qa_generated = "N/A"
    
    for line in lines:
        if "Pages scraped:" in line:
            pages_crawled = line.split("Pages scraped:")[-1].strip()
        elif "clean documents" in line and "Saved" in line:
            try:
                docs_cleaned = line.split("Saved")[-1].split("/")[0].strip()
            except:
                pass
        elif "blocks from" in line and "Saved" in line:
            try:
                blocks_created = line.split("Saved")[-1].split("blocks")[0].strip()
            except:
                pass
        elif "Generated" in line and "Q&A pairs" in line:
            try:
                qa_generated = line.split("Generated")[-1].split("Q&A")[0].strip()
            except:
                pass
    
    stats.append(f"**Pages Crawled:** {pages_crawled}")
    stats.append(f"**Documents Cleaned:** {docs_cleaned}")
    stats.append(f"**Blocks Created:** {blocks_created}")
    stats.append(f"**Q&A Pairs Generated:** {qa_generated}")
    
    if run_dir:
        stats.append(f"\n**📂 Output Location:**")
        stats.append(f"`{run_dir}`")
    
    # Add file sizes
    if run_dir:
        stats.append("\n### 📄 Generated Files:")
        run_path = Path(run_dir)
        if run_path.exists():
            for file in ["crawl_raw.jsonl", "crawl_clean.jsonl", "crawl_sliced.jsonl", "qa_training.jsonl"]:
                file_path = run_path / file
                if file_path.exists():
                    size_kb = file_path.stat().st_size / 1024
                    stats.append(f"- `{file}`: {size_kb:.1f} KB")
    
    return "\n".join(stats) if len(stats) > 1 else "No statistics available."


def load_sample_qa(run_dir, num_samples=5):
    """Load sample Q&A pairs from the output"""
    if not run_dir:
        return "No Q&A data available."
    
    qa_file = Path(run_dir) / "qa_training.jsonl"
    if not qa_file.exists():
        return "Q&A file not found."
    
    samples = []
    try:
        with open(qa_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= num_samples:
                    break
                qa = json.loads(line)
                samples.append(f"**Q:** {qa['question']}\n**A:** {qa['answer']}\n")
        
        if samples:
            return "\n---\n".join(samples)
        else:
            return "No Q&A pairs found in file."
    except Exception as e:
        return f"Error loading samples: {str(e)}"


# Create the Gradio interface
with gr.Blocks(title="Data Factory") as demo:
    
    # State to store run directory
    run_dir_state = gr.State(value=None)
    
    # Header
    gr.Markdown("""
    # 🏭 Data Factory
    ### Generate training datasets from any website
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            # Input section
            gr.Markdown("### 📍 Configuration")
            
            url_input = gr.Textbox(
                label="URL to Crawl",
                placeholder="https://example.com",
                info="Enter the website URL you want to scrape"
            )
            
            with gr.Row():
                max_pages_slider = gr.Slider(
                    minimum=5,
                    maximum=200,
                    value=50,
                    step=5,
                    label="Max Pages",
                    info="Maximum number of pages to crawl"
                )
                
                delay_slider = gr.Slider(
                    minimum=0.5,
                    maximum=5.0,
                    value=1.0,
                    step=0.5,
                    label="Delay (seconds)",
                    info="Delay between requests (be respectful!)"
                )
            
            run_button = gr.Button("🚀 Start Pipeline", variant="primary", size="lg")
            
            # Status section
            gr.Markdown("### 📊 Status")
            status_box = gr.Textbox(
                label="Current Status",
                value="Ready to start. Enter a URL and click 'Start Pipeline'.",
                interactive=False,
                lines=2
            )
        
        with gr.Column(scale=1):
            # Info panel
            gr.Markdown("""
            ### ℹ️ Quick Guide
            
            **Steps:**
            1. Enter a URL
            2. Adjust settings (optional)
            3. Click "Start Pipeline"
            4. Wait for completion
            5. Download your data!
            
            **Output Files:**
            - `crawl_raw.jsonl` - Raw data
            - `crawl_clean.jsonl` - Cleaned data
            - `crawl_sliced.jsonl` - Sliced blocks
            - `qa_training.jsonl` - Training pairs
            
            **Tips:**
            - Start with 20-50 pages for testing
            - Use 1-2s delay for politeness
            - Check logs if errors occur
            """)
    
    # Logs section (collapsible)
    with gr.Accordion("📝 Live Logs & Terminal Output", open=False):
        logs_box = gr.Textbox(
            label="Pipeline Logs",
            lines=15,
            max_lines=20,
            interactive=False
        )
    
    # Results section (hidden by default)
    with gr.Column(visible=False) as download_section:
        gr.Markdown("### ✅ Pipeline Complete!")
        
        stats_box = gr.Markdown("Loading statistics...")
        
        gr.Markdown("### 📥 Download Results")
        gr.Markdown("*Click the file names below to download*")
        
        with gr.Row():
            download_raw = gr.File(label="📄 Raw Data (crawl_raw.jsonl)", interactive=False)
            download_clean = gr.File(label="🧹 Clean Data (crawl_clean.jsonl)", interactive=False)
        
        with gr.Row():
            download_sliced = gr.File(label="✂️ Sliced Data (crawl_sliced.jsonl)", interactive=False)
            download_tagged = gr.File(label="🏷️ Tagged Data (crawl_tagged.jsonl)", interactive=False)
        
        with gr.Row():
            download_qa = gr.File(label="🤖 Training Q&A (qa_training.jsonl)", interactive=False)
        
        # Sample Q&A viewer
        with gr.Accordion("👀 Preview Sample Q&A Pairs", open=False):
            sample_qa_box = gr.Markdown("Click 'Load Samples' to preview")
            load_samples_btn = gr.Button("Load Samples")
    
    # Connect the run button
    run_button.click(
        fn=run_pipeline,
        inputs=[url_input, max_pages_slider, delay_slider],
        outputs=[
            status_box,
            logs_box,
            stats_box,
            download_section,
            download_raw,
            download_clean,
            download_sliced,
            download_tagged,
            download_qa,
            run_dir_state
        ]
    )
    
    # Connect sample loader
    load_samples_btn.click(
        fn=load_sample_qa,
        inputs=[run_dir_state],
        outputs=[sample_qa_box]
    )
    
    # Footer
    gr.Markdown("""
    ---
    Made with ❤️ by the Data Factory team | [GitHub](https://github.com/kashsupramos/data-factory) | [Report Issues](https://github.com/kashsupramos/data-factory/issues)
    """)


if __name__ == "__main__":
    print("🏭 Starting Data Factory GUI...")
    print("📂 Project root:", PROJECT_ROOT)
    print("🔧 Pipeline location:", CLAUDEDATASETS_DIR)
    print("\n🌐 Opening web interface...\n")
    
    demo.launch(
        server_name="127.0.0.1",
        server_port=7861,  # Using 7861 in case 7860 is in use
        share=False,
        show_error=True,
        inbrowser=True  # Auto-open browser
    )
