# Children's Storybook Creation App

An interactive Gradio application that helps kids create illustrated storybooks using AI.

## Features

- Kids can create personalized storybooks with their name as the author
- AI-generated book covers based on story topics
- AI-generated illustrations for each page based on kid's text
- Unlimited pages - kids decide when to finish
- Download completed books as PDF

## Setup

### Prerequisites

- Python 3.8 or higher
- Google AI API key (for gemini-2.5-flash and imagen-4.0-generate-001)

### Installation

1. Clone the repository or navigate to the project directory

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Create a `.env` file in the project directory
   - Add your Google AI API key to `.env`:
   ```
   GOOGLE_AI_API_KEY=your_actual_api_key_here
   ```
   - Note: Make sure `.env` is in your `.gitignore` (it should be by default)

### Running the App

```bash
python app.py
```

The app will start on `http://localhost:7860` (or another port if 7860 is busy).

## Usage

1. Enter your full name
2. Describe what your story is about
3. Wait for the book cover to be generated
4. Add pages one by one by typing the text for each page
5. Click "Add Another Page" to continue or "Finish Book" when done
6. View your complete book and download it as PDF

## Project Structure

```
ChildrensBook/
├── app.py              # Main Gradio application
├── cover_agent.py      # Cover creation agent
├── story_agent.py      # Story page illustration agent
├── pdf_generator.py    # PDF creation functionality
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .env.example       # Environment variables template
```

## Technical Stack

- **UI Framework**: Gradio
- **LLM**: gemini-2.5-flash (via Google Generative AI SDK)
- **Image Generation**: imagen-4.0-generate-001 (via Google Generative AI SDK)
- **PDF Generation**: reportlab

## Troubleshooting

### Image Generation Issues

If you encounter errors with image generation, the imagen API structure may differ from what's implemented. The code tries multiple approaches:
1. Using `GenerativeModel('imagen-4.0-generate-001')`
2. Using `genai.images.generate()` method

You may need to adjust the image generation code in `cover_agent.py` and `story_agent.py` based on the actual Google AI SDK API structure for imagen models.

### API Key Issues

Make sure your `.env` file is in the project root directory and contains:
```
GOOGLE_AI_API_KEY=your_actual_api_key_here
```

### Model Name Issues

If `gemini-2.5-flash` is not available, you may need to use an alternative model name like `gemini-2.0-flash-exp` or `gemini-1.5-flash`. Update the model names in `cover_agent.py` and `story_agent.py` accordingly.

