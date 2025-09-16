# 🚀 Glassdoor Interview Scraper - Usage Guide

## 📋 Quick Start

Choose the method that works best for you:

### 🎯 Method 1: Interactive Mode (Recommended for Beginners)
```bash
python interactive_scraper.py
```
**Features:**
- Interactive menu with options
- URL validation and examples
- Easy to use interface
- Shows example URLs
- Handles errors gracefully

### 📝 Method 2: Simple Input Mode
```bash
python scrape_input.py
```
**Features:**
- Prompts for URL input
- Validates URL format
- Quick and simple
- Perfect for one-time use

### 🚀 Method 3: Command Line Mode
```bash
python run_scraper.py "https://www.glassdoor.com/Interview/Tesla-Software-Engineer-Interview-Questions-EI_IE43129.0,5_KO6,23.htm"
```
**Features:**
- Direct URL input
- No prompts needed
- Great for automation
- Perfect for scripts

## 📚 Example URLs

Here are some example URLs you can try:

### 🏢 Tesla
```
https://www.glassdoor.com/Interview/Tesla-Software-Engineer-Interview-Questions-EI_IE43129.0,5_KO6,23.htm
```

### 🔍 Google
```
https://www.glassdoor.com/Interview/Google-Software-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,20.htm
```

### 🏢 Microsoft
```
https://www.glassdoor.com/Interview/Microsoft-Data-Scientist-Interview-Questions-EI_IE1651.0,9_KO10,24.htm
```

### 🛒 Amazon
```
https://www.glassdoor.com/Interview/Amazon-Software-Engineer-Interview-Questions-EI_IE6036.0,6_KO7,20.htm
```

### 🍎 Apple
```
https://www.glassdoor.com/Interview/Apple-Software-Engineer-Interview-Questions-EI_IE1136046.0,5_KO6,23.htm
```

## 📁 Output Files

After scraping, you'll get:

### 📄 DOCX File
- **Location**: `scraped_data/`
- **Format**: `Company_Position_interviews_YYYYMMDD_HHMMSS.docx`
- **Content**: Formatted questions and answers
- **Features**: Table of contents, metadata, statistics

### 📊 JSON File
- **Location**: `scraped_data/`
- **Format**: `interview_data_YYYYMMDD_HHMMSS.json`
- **Content**: Raw interview data
- **Features**: Complete interview experiences, metadata

### 🌐 HTML File
- **Location**: `scraped_data/`
- **Format**: `interview_page_YYYYMMDD_HHMMSS.html`
- **Content**: Raw HTML for debugging
- **Features**: Complete page source

## 🔧 Troubleshooting

### Common Issues:

1. **Invalid URL Error**
   - Make sure it's a Glassdoor interview URL
   - Check the URL format
   - Ensure it contains "Interview" and "Questions"

2. **Chrome Driver Issues**
   - The scraper automatically downloads Chrome driver
   - Make sure you have Chrome browser installed
   - Check internet connection

3. **Cloudflare Blocking**
   - The scraper automatically handles Cloudflare
   - Wait for the "Challenge page detected" message
   - Don't interrupt the process

4. **No Questions Found**
   - Some pages may have limited content
   - Try a different company/position
   - Check the HTML file for debugging

## 📈 What You Get

### 📊 Statistics
- Total interview experiences
- Number of Q&A pairs extracted
- Company and position information
- Difficulty and outcome distributions

### 📝 Content
- Interview questions
- Detailed answers
- Interview experiences
- Metadata (date, location, outcome, difficulty)

### 🎨 Formatting
- Professional DOCX layout
- Table of contents
- Organized sections
- Easy to read and share

## 🚀 Advanced Usage

### Custom Output Prefix
```bash
python code/scrape_any_link.py "URL" --output custom_name
```

### Generate DOCX from Existing JSON
```bash
python code/generate_docx.py
```

### Batch Processing
```bash
# Create a batch script for multiple URLs
echo "URL1" | python scrape_input.py
echo "URL2" | python scrape_input.py
```

## 💡 Tips

1. **Use Interactive Mode** for the best experience
2. **Check the logs** if something goes wrong
3. **Wait for completion** - don't interrupt the process
4. **Try different URLs** if one doesn't work
5. **Check the scraped_data folder** for your files

## 🆘 Support

If you encounter issues:
1. Check the logs in the `logs/` folder
2. Verify your URL format
3. Ensure you have Chrome browser installed
4. Check your internet connection
5. Try a different URL

---

**Happy Scraping! 🎉**
