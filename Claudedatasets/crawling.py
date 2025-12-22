"""
Web Scraper for Beauty Websites
Can be run standalone OR called by pipeline.py

Standalone usage:
    python crawling.py
    
Pipeline usage:
    python crawling.py <url> <output_dir> <max_pages> <delay>
"""
import sys
import os
# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
import time
import json
from datetime import datetime
from collections import deque
from pathlib import Path

class BeautyWebsiteScraper:
    def __init__(self, base_url, max_pages=100, delay=1):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.visited_urls = set()
        self.seen_urls = set([self.base_url])
        self.queue = deque([self.base_url])
        self.scraped_data = []
        self.max_pages = max_pages
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
        }
        self.SKIP_KEYWORDS = ['login', 'signup', 'register', 'cart', 'checkout', 'account', 'search', 'filter', 'privacy', 'terms', 'policy', 'cookie', 'cookies']
        self.SKIP_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.pdf', '.zip', '.mp4', '.mp3')
    
    def is_valid_url(self, url):
        parsed = urlparse(url)
        return parsed.netloc == self.domain or parsed.netloc == ''

    def fetch_page(self, url):
        try:
            print(f"  Scraping: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"  Failed: {url} -> {e}")
            return None

    def extract_links(self, url, soup):
        links = soup.find_all('a', href=True)

        for link in links:
            full_url = urljoin(url, link['href']).split('#')[0]
            full_url = full_url.rstrip('/')

            if not self.is_valid_url(full_url):
                continue

            if any(bad in full_url.lower() for bad in self.SKIP_KEYWORDS):
                continue
            if full_url.lower().endswith(self.SKIP_EXTENSIONS):
                continue
            if full_url in self.seen_urls:
                continue

            self.queue.append(full_url)
            self.seen_urls.add(full_url)

    def classify_page(self, soup):
        text = soup.get_text(" ", strip=True).lower()
        if any(k in text for k in ['ingredient', 'how to use', 'benefits']):
            return 'product'
        if any(k in text for k in ['faq', 'frequently asked', 'shipping', 'returns']):
            return 'faq'
        if any(k in text for k in ['routine', 'step', 'cleanse', 'apply']):
            return 'routine'
        return 'general'

    def extract_page_data(self, url, soup):
        if soup is None:
            return None

        data = {
            'url': url,
            'page_type': self.classify_page(soup),
            'title': soup.title.string.strip() if soup.title else '',
            'meta_description': '',
            'headings': [],
            'paragraphs': [],
            'images': [],
            'lists': [],
            'timestamp': datetime.now().isoformat()
        }

        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            data['meta_description'] = meta_desc.get('content', '')

        for i in range(1, 7):
            for h in soup.find_all(f'h{i}'):
                text = h.get_text(strip=True)
                if text:
                    data['headings'].append({'level': i, 'text': text})

        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if len(text) > 30:
                data['paragraphs'].append(text)

        for img in soup.find_all('img', src=True):
            data['images'].append({
                'src': urljoin(url, img['src']),
                'alt': img.get('alt', '')
            })

        for ul in soup.find_all(['ul', 'ol']):
            items = [li.get_text(strip=True) for li in ul.find_all('li') if li.get_text(strip=True)]
            if items:
                data['lists'].append(items)

        return data

    def crawl(self):
        print(f"\n🕷️  Starting crawl...")
        print(f"  Target: {self.base_url}")
        print(f"  Max pages: {self.max_pages}")
        print(f"  Delay: {self.delay}s\n")
        
        while self.queue and len(self.scraped_data) < self.max_pages:
            url = self.queue.popleft()
            if url in self.visited_urls:
                continue

            soup = self.fetch_page(url)
            self.visited_urls.add(url)

            if soup:
                self.extract_links(url, soup)
                page_data = self.extract_page_data(url, soup)
                if page_data:
                    self.scraped_data.append(page_data)
            
            # Progress update
            if len(self.scraped_data) % 10 == 0 and len(self.scraped_data) > 0:
                print(f"  Progress: {len(self.scraped_data)}/{self.max_pages} pages scraped")

            time.sleep(self.delay)

        return self.scraped_data

    def save_jsonl(self, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            for record in self.scraped_data:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')

    def save_csv(self, output_path):
        rows = []
        for d in self.scraped_data:
            rows.append({
                'url': d['url'],
                'page_type': d['page_type'],
                'title': d['title'],
                'meta_description': d['meta_description'],
                'text': ' '.join(d['paragraphs'])
            })
        pd.DataFrame(rows).to_csv(output_path, index=False)


def main():
    """Main function - handles both standalone and pipeline modes"""
    
    # Check if called by pipeline (with arguments)
    if len(sys.argv) >= 3:
        # Pipeline mode: python crawling.py <url> <output_dir> [max_pages] [delay]
        base_url = sys.argv[1]
        output_dir = Path(sys.argv[2])
        max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        delay = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        
    else:
        # Standalone mode: ask for input
        print("="*60)
        print("🕷️  BEAUTY WEBSITE SCRAPER (Standalone Mode)")
        print("="*60)
        
        base_url = input("Enter base URL to crawl: ").strip()
        
        if not base_url:
            print("❌ No URL provided!")
            sys.exit(1)
        
        # Generate run directory
        from datetime import datetime
        import uuid
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        short_id = uuid.uuid4().hex[:6]
        run_id = f"run_{timestamp}_{short_id}"
        
        output_dir = Path("AllDatasets/runs") / run_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        max_pages = 100
        delay = 1.0
        
        print(f"\n📂 Run directory: {output_dir}")
        print(f"📊 Max pages: {max_pages}")
        print(f"⏱️  Delay: {delay}s\n")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create scraper and run
    scraper = BeautyWebsiteScraper(
        base_url=base_url,
        max_pages=max_pages,
        delay=delay
    )
    
    scraper.crawl()
    
    # Save outputs
    raw_jsonl_path = output_dir / "crawl_raw.jsonl"
    raw_csv_path = output_dir / "crawl_raw.csv"
    
    scraper.save_jsonl(raw_jsonl_path)
    scraper.save_csv(raw_csv_path)
    
    print(f"\n✅ Crawl completed!")
    print(f"  Pages scraped: {len(scraper.scraped_data)}")
    print(f"  Output: {raw_jsonl_path}")
    
    # If standalone mode, show next step
    if len(sys.argv) < 3:
        print(f"\n📝 Next step: Run cleaning")
        print(f"  python cleancrawling.py {output_dir}")


if __name__ == '__main__':
    main()