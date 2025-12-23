"""
Tag sliced blocks with predefined roles
Can be run standalone OR called by pipeline.py

Standalone usage:
    python tag_sliced_blocks.py <run_directory>
    
Pipeline usage:
    python tag_sliced_blocks.py <run_directory>
"""

import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

# Load environment
load_dotenv()

# Filenames (standardized across all runs)
SLICED_FILENAME = "crawl_sliced.jsonl"
TAGGED_FILENAME = "crawl_tagged.jsonl"

# Define your roles and keywords (order matters - checked top to bottom)
ROLES = [
    ("TRANSACTIONAL", ["price", "$", "£", "€", "booking", "book now", "buy", "purchase", "order", "payment", "cost", "fee"]),
    ("TEMPORAL", ["schedule", "appointment", "date", "time", "opening hours", "deadline", "hours", "open", "closed", "monday", "tuesday", "wednesday", "thursday", "friday", "available"]),
    ("PROCEDURAL", ["how to", "step", "instruction", "procedure", "guide", "tutorial", "process", "method", "apply", "prepare"]),
    ("PROMOTIONAL", ["offer", "discount", "sale", "promotion", "deal", "special", "limited", "testimonial", "review", "rated"]),
    ("POLICY_LEGAL", ["terms", "privacy", "policy", "regulation", "legal", "conditions", "agreement", "copyright", "disclaimer"]),
    ("CONTACT", ["email", "phone", "contact", "support", "address", "location", "call", "reach us", "get in touch"]),
    ("DESCRIPTIVE", ["what is", "treatment", "procedure", "benefit", "result", "effect", "improve", "enhance", "rejuvenate", "reduce"]),
]


def rule_tag_block(block_text):
    """Simple rule-based tagging with ANY keyword match"""
    text = block_text.lower()
    
    # Check each role in priority order
    for role, keywords in ROLES:
        # If ANY keyword matches, tag with that role
        for keyword in keywords:
            if keyword in text:
                # Calculate a simple confidence based on keyword length
                confidence = min(0.9, 0.6 + (len(keyword) * 0.02))
                return role, confidence
    
    # Default to GENERAL if no keywords match
    return "GENERAL", 0.3


def tag_run(run_dir: Path):
    """Tag the sliced data in a run directory"""
    input_path = run_dir / SLICED_FILENAME
    output_path = run_dir / TAGGED_FILENAME
    
    # Validation
    if not input_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_path}")
    
    if output_path.exists():
        print(f"⚠️  Output file already exists: {output_path}")
        print(f"   Using existing tagged file...")
        return
    
    print(f"📂 Tagging: {run_dir.name}")
    print(f"📥 Reading from: {SLICED_FILENAME}")
    
    tagged_blocks = []
    role_counts = {}
    
    # Load and tag blocks
    with open(input_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                block = json.loads(line)
                role, confidence = rule_tag_block(block["block_text"])
                
                # Add role and confidence to block
                block["role"] = role
                block["confidence"] = round(confidence, 2)
                
                tagged_blocks.append(block)
                
                # Track role counts
                role_counts[role] = role_counts.get(role, 0) + 1
                
                # Progress indicator
                if line_num % 100 == 0:
                    print(f"   Tagged {line_num} blocks...")
                    
            except json.JSONDecodeError:
                print(f"⚠️  Skipping malformed JSON at line {line_num}")
            except Exception as e:
                print(f"⚠️  Error processing line {line_num}: {e}")
    
    # Save tagged blocks
    with open(output_path, "w", encoding="utf-8") as f:
        for block in tagged_blocks:
            f.write(json.dumps(block, ensure_ascii=False) + "\n")
    
    # Statistics
    total_blocks = len(tagged_blocks)
    print(f"\n✅ Tagged {total_blocks} blocks")
    print(f"💾 Output: {TAGGED_FILENAME}")
    print(f"📂 Location: {output_path}")
    
    # Show role distribution
    print(f"\n📊 Role Distribution:")
    for role in sorted(role_counts.keys()):
        count = role_counts[role]
        percentage = (count / total_blocks * 100) if total_blocks > 0 else 0
        print(f"   {role}: {count} ({percentage:.1f}%)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tag_sliced_blocks.py <run_directory>")
        print("\nExample:")
        print("  python tag_sliced_blocks.py AllDatasets/runs/run_2025-12-23_14-00-59_813c0e")
        sys.exit(1)
    
    run_dir = Path(sys.argv[1]).resolve()
    
    if not run_dir.exists() or not run_dir.is_dir():
        print(f"❌ Invalid run directory: {run_dir}")
        sys.exit(1)
    
    try:
        tag_run(run_dir)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
