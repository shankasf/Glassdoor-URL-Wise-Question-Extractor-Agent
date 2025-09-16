import json
import re
from datetime import datetime
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SmartQAExtractor:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.data = self.load_json_data()
        self.extracted_qa = []
        
    def load_json_data(self):
        """Load JSON data from file"""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return []
    
    def clean_question(self, question):
        """Clean and format question text"""
        if not question:
            return ""
        
        # Remove common artifacts
        question = question.replace("Answer questionHelpfulShare", "")
        question = question.replace("HelpfulShare", "")
        question = question.replace("uestion", "question")
        question = question.replace("uestions", "questions")
        
        # Remove leading/trailing whitespace and common prefixes
        question = question.strip()
        
        # Remove common prefixes
        prefixes_to_remove = [
            "Question 1",
            "Question 2", 
            "Question 3",
            "Question 4",
            "Question 5",
            "[1]",
            "[2]",
            "[3]",
            "Interview questions [1]",
            "Interview questions [2]",
            "Interview questions [3]"
        ]
        
        for prefix in prefixes_to_remove:
            if question.startswith(prefix):
                question = question[len(prefix):].strip()
        
        # Clean up the question
        question = re.sub(r'^[:\-\s]+', '', question)  # Remove leading colons, dashes, spaces
        question = re.sub(r'\s+', ' ', question)  # Normalize whitespace
        
        return question
    
    def extract_answer_from_full_text(self, full_text, question):
        """Extract answer from full_text based on the question"""
        if not full_text or not question:
            return "No answer found"
        
        # Look for answer patterns in the full text
        answer_patterns = [
            r'I interviewed at Tesla.*?Interview\s*(.+?)(?=Interview questions|$)',
            r'got the HR call.*?interview\s*(.+?)(?=Interview questions|$)',
            r'Interviewer was.*?interview\s*(.+?)(?=Interview questions|$)',
            r'Was asked to.*?interview\s*(.+?)(?=Interview questions|$)',
            r'Problem quite hard.*?react\s*(.+?)(?=Interview questions|$)',
            r'Not a simple.*?react\s*(.+?)(?=Interview questions|$)',
            r'comprehensive and ask.*?react\s*(.+?)(?=Interview questions|$)',
            r'understanding of.*?react\s*(.+?)(?=Interview questions|$)',
            r'write a library.*?difficult\s*(.+?)(?=Interview questions|$)',
            r'worded in a way.*?difficult\s*(.+?)(?=Interview questions|$)',
            r'unnecessarily difficult\s*(.+?)(?=Interview questions|$)',
            r'medium question.*?difficult\s*(.+?)(?=Interview questions|$)',
            r'little bland.*?difficult\s*(.+?)(?=Interview questions|$)',
            r'help me out.*?difficult\s*(.+?)(?=Interview questions|$)',
            r'feel the question.*?difficult\s*(.+?)(?=Interview questions|$)',
            r'The interview process.*?interview\s*(.+?)(?=Interview questions|$)',
            r'There was an HR rep.*?interview\s*(.+?)(?=Interview questions|$)',
            r'engineers at the panel.*?interview\s*(.+?)(?=Interview questions|$)',
            r'I would recommend.*?interview\s*(.+?)(?=Interview questions|$)',
            r'practicing leetcode.*?interview\s*(.+?)(?=Interview questions|$)',
            r'before the interview.*?questions\s*(.+?)(?=Interview questions|$)',
            r'Interview questions.*?questions\s*(.+?)(?=Interview questions|$)',
            r'Question 1.*?questions\s*(.+?)(?=Interview questions|$)',
            r'Leetcode like.*?questions\s*(.+?)(?=Interview questions|$)',
            r'question about algorithms.*?questions\s*(.+?)(?=Interview questions|$)',
            r'Design a frontend.*?questions\s*(.+?)(?=Interview questions|$)',
            r'for a system.*?questions\s*(.+?)(?=Interview questions|$)',
            r'Past projects.*?questions\s*(.+?)(?=Interview questions|$)',
            r'current work.*?questions\s*(.+?)(?=Interview questions|$)',
            r'hobbies etc.*?questions\s*(.+?)(?=Interview questions|$)',
            r'Tell me about.*?questions\s*(.+?)(?=Interview questions|$)',
            r'your experience.*?questions\s*(.+?)(?=Interview questions|$)',
            r'large-scale distributed.*?questions\s*(.+?)(?=Interview questions|$)',
            r'systems.*?questions\s*(.+?)(?=Interview questions|$)',
            r'If you were to.*?questions\s*(.+?)(?=Interview questions|$)',
            r'describe yourself.*?questions\s*(.+?)(?=Interview questions|$)',
            r'in two words.*?questions\s*(.+?)(?=Interview questions|$)',
            r'what would they be.*?questions\s*(.+?)(?=Interview questions|$)',
            r'Does a hotdog.*?questions\s*(.+?)(?=Interview questions|$)',
            r'split lengthwise.*?questions\s*(.+?)(?=Interview questions|$)',
            r'or widthwise.*?questions\s*(.+?)(?=Interview questions|$)',
            r'why.*?questions\s*(.+?)(?=Interview questions|$)',
            r'Describe your most.*?questions\s*(.+?)(?=Interview questions|$)',
            r'difficult problem.*?questions\s*(.+?)(?=Interview questions|$)',
            r'you solved.*?questions\s*(.+?)(?=Interview questions|$)',
            r'Some hardware.*?questions\s*(.+?)(?=Interview questions|$)',
            r'related questions.*?questions\s*(.+?)(?=Interview questions|$)',
            r'Power system.*?questions\s*(.+?)(?=Interview questions|$)',
            r'and LabView.*?questions\s*(.+?)(?=Interview questions|$)',
            r'They asked about.*?questions\s*(.+?)(?=Interview questions|$)',
            r'my experience.*?questions\s*(.+?)(?=Interview questions|$)',
            r'why I wanna.*?questions\s*(.+?)(?=Interview questions|$)',
            r'work there.*?questions\s*(.+?)(?=Interview questions|$)',
            r'I was asked.*?questions\s*(.+?)(?=Interview questions|$)',
            r'a question on.*?questions\s*(.+?)(?=Interview questions|$)',
            r'DP.*?questions\s*(.+?)(?=Interview questions|$)'
        ]
        
        for pattern in answer_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
            if match:
                answer = match.group(1).strip()
                if len(answer) > 10:
                    # Clean up the answer
                    answer = answer.replace("Answer questionHelpfulShare", "")
                    answer = answer.replace("HelpfulShare", "")
                    answer = re.sub(r'\s+', ' ', answer)
                    return answer
        
        # If no specific pattern matches, try to extract context around the question
        question_lower = question.lower()
        full_text_lower = full_text.lower()
        
        # Find the question in the full text
        question_pos = full_text_lower.find(question_lower)
        if question_pos != -1:
            # Get text after the question
            after_question = full_text[question_pos + len(question):]
            # Take first 300 characters as potential answer
            potential_answer = after_question[:300].strip()
            if len(potential_answer) > 20:
                # Clean up the answer
                potential_answer = potential_answer.replace("Answer questionHelpfulShare", "")
                potential_answer = potential_answer.replace("HelpfulShare", "")
                potential_answer = re.sub(r'\s+', ' ', potential_answer)
                return potential_answer
        
        return "No specific answer found in the interview experience."
    
    def extract_questions_and_answers(self):
        """Extract questions and answers from interview experiences"""
        print("Extracting questions and answers from interview experiences...")
        
        for page_data in self.data:
            if 'interview_experiences' not in page_data:
                continue
                
            company = page_data.get('company', 'Unknown')
            position = page_data.get('position', 'Unknown')
            
            for experience in page_data['interview_experiences']:
                full_text = experience.get('full_text', '')
                questions = experience.get('questions', [])
                
                if not full_text or not questions:
                    continue
                
                # Process each question
                for question in questions:
                    cleaned_question = self.clean_question(question)
                    
                    if len(cleaned_question) < 10:  # Skip very short questions
                        continue
                    
                    # Extract answer from full_text
                    answer = self.extract_answer_from_full_text(full_text, cleaned_question)
                    
                    qa_pair = {
                        'question': cleaned_question,
                        'answer': answer,
                        'company': company,
                        'position': position,
                        'experience_index': experience.get('index', 0),
                        'date': experience.get('date', ''),
                        'location': experience.get('location', ''),
                        'outcome': experience.get('outcome', ''),
                        'difficulty': experience.get('difficulty', ''),
                        'experience_rating': experience.get('experience_rating', ''),
                        'source_text': full_text[:200] + '...' if len(full_text) > 200 else full_text
                    }
                    
                    self.extracted_qa.append(qa_pair)
        
        # Remove duplicates based on question similarity
        unique_qa = []
        seen_questions = set()
        
        for qa in self.extracted_qa:
            question_key = qa['question'].lower().strip()
            if question_key not in seen_questions and len(question_key) > 10:
                unique_qa.append(qa)
                seen_questions.add(question_key)
        
        self.extracted_qa = unique_qa
        print(f"Extracted {len(self.extracted_qa)} unique question-answer pairs")
        return self.extracted_qa
    
    def get_statistics(self):
        """Get statistics about extracted Q&A"""
        if not self.extracted_qa:
            return {}
        
        companies = set(qa['company'] for qa in self.extracted_qa)
        positions = set(qa['position'] for qa in self.extracted_qa)
        difficulties = [qa['difficulty'] for qa in self.extracted_qa if qa['difficulty']]
        outcomes = [qa['outcome'] for qa in self.extracted_qa if qa['outcome']]
        
        return {
            'total_qa_pairs': len(self.extracted_qa),
            'companies': list(companies),
            'positions': list(positions),
            'difficulty_distribution': {d: difficulties.count(d) for d in set(difficulties)},
            'outcome_distribution': {o: outcomes.count(o) for o in set(outcomes)}
        }

