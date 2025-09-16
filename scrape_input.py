#!/usr/bin/env python3
"""
Simple Glassdoor Interview Scraper with Input
Usage: python scrape_input.py
"""

import sys
import os
import re

# Add code directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'code'))

from scrape_any_link import scrape_and_generate_docx

def validate_glassdoor_url(url):
    """Validate if the URL is a Glassdoor interview URL"""
    if not url:
        return False
    
    # Check if it's a Glassdoor URL
    if 'glassdoor.com' not in url.lower():
        return False
    
    # Check if it's an interview URL
    if 'interview' not in url.lower():
        return False
    
    # Check if it has the proper format
    if not re.search(r'Interview.*Questions.*EI_IE\d+', url):
        return False
    
    return True

def main():
    """Main function"""
    print("🚀 Glassdoor Interview Scraper")
    print("=" * 40)
    print()
    print("📝 Enter a Glassdoor interview URL to scrape:")
    print("   Example: https://www.glassdoor.com/Interview/Tesla-Software-Engineer-Interview-Questions-EI_IE43129.0,5_KO6,23.htm")
    print()
    
    # Get URL from user
    url = input("🔗 URL: ").strip()
    
    if not url:
        print("❌ No URL provided. Exiting.")
        sys.exit(1)
    
    # Validate URL
    if not validate_glassdoor_url(url):
        print("❌ Invalid Glassdoor interview URL.")
        print("   Make sure it's a Glassdoor interview page URL")
        print("   Example: https://www.glassdoor.com/Interview/Company-Position-Interview-Questions-EI_IE12345.0,5_KO6,23.htm")
        sys.exit(1)
    
    print(f"\n🚀 Starting scrape for: {url}")
    print("⏳ This may take a few minutes...")
    print()
    
    # Scrape the URL
    result = scrape_and_generate_docx(url)
    
    if result:
        print(f"\n✅ Success! Files generated:")
        print(f"   📄 DOCX: {result['docx_file']}")
        print(f"   📊 JSON: {result['json_file']}")
        print(f"   🏢 Company: {result['company']}")
        print(f"   💼 Position: {result['position']}")
        print(f"   📈 Total Experiences: {result['total_experiences']}")
        print(f"   ❓ Q&A Pairs: {result['qa_pairs']}")
        print(f"\n📁 Check the 'scraped_data' folder for your files!")
    else:
        print("\n❌ Scraping failed. Please check the logs and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
