import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import time
import random
import json
import logging
from datetime import datetime
import os
import sys
import re
import argparse
from urllib.parse import urlparse

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from question_answer_extractor import QuestionAnswerExtractor
from docx_generator import generate_docx_from_qa

# Setup logging
def setup_logging():
    """Setup comprehensive logging"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f'logs/universal_scraper_{timestamp}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_filename}")
    return logger

class UniversalInterviewScraper:
    def __init__(self):
        self.logger = setup_logging()
        self.driver = None
        self.scraped_data = []
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.logger.info("UniversalInterviewScraper initialized")
        
    def setup_driver(self):
        """Setup undetected Chrome driver with minimal options"""
        self.logger.info("Setting up undetected Chrome driver...")
        
        try:
            # Use minimal options to avoid compatibility issues
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
            
            # Create driver
            self.driver = uc.Chrome(options=options)
            
            self.logger.info("Chrome driver setup completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to setup Chrome driver: {e}")
            return False
    
    def wait_for_page_load(self, timeout=30):
        """Wait for page to load completely"""
        self.logger.info("Waiting for page to load...")
        
        try:
            # Wait for body element
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Additional wait for dynamic content
            time.sleep(5)
            
            # Check if we're still on a challenge page
            page_source = self.driver.page_source.lower()
            if any(indicator in page_source for indicator in [
                "cloudflare", "checking your browser", "just a moment", 
                "ddos protection", "security check"
            ]):
                self.logger.info("Challenge page detected, waiting longer...")
                time.sleep(10)
            
            self.logger.info("Page loaded successfully")
            return True
            
        except TimeoutException:
            self.logger.warning("Page load timeout")
            return False
        except Exception as e:
            self.logger.error(f"Error waiting for page load: {e}")
            return False
    
    def extract_company_and_position(self, url, soup):
        """Extract company and position from URL and page content"""
        # Extract from URL
        url_parts = url.split('/')
        company = "Unknown"
        position = "Unknown"
        
        # Look for company and position in URL
        for part in url_parts:
            if 'Interview' in part:
                # Extract company and position from URL pattern
                # Example: Tesla-Software-Engineer-Interview-Questions
                if '-' in part:
                    parts = part.split('-')
                    if len(parts) >= 3:
                        company = parts[0]
                        position = ' '.join(parts[1:-2])  # Everything between company and "Interview"
        
        # Try to extract from page title
        title_element = soup.find('title')
        if title_element:
            title = title_element.get_text()
            # Pattern: "Company Position Interview Questions | Glassdoor"
            if 'Interview Questions' in title:
                title_parts = title.split('Interview Questions')[0].strip()
                if '|' in title_parts:
                    title_parts = title_parts.split('|')[0].strip()
                
                # Split by common separators
                for separator in [' ', '-', '_']:
                    if separator in title_parts:
                        parts = title_parts.split(separator)
                        if len(parts) >= 2:
                            company = parts[0]
                            position = ' '.join(parts[1:])
                        break
        
        # Clean company name for folder usage
        company = self.clean_company_name(company)
        
        return company, position
    
    def clean_company_name(self, company):
        """Clean company name for use in folder names"""
        if not company or company == "Unknown":
            return "Unknown"
        
        # Remove special characters and normalize
        import re
        company = re.sub(r'[^\w\s-]', '', company)
        company = re.sub(r'\s+', '_', company.strip())
        company = company.replace('__', '_')
        
        return company
    
    def extract_interview_experiences(self, soup):
        """Extract detailed interview experiences from the page"""
        self.logger.info("Extracting interview experiences...")
        
        experiences = []
        
        # Look for interview experience containers
        experience_selectors = [
            'div[data-test="InterviewReview"]',
            '.interview-review',
            '.review-container',
            'div[class*="interview"]',
            'div[class*="review"]',
            'article[class*="interview"]',
            'section[class*="interview"]'
        ]
        
        for selector in experience_selectors:
            elements = soup.select(selector)
            if elements:
                self.logger.info(f"Found {len(elements)} elements with selector: {selector}")
                
                for i, element in enumerate(elements):
                    try:
                        experience = self.parse_interview_experience(element, i+1)
                        if experience:
                            experiences.append(experience)
                            self.logger.info(f"Extracted experience {i+1}: {experience.get('title', 'No title')[:50]}...")
                    except Exception as e:
                        self.logger.error(f"Error parsing experience {i+1}: {e}")
                        continue
                
                if experiences:
                    break
        
        # If no specific containers found, try to extract from general content
        if not experiences:
            self.logger.info("No specific interview containers found, trying general extraction...")
            experiences = self.extract_from_general_content(soup)
        
        self.logger.info(f"Total experiences extracted: {len(experiences)}")
        return experiences
    
    def parse_interview_experience(self, element, index):
        """Parse individual interview experience"""
        experience = {
            'index': index,
            'title': '',
            'date': '',
            'location': '',
            'outcome': '',
            'difficulty': '',
            'experience_rating': '',
            'interview_process': '',
            'questions': [],
            'advice': '',
            'full_text': ''
        }
        
        # Extract title/header
        title_selectors = ['h3', 'h4', '.title', '.header', '[class*="title"]', '[class*="header"]']
        for selector in title_selectors:
            title_elem = element.select_one(selector)
            if title_elem:
                experience['title'] = title_elem.get_text(strip=True)
                break
        
        # Extract date
        date_patterns = [
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}',
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{4}-\d{2}-\d{2}'
        ]
        
        text = element.get_text()
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                experience['date'] = match.group()
                break
        
        # Extract location
        location_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s+[A-Z]{2})',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s+[A-Z][a-z]+)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text)
            if match:
                experience['location'] = match.group()
                break
        
        # Extract outcome
        outcome_keywords = ['offer', 'no offer', 'declined', 'accepted', 'rejected']
        for keyword in outcome_keywords:
            if keyword.lower() in text.lower():
                experience['outcome'] = keyword
                break
        
        # Extract difficulty
        difficulty_keywords = ['difficult', 'easy', 'average', 'hard', 'medium']
        for keyword in difficulty_keywords:
            if keyword.lower() in text.lower():
                experience['difficulty'] = keyword
                break
        
        # Extract experience rating
        rating_patterns = [
            r'(positive|negative|neutral)\s+experience',
            r'experience.*?(positive|negative|neutral)'
        ]
        
        for pattern in rating_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                experience['experience_rating'] = match.group(1).lower()
                break
        
        # Extract questions from text
        questions = self.extract_questions_from_text(text)
        experience['questions'] = questions
        
        # Extract full text
        experience['full_text'] = text
        
        return experience
    
    def extract_questions_from_text(self, text):
        """Extract interview questions from text"""
        questions = []
        
        # Look for specific question patterns in Glassdoor format
        question_patterns = [
            r'Question\s+\d+[:\-]?\s*(.+?)(?=Answer question|Helpful|Share|Question\s+\d+|$)',
            r'Q\d*[:\-]?\s*(.+?)(?=Answer question|Helpful|Share|Q\d*|$)',
            r'Interview questions?\s*\[?\d*\]?\s*[:\-]?\s*(.+?)(?=Answer question|Helpful|Share|Interview|$)',
            r'What\s+(.+?)(?=\?|Answer question|Helpful|Share|$)',
            r'How\s+(.+?)(?=\?|Answer question|Helpful|Share|$)',
            r'Why\s+(.+?)(?=\?|Answer question|Helpful|Share|$)',
            r'Describe\s+(.+?)(?=\?|Answer question|Helpful|Share|$)',
            r'Explain\s+(.+?)(?=\?|Answer question|Helpful|Share|$)',
            r'Tell me about\s+(.+?)(?=\?|Answer question|Helpful|Share|$)',
            r'If you were to\s+(.+?)(?=\?|Answer question|Helpful|Share|$)',
            r'Does\s+(.+?)(?=\?|Answer question|Helpful|Share|$)',
            r'Some\s+(.+?)(?=\?|Answer question|Helpful|Share|$)',
            r'They asked about\s+(.+?)(?=\?|Answer question|Helpful|Share|$)',
            r'I was asked\s+(.+?)(?=\?|Answer question|Helpful|Share|$)',
            r'Leetcode like\s+(.+?)(?=Answer question|Helpful|Share|$)',
            r'Design a\s+(.+?)(?=Answer question|Helpful|Share|$)',
            r'Past projects\s+(.+?)(?=Answer question|Helpful|Share|$)',
            r'current work\s+(.+?)(?=Answer question|Helpful|Share|$)',
            r'hobbies etc\s+(.+?)(?=Answer question|Helpful|Share|$)',
            r'Tell me about your experience\s+(.+?)(?=Answer question|Helpful|Share|$)',
            r'large-scale distributed\s+(.+?)(?=Answer question|Helpful|Share|$)',
            r'If you were to describe yourself\s+(.+?)(?=Answer question|Helpful|Share|$)',
            r'Does a hotdog\s+(.+?)(?=Answer question|Helpful|Share|$)',
            r'Describe your most difficult\s+(.+?)(?=Answer question|Helpful|Share|$)',
            r'Some hardware related\s+(.+?)(?=Answer question|Helpful|Share|$)',
            r'Power system and LabView\s+(.+?)(?=Answer question|Helpful|Share|$)',
            r'They asked about my experience\s+(.+?)(?=Answer question|Helpful|Share|$)',
            r'I was asked a question on\s+(.+?)(?=Answer question|Helpful|Share|$)'
        ]
        
        for pattern in question_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                question = match.strip()
                if len(question) > 10 and len(question) < 500:
                    # Clean up the question
                    question = question.replace("Answer questionHelpfulShare", "")
                    question = question.replace("HelpfulShare", "")
                    question = re.sub(r'\s+', ' ', question)
                    questions.append(question)
        
        # Remove duplicates and clean up
        questions = list(set(questions))
        questions = [q.strip() for q in questions if q.strip()]
        
        return questions[:10]  # Limit to 10 questions per experience
    
    def extract_from_general_content(self, soup):
        """Extract experiences from general page content"""
        experiences = []
        
        # Get all text and split into potential interview experiences
        all_text = soup.get_text()
        
        # Look for interview experience indicators
        experience_indicators = [
            'I interviewed at',
            'Interview process',
            'Interview questions',
            'Software Engineer Interview',
            'Anonymous Interview Candidate'
        ]
        
        # Split text into sections
        sections = re.split(r'\n\s*\n', all_text)
        
        current_experience = None
        for section in sections:
            section = section.strip()
            if not section or len(section) < 50:
                continue
            
            # Check if this section contains interview experience
            if any(indicator in section for indicator in experience_indicators):
                if current_experience:
                    experiences.append(current_experience)
                
                current_experience = {
                    'index': len(experiences) + 1,
                    'title': 'Interview Experience',
                    'date': '',
                    'location': '',
                    'outcome': '',
                    'difficulty': '',
                    'experience_rating': '',
                    'interview_process': '',
                    'questions': [],
                    'advice': '',
                    'full_text': section
                }
            elif current_experience:
                # Continue building current experience
                current_experience['full_text'] += '\n\n' + section
        
        if current_experience:
            experiences.append(current_experience)
        
        return experiences
    
    def scrape_interview_page(self, url):
        """Scrape interview page with Cloudflare bypass"""
        self.logger.info(f"Starting to scrape interview page: {url}")
        
        try:
            # Navigate to the page
            self.logger.info("Navigating to page...")
            self.driver.get(url)
            
            # Wait for page to load
            if not self.wait_for_page_load():
                self.logger.error("Page failed to load properly")
                return None
            
            # Get page source
            page_source = self.driver.page_source
            self.logger.info(f"Page source length: {len(page_source)} characters")
            
            # Save HTML for debugging
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_filename = os.path.join(self.base_dir, 'scraped_data', f'interview_page_{timestamp}.html')
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(page_source)
            self.logger.info(f"HTML saved to {html_filename}")
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Extract company and position
            company, position = self.extract_company_and_position(url, soup)
            
            # Extract page metadata
            page_data = {
                'url': url,
                'scraped_at': datetime.now().isoformat(),
                'title': '',
                'company': company,
                'position': position,
                'total_interviews': 0,
                'interview_experiences': []
            }
            
            # Extract title
            title_element = soup.find('title')
            if title_element:
                page_data['title'] = title_element.get_text(strip=True)
                self.logger.info(f"Page title: {page_data['title']}")
            
            # Extract interview experiences
            experiences = self.extract_interview_experiences(soup)
            page_data['interview_experiences'] = experiences
            page_data['total_interviews'] = len(experiences)
            
            self.logger.info(f"Successfully extracted {len(experiences)} interview experiences")
            
            self.scraped_data.append(page_data)
            return page_data
            
        except Exception as e:
            self.logger.error(f"Error scraping interview page: {e}")
            return None
    
    def save_to_json(self, filename=None):
        """Save scraped data to JSON file in company-specific folder"""
        try:
            # Get company name from scraped data
            company = "Unknown"
            if self.scraped_data and len(self.scraped_data) > 0:
                company = self.scraped_data[0].get('company', 'Unknown')
            
            # Create company-specific folder
            company_folder = os.path.join(self.base_dir, 'scraped_data', company)
            os.makedirs(company_folder, exist_ok=True)
            
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f'interview_data_{timestamp}.json'
            
            filepath = os.path.join(company_folder, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Data saved to {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Error saving to JSON: {e}")
            return None
    
    def process_and_generate_docx(self, json_file_path):
        """Process JSON data and generate DOCX file"""
        self.logger.info("Processing JSON data and generating DOCX...")
        
        # Extract Q&A pairs
        extractor = QuestionAnswerExtractor(json_file_path)
        qa_pairs = extractor.extract_questions_and_answers()
        
        if not qa_pairs:
            self.logger.warning("No Q&A pairs found")
            return None
        
        # Get company and position from first Q&A pair
        company = qa_pairs[0].get('company', 'Unknown')
        position = qa_pairs[0].get('position', 'Unknown')
        
        # Generate DOCX in company-specific folder
        company_folder = os.path.join(self.base_dir, 'scraped_data', company)
        docx_path = generate_docx_from_qa(qa_pairs, company, position, company_folder)
        
        self.logger.info(f"DOCX file generated: {docx_path}")
        return docx_path
    
    def close(self):
        """Close the driver"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Chrome driver closed")

