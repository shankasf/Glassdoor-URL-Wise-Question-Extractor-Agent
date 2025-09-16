# Glassdoor URL Wise Question Extractor Agent

A comprehensive web scraper designed to extract interview questions and experiences from any Glassdoor interview page, with Cloudflare bypass capabilities and automatic DOCX generation.

## Project Structure

```
glassdoor_interview_question_extractor_agent/
├── code/                           # Source code
│   ├── smart_qa_extractor.py      # Smart Q&A extraction from JSON
│   ├── docx_generator.py          # DOCX file generation
│   ├── generate_docx.py           # DOCX generation utility
│   ├── universal_interview_scraper.py # Universal scraper for any link
│   └── scrape_any_link.py         # Command-line interface
├── requirements.txt               # Python dependencies
├── interactive_scraper.py         # Interactive mode (recommended)
├── scrape_input.py                # Simple input mode
├── run_scraper.py                 # Command line mode
├── USAGE_GUIDE.md                 # Detailed usage instructions
├── COMPANY_FOLDERS.md             # Company folder structure guide
└── README.md                      # This file
```

## Features

- **🌐 Universal Scraping**: Works with any Glassdoor interview URL
- **🛡️ Cloudflare Bypass**: Uses undetected-chromedriver to bypass protection
- **📝 Smart Q&A Extraction**: Intelligently extracts questions and answers from interview experiences
- **📄 DOCX Generation**: Creates beautifully formatted Word documents
- **📊 Multiple Formats**: Saves data in JSON, CSV, and DOCX formats
- **🔍 Comprehensive Logging**: Detailed logging for debugging and monitoring
- **📁 Organized Output**: Clean project structure with company-specific folders

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

> **⚠️ Legal Notice**: Before using this tool, please read the [Legal Disclaimer](#-legal-disclaimer--important-information) section below. By using this tool, you agree to comply with all applicable laws and Glassdoor's Terms of Service.

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
- **Logs**: Detailed execution logs (automatically created during scraping)

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

## ⚠️ Legal Disclaimer & Important Information

### **Legal Considerations**

This tool is designed for **educational and personal use only**. Users must understand and comply with the following legal requirements:

#### **🔍 Legal Status**
- **Generally Legal**: For personal/educational use with publicly accessible data
- **ToS Compliance**: Users must review and comply with Glassdoor's Terms of Service
- **Jurisdiction**: Users are responsible for following applicable laws in their region
- **Professional Advice**: Always consult with a legal professional for specific legal guidance

#### **📋 User Responsibilities**
- ✅ **Personal Use Only**: Use scraped data for individual research and learning
- ✅ **Review ToS**: Read and understand Glassdoor's Terms of Service
- ✅ **Respect Privacy**: Don't collect or share personal information inappropriately
- ✅ **Rate Limiting**: Use the tool responsibly to avoid overwhelming servers
- ❌ **No Commercial Use**: Do not use for commercial purposes without proper authorization
- ❌ **No Redistribution**: Do not redistribute large datasets publicly

#### **🛡️ Built-in Legal Safeguards**
- **Public Data Only**: Only accesses publicly visible interview data
- **No Authentication Bypass**: Doesn't circumvent login requirements
- **Rate Limiting**: Implements delays between requests (2-5 seconds)
- **Educational Purpose**: Clearly designed for learning and research
- **Transparency**: Open source code for review and verification

#### **⚖️ Legal Precedents**
- **LinkedIn v. hiQ Labs**: Courts ruled scraping publicly accessible data doesn't violate CFAA
- **Fair Use Doctrine**: Educational and research purposes are generally protected
- **Public Data**: Information voluntarily shared by users on public platforms

#### **📊 Risk Assessment**
| Use Case | Risk Level | Recommendation |
|----------|------------|----------------|
| Personal Research | 🟢 Low | Generally safe with proper use |
| Educational Projects | 🟢 Low | Recommended with disclaimers |
| Commercial Use | 🔴 High | Requires legal consultation |
| Data Redistribution | 🔴 High | Not recommended |

### **🚨 Important Warnings**

1. **Terms of Service**: Glassdoor's ToS may prohibit automated data collection
2. **Data Protection Laws**: GDPR, CCPA, and other privacy laws may apply
3. **Rate Limiting**: Excessive requests may result in IP blocking
4. **Legal Changes**: Laws and ToS can change; stay informed

### **📞 Legal Resources**
- [Glassdoor Terms of Service](https://www.glassdoor.com/about/terms.htm)
- [GDPR Information](https://gdpr.eu/)
- [CCPA Information](https://oag.ca.gov/privacy/ccpa)
- [Web Scraping Legal Guide](https://www.scraperapi.com/blog/is-web-scraping-legal/)

---

## Technical Notes

- The scraper automatically handles Cloudflare challenges
- Data is saved in organized company-specific folders for easy access
- Comprehensive logging helps with debugging (logs are created automatically)
- Respects website terms of service and implements delays
- Generated DOCX files are ready for sharing and printing
- Virtual environment and logs are excluded from version control


