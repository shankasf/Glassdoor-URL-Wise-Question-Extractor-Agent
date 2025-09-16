import json
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smart_qa_extractor import SmartQAExtractor
from docx_generator import generate_docx_from_qa

def generate_docx_from_json(json_file_path):
    """Generate DOCX file from JSON data"""
    print(f"Processing JSON file: {json_file_path}")
    
    # Extract Q&A pairs
    extractor = SmartQAExtractor(json_file_path)
    qa_pairs = extractor.extract_questions_and_answers()
    
    if not qa_pairs:
        print("No Q&A pairs found")
        return None
    
    # Get company and position from first Q&A pair
    company = qa_pairs[0].get('company', 'Unknown')
    position = qa_pairs[0].get('position', 'Unknown')
    
    print(f"Generating DOCX for {company} {position} interviews...")
    print(f"Total Q&A pairs: {len(qa_pairs)}")
    
    # Generate DOCX in company-specific folder
    company_folder = os.path.join('scraped_data', company)
    os.makedirs(company_folder, exist_ok=True)
    docx_path = generate_docx_from_qa(qa_pairs, company, position, company_folder)
    
    print(f"DOCX file generated: {docx_path}")
    return docx_path

def main():
    json_file = 'scraped_data/tesla_interview_experiences.json'
    
    if not os.path.exists(json_file):
        print(f"JSON file not found: {json_file}")
        return
    
    docx_path = generate_docx_from_json(json_file)
    
    if docx_path:
        print(f"\n✅ Successfully generated DOCX file: {docx_path}")
    else:
        print("❌ Failed to generate DOCX file")

if __name__ == "__main__":
    main()
