"""
Master Pipeline for Beauty Dataset Generation
Runs all 5 steps automatically: Crawl → Clean → Slice → Generate QA

Usage:
    python pipeline.py https://example.com
    python pipeline.py https://example.com --max-pages 50
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
import uuid
import argparse

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

def generate_run_id():
    """Generate unique run ID with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    short_id = uuid.uuid4().hex[:6]
    return f"run_{timestamp}_{short_id}"


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}\n")
    
    try:
        # Set UTF-8 encoding for subprocess on Windows
        import os
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8',  # Force UTF-8 encoding
            errors='replace',   # Replace problematic characters instead of crashing
            env=env
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during: {description}")
        print(f"Exit code: {e.returncode}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Master pipeline for beauty dataset generation"
    )
    parser.add_argument(
        'url',
        nargs='?',  # Make URL optional
        help='Base URL to crawl (e.g., https://example.com)'
    )
    parser.add_argument(
        '--max-pages',
        type=int,
        default=100,
        help='Maximum pages to crawl (default: 100)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )
    
    args = parser.parse_args()
    
    # If no URL provided, ask for it interactively
    if not args.url:
        print("="*60)
        print("🚀 BEAUTY DATASET PIPELINE")
        print("="*60)
        args.url = input("Enter URL to crawl: ").strip()
        
        if not args.url:
            print("❌ No URL provided!")
            sys.exit(1)
        
        # Optionally ask for max pages
        max_pages_input = input(f"Max pages to crawl (default: {args.max_pages}): ").strip()
        if max_pages_input:
            try:
                args.max_pages = int(max_pages_input)
            except ValueError:
                print("⚠️  Invalid number, using default")
    
    # Get paths
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent.resolve()
    
    # Define script locations
    crawling_script = script_dir / "crawling.py"
    cleaning_script = script_dir / "cleancrawling.py"
    slicing_script = script_dir / "slicingdata.py"
    tagging_script = script_dir / "tag_sliced_blocks.py"
    qa_script = script_dir / "generate_qa_dataset.py"
    
    # Verify scripts exist
    missing_scripts = []
    for script in [crawling_script, cleaning_script, slicing_script, tagging_script, qa_script]:
        if not script.exists():
            missing_scripts.append(script.name)
    
    if missing_scripts:
        print(f"❌ Missing scripts: {', '.join(missing_scripts)}")
        print(f"📂 Looking in: {script_dir}")
        sys.exit(1)
    
    # Generate run directory
    run_id = generate_run_id()
    runs_dir = project_root / "AllDatasets" / "runs"
    run_dir = runs_dir / run_id
    
    print("="*60)
    print("🚀 BEAUTY DATASET PIPELINE")
    print("="*60)
    print(f"🎯 Target URL: {args.url}")
    print(f"📊 Max pages: {args.max_pages}")
    print(f"⏱️  Delay: {args.delay}s")
    print(f"📂 Run directory: {run_dir}")
    print(f"📁 Run ID: {run_id}")
    print("="*60)
    
    # Create run directory
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created run directory: {run_dir}\n")
    
    # Expected output files
    crawl_raw = run_dir / "crawl_raw.jsonl"
    crawl_clean = run_dir / "crawl_clean.jsonl"
    crawl_sliced = run_dir / "crawl_sliced.jsonl"
    crawl_tagged = run_dir / "crawl_tagged.jsonl"
    qa_training = run_dir / "qa_training.jsonl"
    
    # ========================================
    # STEP 1: CRAWL
    # ========================================
    success = run_command(
        [
            sys.executable,
            str(crawling_script),
            args.url,
            str(run_dir),
            str(args.max_pages),
            str(args.delay)
        ],
        "STEP 1: Crawling website"
    )
    
    if not success or not crawl_raw.exists():
        print(f"❌ Crawling failed or {crawl_raw.name} not created")
        sys.exit(1)
    
    print(f"✅ Crawling complete: {crawl_raw}")
    
    # ========================================
    # STEP 2: CLEAN
    # ========================================
    success = run_command(
        [
            sys.executable,
            str(cleaning_script),
            str(run_dir)
        ],
        "STEP 2: Cleaning data"
    )
    
    if not success or not crawl_clean.exists():
        print(f"❌ Cleaning failed or {crawl_clean.name} not created")
        sys.exit(1)
    
    print(f"✅ Cleaning complete: {crawl_clean}")
    
    # ========================================
    # STEP 3: SLICE
    # ========================================
    success = run_command(
        [
            sys.executable,
            str(slicing_script),
            str(run_dir)
        ],
        "STEP 3: Slicing data"
    )
    
    if not success or not crawl_sliced.exists():
        print(f"❌ Slicing failed or {crawl_sliced.name} not created")
        sys.exit(1)
    
    print(f"✅ Slicing complete: {crawl_sliced}")
    
    # ========================================
    # STEP 3.5: TAG SLICED BLOCKS
    # ========================================
    crawl_tagged = run_dir / "crawl_tagged.jsonl"
    
    success = run_command(
        [
            sys.executable,
            str(script_dir / "tag_sliced_blocks.py"),
            str(run_dir)  # Pass run_dir, not individual files
        ],
        "STEP 3.5: Tagging sliced blocks"
    )
    
    if not success or not crawl_tagged.exists():
        print(f"❌ Tagging failed or {crawl_tagged.name} not created")
        sys.exit(1)
    
    print(f"✅ Tagging complete: {crawl_tagged}")
    
    # ========================================
    # STEP 4: GENERATE QA
    # ========================================
    success = run_command(
        [
            sys.executable,
            str(qa_script),
            str(run_dir)
        ],
        "STEP 4: Generating QA pairs"
    )
    
    if not success or not qa_training.exists():
        print(f"❌ QA generation failed or {qa_training.name} not created")
        sys.exit(1)
    
    print(f"✅ QA generation complete: {qa_training}")
    
    # ========================================
    # FINAL SUMMARY
    # ========================================
    print("\n" + "="*60)
    print("✨ PIPELINE COMPLETE!")
    print("="*60)
    print(f"📂 All outputs saved to: {run_dir}")
    print(f"\n📄 Generated files:")
    print(f"  1. {crawl_raw.name} - Raw scraped data")
    print(f"  2. {crawl_clean.name} - Cleaned data")
    print(f"  3. {crawl_sliced.name} - Sliced data")
    print(f"  4. {crawl_tagged.name} - Tagged data (with roles)")
    print(f"  5. {qa_training.name} - Training QA pairs")
    
    # Show file sizes
    print(f"\n📊 File sizes:")
    for file in [crawl_raw, crawl_clean, crawl_sliced, crawl_tagged, qa_training]:
        if file.exists():
            size_kb = file.stat().st_size / 1024
            print(f"  {file.name}: {size_kb:.1f} KB")
    
    print(f"\n🎉 Success! Your dataset is ready for training!")


if __name__ == "__main__":
    main()