def main():
    json_file = 'scraped_data/tesla_interview_experiences.json'
    
    if not os.path.exists(json_file):
        print(f"JSON file not found: {json_file}")
        return
    
    extractor = SmartQAExtractor(json_file)
    qa_pairs = extractor.extract_questions_and_answers()
    
    if qa_pairs:
        print(f"\nExtracted {len(qa_pairs)} unique question-answer pairs")
        
        # Show sample Q&A
        print("\nSample Question-Answer Pairs:")
        for i, qa in enumerate(qa_pairs[:5]):
            print(f"\n--- Q&A {i+1} ---")
            print(f"Question: {qa['question']}")
            print(f"Answer: {qa['answer']}")
            print(f"Company: {qa['company']}")
            print(f"Position: {qa['position']}")
            print(f"Difficulty: {qa['difficulty']}")
            print(f"Outcome: {qa['outcome']}")
            print("-" * 50)
        
        # Get statistics
        stats = extractor.get_statistics()
        print(f"\nStatistics:")
        print(f"Total Q&A pairs: {stats['total_qa_pairs']}")
        print(f"Companies: {', '.join(stats['companies'])}")
        print(f"Positions: {', '.join(stats['positions'])}")
        print(f"Difficulty distribution: {stats['difficulty_distribution']}")
        print(f"Outcome distribution: {stats['outcome_distribution']}")
        
        return qa_pairs
    else:
        print("No question-answer pairs found")
        return []

if __name__ == "__main__":
    main()
