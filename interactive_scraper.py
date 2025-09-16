#!/usr/bin/env python3
"""
Interactive Glassdoor Interview Scraper
Usage: python interactive_scraper.py
"""

import sys
import os
import re
from datetime import datetime

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

def get_user_input():
    """Get URL input from user with validation"""
    print("🚀 Interactive Glassdoor Interview Scraper")
    print("=" * 50)
    print()
    print("📝 Enter a Glassdoor interview URL to scrape:")
    print("   Example: https://www.glassdoor.com/Interview/Tesla-Software-Engineer-Interview-Questions-EI_IE43129.0,5_KO6,23.htm")
    print()
    
    while True:
        url = input("🔗 URL: ").strip()
        
        if not url:
            print("❌ Please enter a URL")
            continue
        
        if url.lower() in ['exit', 'quit', 'q']:
            print("👋 Goodbye!")
            sys.exit(0)
        
        if not validate_glassdoor_url(url):
            print("❌ Invalid Glassdoor interview URL. Please check the format.")
            print("   Make sure it's a Glassdoor interview page URL")
            print("   Example: https://www.glassdoor.com/Interview/Company-Position-Interview-Questions-EI_IE12345.0,5_KO6,23.htm")
            print()
            continue
        
        return url

def show_examples():
    """Show example URLs"""
    print("\n📚 Example URLs you can try:")
    print("   • Tesla Software Engineer:")
    print("     https://www.glassdoor.com/Interview/Tesla-Software-Engineer-Interview-Questions-EI_IE43129.0,5_KO6,23.htm")
    print()
    print("   • Google Software Engineer:")
    print("     https://www.glassdoor.com/Interview/Google-Software-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,20.htm")
    print()
    print("   • Microsoft Data Scientist:")
    print("     https://www.glassdoor.com/Interview/Microsoft-Data-Scientist-Interview-Questions-EI_IE1651.0,9_KO10,24.htm")
    print()
    print("   • Amazon Software Engineer:")
    print("     https://www.glassdoor.com/Interview/Amazon-Software-Engineer-Interview-Questions-EI_IE6036.0,6_KO7,20.htm")
    print()

def main():
    """Main interactive function"""
    try:
        while True:
            print("\n" + "="*60)
            print("🎯 What would you like to do?")
            print("1. Scrape a Glassdoor interview URL")
            print("2. Show example URLs")
            print("3. Exit")
            print("="*60)
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                url = get_user_input()
                
                print(f"\n🚀 Starting scrape for: {url}")
                print("⏳ This may take a few minutes...")
                print()
                
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
                
                print("\n" + "="*60)
                continue_choice = input("Press Enter to continue or 'q' to quit: ").strip()
                if continue_choice.lower() in ['q', 'quit', 'exit']:
                    break
                    
            elif choice == '2':
                show_examples()
                input("\nPress Enter to continue...")
                
            elif choice == '3':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please try again or check the logs for more details.")

if __name__ == "__main__":
    main()
