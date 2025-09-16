import json
import re
from datetime import datetime
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class QuestionAnswerExtractor:
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
                if not full_text or len(full_text) < 50:
                    continue
                
                # Extract Q&A pairs from full_text
                qa_pairs = self.parse_qa_from_text(full_text)
                
                for qa in qa_pairs:
                    qa['company'] = company
                    qa['position'] = position
                    qa['experience_index'] = experience.get('index', 0)
                    qa['date'] = experience.get('date', '')
                    qa['location'] = experience.get('location', '')
                    qa['outcome'] = experience.get('outcome', '')
                    qa['difficulty'] = experience.get('difficulty', '')
                    qa['experience_rating'] = experience.get('experience_rating', '')
                    
                    self.extracted_qa.append(qa)
        
        print(f"Extracted {len(self.extracted_qa)} question-answer pairs")
        return self.extracted_qa
    
    def parse_qa_from_text(self, text):
        """Parse questions and answers from text"""
        qa_pairs = []
        
        # Look for question patterns
        question_patterns = [
            r'Question\s+\d+[:\-]?\s*(.+?)(?=Question\s+\d+|Answer question|Helpful|Share|$)',
            r'Q\d*[:\-]?\s*(.+?)(?=Q\d*|Answer question|Helpful|Share|$)',
            r'Interview questions?\s*\[?\d*\]?\s*[:\-]?\s*(.+?)(?=Interview|Answer question|Helpful|Share|$)',
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
            r'I was asked\s+(.+?)(?=\?|Answer question|Helpful|Share|$)'
        ]
        
        for pattern in question_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                question = match.strip()
                if len(question) > 10 and len(question) < 500:
                    # Try to find corresponding answer
                    answer = self.find_answer_for_question(text, question)
                    
                    qa_pairs.append({
                        'question': question,
                        'answer': answer,
                        'source_text': text[:200] + '...' if len(text) > 200 else text
                    })
        
        # Remove duplicates
        unique_qa = []
        seen_questions = set()
        for qa in qa_pairs:
            if qa['question'].lower() not in seen_questions:
                unique_qa.append(qa)
                seen_questions.add(qa['question'].lower())
        
        return unique_qa
    
    def find_answer_for_question(self, text, question):
        """Find answer for a specific question in the text"""
        # Look for answer patterns after the question
        answer_patterns = [
            r'Answer question\s*(.+?)(?=Helpful|Share|Question|$)',
            r'Answer\s*(.+?)(?=Helpful|Share|Question|$)',
            r'Interview\s*(.+?)(?=Helpful|Share|Question|$)',
            r'The interview\s*(.+?)(?=Helpful|Share|Question|$)',
            r'I interviewed\s*(.+?)(?=Helpful|Share|Question|$)',
            r'got the HR call\s*(.+?)(?=Helpful|Share|Question|$)',
            r'Interviewer was\s*(.+?)(?=Helpful|Share|Question|$)',
            r'Was asked to\s*(.+?)(?=Helpful|Share|Question|$)',
            r'Problem quite hard\s*(.+?)(?=Helpful|Share|Question|$)',
            r'Not a simple\s*(.+?)(?=Helpful|Share|Question|$)',
            r'comprehensive and ask\s*(.+?)(?=Helpful|Share|Question|$)',
            r'understanding of\s*(.+?)(?=Helpful|Share|Question|$)',
            r'front end and react\s*(.+?)(?=Helpful|Share|Question|$)',
            r'write a library\s*(.+?)(?=Helpful|Share|Question|$)',
            r'worded in a way\s*(.+?)(?=Helpful|Share|Question|$)',
            r'unnecessarily difficult\s*(.+?)(?=Helpful|Share|Question|$)',
            r'medium question\s*(.+?)(?=Helpful|Share|Question|$)',
            r'little bland\s*(.+?)(?=Helpful|Share|Question|$)',
            r'help me out\s*(.+?)(?=Helpful|Share|Question|$)',
            r'feel the question\s*(.+?)(?=Helpful|Share|Question|$)'
        ]
        
        for pattern in answer_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                answer = match.group(1).strip()
                if len(answer) > 10:
                    return answer
        
        # If no specific answer found, extract context around the question
        question_pos = text.lower().find(question.lower())
        if question_pos != -1:
            # Get text after the question
            after_question = text[question_pos + len(question):]
            # Take first 200 characters as potential answer
            potential_answer = after_question[:200].strip()
            if len(potential_answer) > 20:
                return potential_answer
        
        return "No specific answer found in the interview experience."
    
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
    
    extractor = QuestionAnswerExtractor(json_file)
    qa_pairs = extractor.extract_questions_and_answers()
    
    if qa_pairs:
        print(f"\nExtracted {len(qa_pairs)} question-answer pairs")
        
        # Show sample Q&A
        print("\nSample Question-Answer Pairs:")
        for i, qa in enumerate(qa_pairs[:3]):
            print(f"\n--- Q&A {i+1} ---")
            print(f"Question: {qa['question']}")
            print(f"Answer: {qa['answer']}")
            print(f"Company: {qa['company']}")
            print(f"Position: {qa['position']}")
            print(f"Difficulty: {qa['difficulty']}")
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
