import json
import re
from pathlib import Path
import sys

if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

# Filenames (standardized across all runs)
RAW_FILENAME = "crawl_raw.jsonl"
CLEAN_FILENAME = "crawl_clean.jsonl"

# Common navigation / boilerplate keywords
NAV_KEYWORDS = [
    "all services", "contact", "terms", "policy", "policies",
    "faq", "frequently asked", "shop", "academy", "medical",
    "login", "signup", "register", "copyright"
]

MIN_PARAGRAPH_LEN = 40


def is_navigation_text(text: str) -> bool:
    """Check if text is navigation/boilerplate content"""
    t = text.lower()
    if len(t) < MIN_PARAGRAPH_LEN:
        return True
    return any(k in t for k in NAV_KEYWORDS)


def normalize(text: str) -> str:
    """Normalize whitespace and line breaks"""
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_run(run_dir: Path):
    """Clean the raw crawl data in a run directory"""
    input_path = run_dir / RAW_FILENAME
    output_path = run_dir / CLEAN_FILENAME

    # Validation
    if not input_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_path}")

    if output_path.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {output_path}")

    print(f"📂 Cleaning: {run_dir.name}")
    print(f"📥 Reading from: {RAW_FILENAME}")
    
    cleaned_docs = []
    seen_hashes = set()
    total_input = 0

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            total_input += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue

            paragraphs = row.get("paragraphs", [])
            headings = row.get("headings", [])

            # Filter out navigation text
            kept_paragraphs = [
                p for p in paragraphs if not is_navigation_text(p)
            ]

            if len(kept_paragraphs) == 0:
                continue

            # Build document text
            parts = []

            title = row.get("title", "").strip()
            if title:
                parts.append(title)

            # Keep only h1 + h2
            for h in headings:
                if h["level"] <= 2:
                    parts.append(h["text"])

            parts.extend(kept_paragraphs)

            document = normalize("\n\n".join(parts))

            # Deduplicate
            doc_hash = hash(document)
            if doc_hash in seen_hashes:
                continue
            seen_hashes.add(doc_hash)

            cleaned_docs.append({
                "url": row["url"],
                "page_type": row.get("page_type", "unknown"),
                "text": document
            })

    # Write cleaned output
    with open(output_path, "w", encoding="utf-8") as out:
        for doc in cleaned_docs:
            out.write(json.dumps(doc, ensure_ascii=False) + "\n")

    print(f"✅ Saved {len(cleaned_docs)}/{total_input} clean documents")
    print(f"💾 Output: {CLEAN_FILENAME}")
    print(f"📂 Location: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cleancrawling.py <run_directory>")
        print("\nExample:")
        print("  python cleancrawling.py AllDatasets/runs/run_2025-12-22_21-11-29_e1b874")
        sys.exit(1)

    run_dir = Path(sys.argv[1]).resolve()

    if not run_dir.exists() or not run_dir.is_dir():
        print(f"❌ Invalid run directory: {run_dir}")
        sys.exit(1)

    try:
        clean_run(run_dir)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)