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
import re
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
def setup_logging():
    """Setup comprehensive logging"""
    # Create logs directory in parent folder
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_dir, f'enhanced_tesla_{timestamp}.log')
    
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

class EnhancedTeslaScraper:
    def __init__(self):
        self.logger = setup_logging()
        self.driver = None
        self.scraped_data = []
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.logger.info("EnhancedTeslaScraper initialized")
        
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
        
        # Extract questions
        questions = self.extract_questions_from_text(text)
        experience['questions'] = questions
        
        # Extract full text
        experience['full_text'] = text
        
        return experience
    
    def extract_questions_from_text(self, text):
        """Extract interview questions from text"""
        questions = []
        
        # Look for question patterns
        question_patterns = [
            r'Question\s+\d+[:\-]?\s*(.+?)(?=Question\s+\d+|$)',
            r'Q\d*[:\-]?\s*(.+?)(?=Q\d*|$)',
            r'Interview questions?\s*[:\-]?\s*(.+?)(?=Interview|$)',
            r'What\s+(.+?)\?',
            r'How\s+(.+?)\?',
            r'Why\s+(.+?)\?',
            r'Describe\s+(.+?)(?=\?|$)',
            r'Explain\s+(.+?)(?=\?|$)',
            r'Tell me about\s+(.+?)(?=\?|$)'
        ]
        
        for pattern in question_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                question = match.strip()
                if len(question) > 10 and len(question) < 500:
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
            'I interviewed at Tesla',
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
                
                # Extract questions from this section
                current_experience['questions'] = self.extract_questions_from_text(section)
            elif current_experience:
                # Continue building current experience
                current_experience['full_text'] += '\n\n' + section
                current_experience['questions'].extend(self.extract_questions_from_text(section))
        
        if current_experience:
            experiences.append(current_experience)
        
        return experiences
    
    def scrape_tesla_interviews(self, url):
        """Scrape Tesla interview experiences with detailed extraction"""
        self.logger.info(f"Starting to scrape Tesla interviews: {url}")
        
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
            html_filename = os.path.join(self.base_dir, 'scraped_data', f'tesla_interviews_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(page_source)
            self.logger.info(f"HTML saved to {html_filename}")
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Extract page metadata
            page_data = {
                'url': url,
                'scraped_at': datetime.now().isoformat(),
                'title': '',
                'company': 'Tesla',
                'position': 'Software Engineer',
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
            self.logger.error(f"Error scraping Tesla interviews: {e}")
            return None
    
    def save_to_json(self, filename='tesla_interview_experiences.json'):
        """Save scraped data to JSON file"""
        try:
            filepath = os.path.join(self.base_dir, 'scraped_data', filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Data saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving to JSON: {e}")
    
    def save_questions_to_csv(self, filename='tesla_interview_questions.csv'):
        """Save interview questions to CSV file"""
        try:
            import csv
            
            filepath = os.path.join(self.base_dir, 'scraped_data', filename)
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['experience_index', 'question', 'date', 'location', 'outcome', 'difficulty', 'experience_rating']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for page_data in self.scraped_data:
                    for experience in page_data.get('interview_experiences', []):
                        for question in experience.get('questions', []):
                            writer.writerow({
                                'experience_index': experience.get('index', ''),
                                'question': question,
                                'date': experience.get('date', ''),
                                'location': experience.get('location', ''),
                                'outcome': experience.get('outcome', ''),
                                'difficulty': experience.get('difficulty', ''),
                                'experience_rating': experience.get('experience_rating', '')
                            })
            
            self.logger.info(f"Questions saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving to CSV: {e}")
    
    def print_summary(self):
        """Print summary of scraped data"""
        print("\n" + "="*80)
        print("TESLA INTERVIEW EXPERIENCES SCRAPING RESULTS")
        print("="*80)
        
        for page_data in self.scraped_data:
            print(f"\nCompany: {page_data['company']}")
            print(f"Position: {page_data['position']}")
            print(f"Total Interview Experiences: {page_data['total_interviews']}")
            print(f"URL: {page_data['url']}")
            
            for i, experience in enumerate(page_data['interview_experiences'][:5]):  # Show first 5
                print(f"\n--- Experience {i+1} ---")
                print(f"Title: {experience.get('title', 'N/A')}")
                print(f"Date: {experience.get('date', 'N/A')}")
                print(f"Location: {experience.get('location', 'N/A')}")
                print(f"Outcome: {experience.get('outcome', 'N/A')}")
                print(f"Difficulty: {experience.get('difficulty', 'N/A')}")
                print(f"Experience Rating: {experience.get('experience_rating', 'N/A')}")
                print(f"Questions Found: {len(experience.get('questions', []))}")
                
                if experience.get('questions'):
                    print("Sample Questions:")
                    for j, question in enumerate(experience['questions'][:3]):  # Show first 3 questions
                        print(f"  {j+1}. {question[:100]}...")
                
                print("-" * 60)
    
    def close(self):
        """Close the driver"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Chrome driver closed")

def main():
    url = "https://www.glassdoor.com/Interview/Tesla-Software-Engineer-Interview-Questions-EI_IE43129.0,5_KO6,23.htm"
    
    scraper = EnhancedTeslaScraper()
    
    try:
        # Setup driver
        if not scraper.setup_driver():
            print("Failed to setup Chrome driver")
            return
        
        # Scrape Tesla interviews
        print(f"\nScraping Tesla interview experiences...")
        data = scraper.scrape_tesla_interviews(url)
        
        if data:
            print(f"Successfully scraped {data['total_interviews']} interview experiences")
            
            # Print summary
            scraper.print_summary()
            
            # Save to files
            scraper.save_to_json()
            scraper.save_questions_to_csv()
            
            print(f"\nScraping completed successfully!")
            print(f"Data saved to scraped_data/ folder")
        else:
            print("Failed to scrape interview experiences")
            
    except Exception as e:
        print(f"Error occurred during scraping: {str(e)}")
        scraper.logger.error(f"Fatal error: {e}", exc_info=True)
    
    finally:
        scraper.close()

if __name__ == "__main__":
    main()