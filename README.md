# Glassdoor URL Wise Question Extractor Agent

A comprehensive web scraper designed to extract interview questions and experiences from any Glassdoor interview page, with Cloudflare bypass capabilities and automatic DOCX generation.

## Project Structure

```
tesla_scraper/
├── code/                           # Source code
│   ├── enhanced_tesla_scraper.py   # Original Tesla scraper
│   ├── smart_qa_extractor.py      # Smart Q&A extraction from JSON
│   ├── docx_generator.py          # DOCX file generation
│   ├── universal_interview_scraper.py # Universal scraper for any link
│   └── scrape_any_link.py         # Command-line interface
├── scraped_data/                   # Output data folder
│   ├── Tesla/                     # Company-specific folders
│   ├── Google/                    # Company-specific folders
│   ├── Microsoft/                 # Company-specific folders
│   └── *.html                     # Raw HTML for debugging
├── logs/                          # Log files
├── venv/                          # Virtual environment
├── requirements.txt               # Python dependencies
├── interactive_scraper.py         # Interactive mode (recommended)
├── scrape_input.py                # Simple input mode
├── run_scraper.py                 # Command line mode
└── README.md                      # This file
```

## Features

- **🌐 Universal Scraping**: Works with any Glassdoor interview URL
- **🛡️ Cloudflare Bypass**: Uses undetected-chromedriver to bypass protection
- **📝 Smart Q&A Extraction**: Intelligently extracts questions and answers from interview experiences
- **📄 DOCX Generation**: Creates beautifully formatted Word documents
- **📊 Multiple Formats**: Saves data in JSON, CSV, and DOCX formats
- **🔍 Comprehensive Logging**: Detailed logging for debugging and monitoring
- **📁 Organized Output**: Clean project structure with dedicated folders

## Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 🎯 Interactive Mode (Recommended)
```bash
python interactive_scraper.py
```
- Interactive menu with options
- URL validation and examples
- Easy to use for beginners

### 📝 Simple Input Mode
```bash
python scrape_input.py
```
- Prompts for URL input
- Validates URL format
- Quick and simple

### 🚀 Command Line Mode
```bash
python run_scraper.py "https://www.glassdoor.com/Interview/Tesla-Software-Engineer-Interview-Questions-EI_IE43129.0,5_KO6,23.htm"
```

### Advanced Usage
```bash
# Basic scraping
python code/scrape_any_link.py "https://www.glassdoor.com/Interview/Company-Position-Interview-Questions-EI_IE12345.0,5_KO6,23.htm"

# With custom output prefix
python code/scrape_any_link.py "https://www.glassdoor.com/Interview/Google-Software-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,20.htm" --output google_swe

# Generate DOCX from existing JSON
python code/generate_docx.py
```

## Output

The scraper will create **company-specific folders** for organized data storage:

### 📁 Folder Structure
```
scraped_data/
├── Tesla/                          # Company-specific folder
│   ├── interview_data_*.json      # Complete interview data
│   └── interview_questions_*.docx # Formatted Q&A document
├── Google/                         # Company-specific folder
│   ├── interview_data_*.json      # Complete interview data
│   └── interview_questions_*.docx # Formatted Q&A document
├── Microsoft/                      # Company-specific folder
│   ├── interview_data_*.json      # Complete interview data
│   └── interview_questions_*.docx # Formatted Q&A document
└── *.html                         # Raw HTML for debugging
```

### 📊 Files Generated
- **JSON Files**: Complete interview data with metadata
- **DOCX Files**: Formatted questions and answers documents
- **HTML Files**: Raw HTML for debugging (in main folder)
- **Logs**: Detailed execution logs in `logs/` folder

## DOCX Document Features

The generated DOCX files include:
- **📋 Table of Contents** - Quick navigation
- **❓ Q&A Sections** - Formatted questions and answers
- **📊 Metadata** - Difficulty, outcome, location, date
- **📈 Summary Statistics** - Interview statistics and distributions
- **🎨 Professional Formatting** - Clean, readable layout

## Supported URLs

Any Glassdoor interview URL in the format:
```
https://www.glassdoor.com/Interview/[Company]-[Position]-Interview-Questions-EI_IE[ID].[X],[Y]_KO[Z],[W].htm
```

Examples:
- Tesla Software Engineer: `https://www.glassdoor.com/Interview/Tesla-Software-Engineer-Interview-Questions-EI_IE43129.0,5_KO6,23.htm`
- Google Software Engineer: `https://www.glassdoor.com/Interview/Google-Software-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,20.htm`
- Microsoft Data Scientist: `https://www.glassdoor.com/Interview/Microsoft-Data-Scientist-Interview-Questions-EI_IE1651.0,9_KO10,24.htm`

## Dependencies

- undetected-chromedriver
- selenium
- beautifulsoup4
- requests
- pandas
- lxml
- python-docx

## Examples

### Scrape Tesla Interviews
```bash
python run_scraper.py "https://www.glassdoor.com/Interview/Tesla-Software-Engineer-Interview-Questions-EI_IE43129.0,5_KO6,23.htm"
```

### Scrape Google Interviews
```bash
python run_scraper.py "https://www.glassdoor.com/Interview/Google-Software-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,20.htm"
```

### Generate DOCX from Existing Data
```bash
python code/generate_docx.py
```

## Notes

- The scraper automatically handles Cloudflare challenges
- Data is saved in organized folders for easy access
- Comprehensive logging helps with debugging
- Respects website terms of service and implements delays
- Generated DOCX files are ready for sharing and printing


