"""
Data Slicer - Breaks cleaned documents into smaller blocks
Can be run standalone OR called by pipeline.py

Standalone usage:
    python slicingdata.py <run_directory>
    
Pipeline usage:
    python slicingdata.py <run_directory>
"""

import json
import re
from typing import List, Dict
from pathlib import Path
import sys

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

# Filenames (standardized across all runs)
CLEAN_FILENAME = "crawl_clean.jsonl"
SLICED_FILENAME = "crawl_sliced.jsonl"

MIN_BLOCK_CHARS = 80   # drop tiny UI junk, tune if needed


def normalize_text(text: str) -> str:
    """Normalize whitespace and line breaks"""
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def is_dense_listing_block(block: str) -> bool:
    """
    Heuristic: long block with many price markers or 'booked'
    Detects service listings, product catalogs, etc.
    """
    price_hits = len(re.findall(r"\$\s*\d+", block))
    booked_hits = block.lower().count("booked")
    
    # Also check for common listing patterns
    bullet_hits = block.count("•") + block.count("*")
    
    return price_hits >= 2 or booked_hits >= 2 or bullet_hits >= 5


def split_dense_block(block: str) -> List[str]:
    """
    Split dense listings into line-like units.
    We split on price boundaries or newline transitions.
    """
    # First try newline split
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    
    # If we got reasonable chunks, return them
    if len(lines) > 1 and all(len(l) > MIN_BLOCK_CHARS for l in lines[:3]):
        return lines
    
    # Fallback: split on '$ <number>' price markers
    chunks = re.split(r"(?=\$\s*\d+)", block)
    valid_chunks = [c.strip() for c in chunks if len(c.strip()) > MIN_BLOCK_CHARS]
    
    # If splitting didn't help, return original block
    if not valid_chunks:
        return [block] if len(block) > MIN_BLOCK_CHARS else []
    
    return valid_chunks


def structural_slice(record: Dict) -> List[Dict]:
    """
    Break a document into logical blocks while preserving context.
    Returns list of sliced blocks with metadata.
    """
    text = normalize_text(record["text"])
    
    # Split on double newlines (paragraph boundaries)
    raw_blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    
    sliced_blocks = []
    block_index = 0
    
    for block in raw_blocks:
        sub_blocks = []
        
        # Check if this is a dense listing that needs further splitting
        if is_dense_listing_block(block):
            sub_blocks = split_dense_block(block)
        else:
            sub_blocks = [block]
        
        # Create records for each sub-block
        for sub in sub_blocks:
            # Skip blocks that are too short
            if len(sub) < MIN_BLOCK_CHARS:
                continue
            
            sliced_blocks.append({
                "source_url": record["url"],
                "page_type": record.get("page_type", "unknown"),
                "block_index": block_index,
                "block_text": sub,
                "block_length": len(sub),
                "word_count": len(sub.split())
            })
            block_index += 1
    
    return sliced_blocks


def slice_run(run_dir: Path):
    """Slice the cleaned data in a run directory"""
    input_path = run_dir / CLEAN_FILENAME
    output_path = run_dir / SLICED_FILENAME
    
    # Validation
    if not input_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_path}")
    
    if output_path.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {output_path}")
    
    print(f"📂 Slicing: {run_dir.name}")
    print(f"📥 Reading from: {CLEAN_FILENAME}")
    
    # Process all documents
    all_blocks = []
    doc_count = 0
    
    with open(input_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                record = json.loads(line)
                blocks = structural_slice(record)
                all_blocks.extend(blocks)
                doc_count += 1
                
                # Progress indicator
                if doc_count % 10 == 0:
                    print(f"   Processed {doc_count} docs → {len(all_blocks)} blocks")
                    
            except json.JSONDecodeError:
                print(f"⚠️  Skipping malformed JSON at line {line_num}")
            except Exception as e:
                print(f"⚠️  Error processing line {line_num}: {e}")
    
    # Save output
    with open(output_path, "w", encoding="utf-8") as f:
        for block in all_blocks:
            f.write(json.dumps(block, ensure_ascii=False) + "\n")
    
    # Statistics
    if all_blocks:
        avg_length = sum(b['block_length'] for b in all_blocks) / len(all_blocks)
        avg_words = sum(b['word_count'] for b in all_blocks) / len(all_blocks)
        
        print(f"✅ Saved {len(all_blocks)} blocks from {doc_count} documents")
        print(f"   Average block length: {avg_length:.0f} characters")
        print(f"   Average words per block: {avg_words:.0f}")
        print(f"💾 Output: {SLICED_FILENAME}")
        print(f"📂 Location: {output_path}")
    else:
        print(f"⚠️  Warning: No blocks were created!")
        print(f"   Check MIN_BLOCK_CHARS setting (currently {MIN_BLOCK_CHARS})")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python slicingdata.py <run_directory>")
        print("\nExample:")
        print("  python slicingdata.py AllDatasets/runs/run_2025-12-22_21-11-29_e1b874")
        sys.exit(1)
    
    run_dir = Path(sys.argv[1]).resolve()
    
    if not run_dir.exists() or not run_dir.is_dir():
        print(f"❌ Invalid run directory: {run_dir}")
        sys.exit(1)
    
    try:
        slice_run(run_dir)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)