def main():
    parser = argparse.ArgumentParser(description='Universal Interview Scraper for Glassdoor')
    parser.add_argument('url', help='Glassdoor interview URL to scrape')
    parser.add_argument('--output', '-o', help='Output filename prefix (optional)')
    
    args = parser.parse_args()
    
    scraper = UniversalInterviewScraper()
    
    try:
        # Setup driver
        if not scraper.setup_driver():
            print("Failed to setup Chrome driver")
            return
        
        # Scrape the interview page
        print(f"\nScraping interview page: {args.url}")
        data = scraper.scrape_interview_page(args.url)
        
        if data:
            print(f"Successfully scraped {data['total_interviews']} interview experiences")
            print(f"Company: {data['company']}")
            print(f"Position: {data['position']}")
            
            # Save to JSON
            json_file = scraper.save_to_json()
            
            if json_file:
                # Process and generate DOCX
                docx_file = scraper.process_and_generate_docx(json_file)
                
                if docx_file:
                    print(f"\nScraping completed successfully!")
                    print(f"JSON file: {json_file}")
                    print(f"DOCX file: {docx_file}")
                else:
                    print("Failed to generate DOCX file")
            else:
                print("Failed to save JSON file")
        else:
            print("Failed to scrape interview page")
            
    except Exception as e:
        print(f"Error occurred during scraping: {str(e)}")
        scraper.logger.error(f"Fatal error: {e}", exc_info=True)
    
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
