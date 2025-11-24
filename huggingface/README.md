# Hugging Face Learning Projects

Minimal learning projects that demonstrate different Hugging Face capabilities.

## Projects

### 1. Contact Finder (`contact_finder.py`)

Extracts contact information from websites using NER (Named Entity Recognition).

**Features:**
- Fetches website content
- Uses Hugging Face NER model to identify entities
- Extracts email addresses and phone numbers using regex
- Simple and educational code structure

**Usage:**
```bash
python contact_finder.py
```

**How It Works:**
1. Fetches website HTML content using `requests`
2. Extracts plain text from HTML
3. Uses Hugging Face's `dslim/bert-base-NER` model to identify named entities
4. Uses regex patterns to find email addresses and phone numbers

### 2. Text Generator (`text_generator.py`)

Generates text based on a query using Hugging Face's text generation models.

**Features:**
- Accepts user input prompts
- Uses Hugging Face text generation pipeline
- Generates text continuations based on the prompt
- Simple and educational code structure

**Usage:**
```bash
python text_generator.py
```

**How It Works:**
1. Loads a text generation model (default: `gpt2`)
2. Takes a user prompt as input
3. Uses Hugging Face's text generation pipeline to generate text continuation
4. Displays the generated text

## Setup

1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Learning Points

- Using Hugging Face transformers pipeline
- Named Entity Recognition (NER)
- Text generation with language models
- Web scraping basics
- Text processing with regex

