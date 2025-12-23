"""
QA Dataset Generator - Creates question-answer pairs from sliced data
Can be run standalone OR called by pipeline.py

Standalone usage:
    python generate_qa_dataset.py <run_directory>
    
Pipeline usage:
    python generate_qa_dataset.py <run_directory>
"""

from dotenv import load_dotenv
import os
load_dotenv()
import json
import re
import requests
import time
from tqdm import tqdm
from collections import defaultdict
from pathlib import Path
import sys

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

# Filenames (standardized across all runs)
TAGGED_FILENAME = "crawl_tagged.jsonl"  # Read from tagged instead of sliced
QA_FILENAME = "qa_training.jsonl"

# =========================
# CONFIG
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"

MAX_TOKENS_PER_BATCH = 6000
TOKEN_MULTIPLIER = 1.3

# =========================
# FILTERING HEURISTICS
# =========================

PRICE_REGEX = re.compile(r"\$\s?\d+")
BOOKED_REGEX = re.compile(r"\bbooked\b", re.I)
DROPDOWN_REGEX = re.compile(r"please choose an option", re.I)

def is_low_signal(block):
    """Filter out low-quality blocks"""
    text = block["block_text"].strip()

    if block["word_count"] < 8:
        return True

    if PRICE_REGEX.search(text) and BOOKED_REGEX.search(text):
        return True

    if DROPDOWN_REGEX.search(text):
        return True

    if len(set(text.split())) < 5:
        return True

    return False

# =========================
# TOKEN ESTIMATION
# =========================

def estimate_tokens(blocks):
    """Estimate token count for a batch of blocks"""
    return int(sum(b["word_count"] for b in blocks) * TOKEN_MULTIPLIER)

# =========================
# LLM CALL
# =========================

def call_llm(blocks, source_url, page_type, max_retries=5):
    """Call Groq API to generate Q&A pairs"""
    content = "\n\n".join(b["block_text"] for b in blocks)

    prompt = f"""
You are generating high-quality training data.

SOURCE URL: {source_url}
PAGE TYPE: {page_type}

CONTENT:
\"\"\"
{content}
\"\"\"

TASK:
- Generate question-answer pairs ONLY if the content explicitly supports them.
- Do NOT infer, guess, or add outside knowledge.
- If no valid questions can be formed, return an empty JSON array [].
- Answers must be fully grounded in the text.
- Return STRICT JSON only.

FORMAT:
[
  {{"question": "...", "answer": "..."}}
]
"""

    for attempt in range(max_retries):
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                    "max_tokens": 2048
                },
                timeout=120
            )

            if response.status_code == 429:
                wait = 2 ** attempt
                print(f"⚠️  Rate limited. Sleeping {wait}s...")
                time.sleep(wait)
                continue

            response.raise_for_status()

            raw = response.json()["choices"][0]["message"]["content"]

            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                print(f"⚠️  Invalid JSON response, skipping batch")
                return []
                
        except Exception as e:
            print(f"⚠️  Error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            continue

    print("❌ Max retries exceeded, skipping batch")
    return []

# =========================
# MAIN PIPELINE
# =========================

def load_blocks(input_path: Path):
    """Load all blocks from the sliced JSONL file"""
    blocks = []
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                blocks.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return blocks


def generate_qa(run_dir: Path, allowed_roles: list = None):
    """Generate Q&A pairs from tagged data in a run directory"""
    input_path = run_dir / TAGGED_FILENAME
    output_path = run_dir / QA_FILENAME
    
    # Validation
    if not input_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_path}")
    
    if output_path.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {output_path}")
    
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment. Create a .env file with your API key.")
    
    # Default roles if none provided
    if allowed_roles is None:
        allowed_roles = ["DESCRIPTIVE", "PROCEDURAL", "TEMPORAL", "TRANSACTIONAL"]
    
    print(f"📂 Generating Q&A: {run_dir.name}")
    print(f"📥 Reading from: {TAGGED_FILENAME}")
    print(f"🔑 Using Groq model: {GROQ_MODEL}")
    print(f"🏷️  Filtering by roles: {', '.join(allowed_roles)}")
    
    # Load all blocks
    all_blocks = load_blocks(input_path)
    print(f"   Loaded {len(all_blocks)} blocks")
    
    # Filter by role BEFORE anything else (THIS SAVES TIME AND MONEY!)
    role_filtered_blocks = []
    skipped_by_role = 0
    for block in all_blocks:
        block_role = block.get("role", "GENERAL")
        if block_role in allowed_roles:
            role_filtered_blocks.append(block)
        else:
            skipped_by_role += 1
    
    print(f"   ✅ Kept {len(role_filtered_blocks)} blocks with selected roles")
    print(f"   ⏭️  Skipped {skipped_by_role} blocks (wrong role)")
    
    # Group by (source_url, page_type)
    grouped = defaultdict(list)
    for b in role_filtered_blocks:  # Use role-filtered blocks
        if not is_low_signal(b):
            key = (b["source_url"], b["page_type"])
            grouped[key].append(b)
    
    print(f"   ✅ After quality filter: {sum(len(v) for v in grouped.values())} high-quality blocks")
    print(f"   📦 Grouped into {len(grouped)} page contexts")
    
    # Generate Q&A pairs
    total_qa_pairs = 0
    
    with open(output_path, "w", encoding="utf-8") as out:
        for (source_url, page_type), blocks in tqdm(grouped.items(), desc="Generating Q&A"):
            blocks = sorted(blocks, key=lambda x: x["block_index"])
            
            batch = []
            for block in blocks:
                # Check if adding this block exceeds token limit
                if estimate_tokens(batch + [block]) > MAX_TOKENS_PER_BATCH:
                    # Process current batch
                    qa_pairs = call_llm(batch, source_url, page_type)
                    for qa in qa_pairs:
                        out.write(json.dumps({
                            "source_url": source_url,
                            "page_type": page_type,
                            "question": qa["question"],
                            "answer": qa["answer"]
                        }, ensure_ascii=False) + "\n")
                        total_qa_pairs += 1
                    batch = []
                
                batch.append(block)
            
            # Process remaining batch
            if batch:
                qa_pairs = call_llm(batch, source_url, page_type)
                for qa in qa_pairs:
                    out.write(json.dumps({
                        "source_url": source_url,
                        "page_type": page_type,
                        "question": qa["question"],
                        "answer": qa["answer"]
                    }, ensure_ascii=False) + "\n")
                    total_qa_pairs += 1
    
    print(f"✅ Generated {total_qa_pairs} Q&A pairs")
    print(f"💾 Output: {QA_FILENAME}")
    print(f"📂 Location: {output_path}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Q&A pairs from tagged data")
    parser.add_argument("run_directory", help="Path to run directory")
    parser.add_argument(
        "--roles",
        nargs="+",
        default=["DESCRIPTIVE", "PROCEDURAL", "TEMPORAL", "TRANSACTIONAL"],
        help="Role tags to include in Q&A generation"
    )
    
    args = parser.parse_args()
    run_dir = Path(args.run_directory).resolve()
    
    if not run_dir.exists() or not run_dir.is_dir():
        print(f"❌ Invalid run directory: {run_dir}")
        sys.exit(1)
    
    try:
        generate_qa(run_dir, allowed_roles=args.roles)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
