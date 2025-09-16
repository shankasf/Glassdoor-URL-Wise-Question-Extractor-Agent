#!/usr/bin/env python3
"""
Simple script to run the Glassdoor Interview Scraper
Usage: python run_scraper.py <glassdoor_interview_url>
"""

import sys
import os

# Add code directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'code'))

from scrape_any_link import scrape_and_generate_docx

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_scraper.py <glassdoor_interview_url>")
        print("\nExample:")
        print("python run_scraper.py \"https://www.glassdoor.com/Interview/Tesla-Software-Engineer-Interview-Questions-EI_IE43129.0,5_KO6,23.htm\"")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print("🚀 Glassdoor Interview Scraper")
    print("=" * 40)
    
    result = scrape_and_generate_docx(url)
    
    if result:
        print(f"\n✅ Success! Files generated:")
        print(f"   📄 DOCX: {result['docx_file']}")
        print(f"   📊 JSON: {result['json_file']}")
    else:
        print("\n❌ Scraping failed. Please check the logs.")

if __name__ == "__main__":
    main()
