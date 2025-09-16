# 🏢 Company-Specific Folder Organization

## 📁 Automatic Folder Creation

The scraper now automatically creates **company-specific folders** based on the company name extracted from the URL. This ensures all data is organized and easy to find.

## 🔍 How It Works

### 1. **Company Name Extraction**
- Extracts company name from the Glassdoor URL
- Cleans and normalizes the name for folder usage
- Handles special characters and spaces

### 2. **Folder Structure**
```
scraped_data/
├── Tesla/                          # Tesla interviews
│   ├── interview_data_20250916_021104.json
│   └── interview_questions_20250916_021105.docx
├── Google/                         # Google interviews
│   ├── interview_data_20250916_021143.json
│   └── interview_questions_20250916_021143.docx
├── Microsoft/                      # Microsoft interviews
│   ├── interview_data_*.json
│   └── interview_questions_*.docx
└── *.html                         # Debug HTML files
```

## 🎯 Benefits

### ✅ **Organized Data**
- Each company has its own folder
- Easy to find specific company data
- No mixing of different companies

### ✅ **Scalable**
- Can handle unlimited companies
- Automatically creates new folders
- Maintains clean organization

### ✅ **User-Friendly**
- Clear folder structure
- Easy to navigate
- Professional organization

## 🔧 Technical Details

### **Company Name Cleaning**
- Removes special characters: `[^\w\s-]`
- Replaces spaces with underscores: `\s+` → `_`
- Handles multiple underscores: `__` → `_`
- Normalizes for folder names

### **Folder Creation**
- Automatically creates folders if they don't exist
- Uses `os.makedirs(company_folder, exist_ok=True)`
- Handles nested folder creation

### **File Naming**
- JSON: `interview_data_YYYYMMDD_HHMMSS.json`
- DOCX: `interview_questions_YYYYMMDD_HHMMSS.docx`
- HTML: `interview_page_YYYYMMDD_HHMMSS.html` (in main folder)

## 📊 Examples

### **Tesla URL**
```
https://www.glassdoor.com/Interview/Tesla-Software-Engineer-Interview-Questions-EI_IE43129.0,5_KO6,23.htm
```
**Creates**: `scraped_data/Tesla/` folder

### **Google URL**
```
https://www.glassdoor.com/Interview/Google-Software-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,20.htm
```
**Creates**: `scraped_data/Google/` folder

### **Microsoft URL**
```
https://www.glassdoor.com/Interview/Microsoft-Data-Scientist-Interview-Questions-EI_IE1651.0,9_KO10,24.htm
```
**Creates**: `scraped_data/Microsoft/` folder

## 🚀 Usage

The folder organization works automatically with all input methods:

### **Interactive Mode**
```bash
python interactive_scraper.py
```

### **Simple Input Mode**
```bash
python scrape_input.py
```

### **Command Line Mode**
```bash
python run_scraper.py "URL"
```

## 📈 Results

After scraping, you'll see:
```
✅ Success! Files generated:
   📄 DOCX: scraped_data\Tesla\interview_questions_20250916_021105.docx
   📊 JSON: scraped_data\Tesla\interview_data_20250916_021104.json
   🏢 Company: Tesla
   💼 Position: Software Engineer
   📈 Total Experiences: 83
   ❓ Q&A Pairs: 80

📁 Check the 'scraped_data' folder for your files!
```

## 🎉 Perfect Organization

Now your scraped data is perfectly organized by company, making it easy to:
- Find specific company interviews
- Compare different companies
- Manage large amounts of data
- Share specific company data
- Maintain clean project structure

---

**Happy Scraping with Perfect Organization! 🎯**
