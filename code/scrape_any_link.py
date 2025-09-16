#!/usr/bin/env python3
"""
Universal Glassdoor Interview Scraper
Usage: python scrape_any_link.py <glassdoor_interview_url>
"""

import sys
import os
import argparse
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from universal_interview_scraper import UniversalInterviewScraper
from smart_qa_extractor import SmartQAExtractor
from docx_generator import generate_docx_from_qa

def scrape_and_generate_docx(url, output_prefix=None):
    """Scrape a Glassdoor interview URL and generate DOCX file"""
    print(f"🚀 Starting scrape for: {url}")
    
    scraper = UniversalInterviewScraper()
    
    try:
        # Setup driver
        if not scraper.setup_driver():
            print("❌ Failed to setup Chrome driver")
            return None
        
        # Scrape the interview page
        print("📊 Scraping interview page...")
        data = scraper.scrape_interview_page(url)
        
        if not data:
            print("❌ Failed to scrape interview page")
            return None
        
        print(f"✅ Successfully scraped {data['total_interviews']} interview experiences")
        print(f"🏢 Company: {data['company']}")
        print(f"💼 Position: {data['position']}")
        
        # Save to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f'interview_data_{timestamp}.json'
        json_file = scraper.save_to_json(json_filename)
        
        if not json_file:
            print("❌ Failed to save JSON file")
            return None
        
        print(f"💾 JSON file saved: {json_file}")
        
        # Extract Q&A pairs
        print("🔍 Extracting questions and answers...")
        extractor = SmartQAExtractor(json_file)
        qa_pairs = extractor.extract_questions_and_answers()
        
        if not qa_pairs:
            print("❌ No Q&A pairs found")
            return None
        
        print(f"📝 Extracted {len(qa_pairs)} question-answer pairs")
        
        # Generate DOCX in company-specific folder
        print("📄 Generating DOCX file...")
        company = data['company']
        position = data['position']
        
        # Create company-specific folder
        company_folder = os.path.join('scraped_data', company)
        os.makedirs(company_folder, exist_ok=True)
        
        if output_prefix:
            docx_filename = f'{output_prefix}_{company}_{position}_{timestamp}.docx'
        else:
            docx_filename = f'{company}_{position}_interviews_{timestamp}.docx'
        
        docx_path = generate_docx_from_qa(qa_pairs, company, position, company_folder)
        
        if docx_path:
            # Rename the file if we have a custom prefix
            if output_prefix:
                new_docx_path = os.path.join(company_folder, docx_filename)
                os.rename(docx_path, new_docx_path)
                docx_path = new_docx_path
            
            print(f"✅ DOCX file generated: {docx_path}")
            
            # Show summary
            print(f"\n📊 Summary:")
            print(f"   Company: {company}")
            print(f"   Position: {position}")
            print(f"   Total Experiences: {data['total_interviews']}")
            print(f"   Q&A Pairs: {len(qa_pairs)}")
            print(f"   JSON File: {json_file}")
            print(f"   DOCX File: {docx_path}")
            
            return {
                'json_file': json_file,
                'docx_file': docx_path,
                'company': company,
                'position': position,
                'total_experiences': data['total_interviews'],
                'qa_pairs': len(qa_pairs)
            }
        else:
            print("❌ Failed to generate DOCX file")
            return None
            
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        return None
    
    finally:
        scraper.close()

def main():
    parser = argparse.ArgumentParser(
        description='Universal Glassdoor Interview Scraper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scrape_any_link.py "https://www.glassdoor.com/Interview/Tesla-Software-Engineer-Interview-Questions-EI_IE43129.0,5_KO6,23.htm"
  python scrape_any_link.py "https://www.glassdoor.com/Interview/Google-Software-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,20.htm" --output google_swe
        """
    )
    
    parser.add_argument('url', help='Glassdoor interview URL to scrape')
    parser.add_argument('--output', '-o', help='Output filename prefix (optional)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Validate URL
    if 'glassdoor.com' not in args.url or 'Interview' not in args.url:
        print("❌ Error: Please provide a valid Glassdoor interview URL")
        print("   Example: https://www.glassdoor.com/Interview/Company-Position-Interview-Questions-EI_IE12345.0,5_KO6,23.htm")
        sys.exit(1)
    
    print("🔧 Universal Glassdoor Interview Scraper")
    print("=" * 50)
    
    result = scrape_and_generate_docx(args.url, args.output)
    
    if result:
        print(f"\n🎉 Scraping completed successfully!")
        print(f"📁 Check the 'scraped_data' folder for your files")
    else:
        print(f"\n💥 Scraping failed. Please check the logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
