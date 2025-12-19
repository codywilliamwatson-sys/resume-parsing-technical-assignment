# Resume Parsing Framework

A SOLID-principles-based framework for parsing resume files and extracting structured information using LLM-powered field extraction.

## Setup

### 1. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Set your Google Gemini API key:

```bash
export GEMINI_API_KEY='your-api-key-here'
```

Or create a `.env` file:

```
GEMINI_API_KEY=your-api-key-here
```

## Usage Examples

### Parse a PDF Resume

```python
from src.framework import ResumeParserFramework
from src.parsers import PDFParser
from src.extractors import ResumeExtractor, NameExtractor, EmailExtractor, SkillsExtractor
from src.llm import GeminiLLM

# Initialize LLM
llm = GeminiLLM()

# Create extractors
extractors = {
    'name': NameExtractor(),
    'email': EmailExtractor(),
    'skills': SkillsExtractor()
}

# Create resume extractor
resume_extractor = ResumeExtractor(extractors, llm)

# Create PDF parser
pdf_parser = PDFParser()

# Create framework
framework = ResumeParserFramework(pdf_parser, resume_extractor)

# Parse resume
resume_data = framework.parse_resume('path/to/resume.pdf')

print(f"Name: {resume_data.name}")
print(f"Email: {resume_data.email}")
print(f"Skills: {resume_data.skills}")
```

### Parse a Word Resume

```python
from src.framework import ResumeParserFramework
from src.parsers import WordParser
from src.extractors import ResumeExtractor, NameExtractor, EmailExtractor, SkillsExtractor
from src.llm import GeminiLLM

# Initialize LLM
llm = GeminiLLM()

# Create extractors
extractors = {
    'name': NameExtractor(),
    'email': EmailExtractor(),
    'skills': SkillsExtractor()
}

# Create resume extractor
resume_extractor = ResumeExtractor(extractors, llm)

# Create Word parser
word_parser = WordParser()

# Create framework
framework = ResumeParserFramework(word_parser, resume_extractor)

# Parse resume
resume_data = framework.parse_resume('path/to/resume.docx')

print(f"Name: {resume_data.name}")
print(f"Email: {resume_data.email}")
print(f"Skills: {resume_data.skills}")
```

## Examples

The `examples/` folder contains runnable example scripts that demonstrate how to use the framework:

- **`parse_pdf_resume.py`** - Example script for parsing PDF resumes
- **`parse_word_resume.py`** - Example script for parsing Word (.docx) resumes
- **`sample_resumes/`** - Sample resume files for testing

### Running Examples

You can run the examples directly:

```bash
# Parse PDF resume
python examples/parse_pdf_resume.py

# Parse Word resume
python examples/parse_word_resume.py
```

Or use the VS Code launch configurations:
- **"Run PDF Parser Example"** - Runs the PDF parsing example
- **"Run Word Parser Example"** - Runs the Word parsing example

Make sure your `GEMINI_API_KEY` environment variable is set before running the examples.

## Running Tests

Run all tests:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_parsers.py
```

Run a specific test:

```bash
pytest tests/test_parsers.py::TestPDFParser::test_parse_success
```

## Project Structure

```
src/
├── parsers/          # File parsers (PDF, Word)
├── extractors/       # Field extractors (Name, Email, Skills)
├── llm/             # LLM interfaces (Gemini)
├── models/          # Data models (ResumeData)
└── framework/       # Main framework class

tests/
├── test_models.py      # Tests for ResumeData
├── test_parsers.py     # Tests for PDFParser and WordParser
├── test_extractors.py  # Tests for field extractors
├── test_llm.py         # Tests for LLM interfaces
└── test_framework.py   # Tests for ResumeParserFramework

examples/
├── parse_pdf_resume.py      # Example script for PDF parsing
├── parse_word_resume.py     # Example script for Word parsing
└── sample_resumes/          # Sample resume files
    ├── sample_resume.pdf
    └── sample_resume.docx
```

