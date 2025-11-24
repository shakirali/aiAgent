"""
Cover Agent - Generates book cover title and illustration
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the API key
api_key = os.getenv("GOOGLE_AI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Initialize the model for text generation
text_model = genai.GenerativeModel('gemini-2.5-flash')


def generate_book_title(story_description: str) -> str:
    """
    Generate a book title from the story description using gemini-2.5-flash
    
    Args:
        story_description: What the story is about
        
    Returns:
        Generated book title
    """
    prompt = f"""Based on the following story description, generate a creative and engaging book title for a children's storybook.
    The title should be:
    - Short and memorable (3-8 words)
    - Appropriate for children
    - Captivating and fun
    - Directly related to the story

    Story description: {story_description}

    Generate only the title, nothing else:"""

    try:
        response = text_model.generate_content(prompt)
        title = response.text.strip()
        # Clean up the title (remove quotes if present)
        title = title.strip('"').strip("'")
        return title
    except Exception as e:
        print(f"Error generating title: {e}")
        # Fallback: use first few words of description
        words = story_description.split()[:5]
        return " ".join(words).title()


def generate_cover_image_prompt(title: str, story_description: str) -> str:
    """
    Generate an image prompt for the cover illustration using gemini-2.5-flash
    
    Args:
        title: Book title
        story_description: What the story is about
        
    Returns:
        Image generation prompt
    """
    prompt = f"""Create a detailed image generation prompt for a children's book cover illustration.

Book Title: {title}
Story Description: {story_description}

The prompt should:
- Be suitable for a children's book cover
- Be colorful, vibrant, and engaging
- Include the main character or theme
- Be appropriate for children
- Be detailed enough for high-quality illustration

Generate only the image prompt, nothing else:"""

    try:
        response = text_model.generate_content(prompt)
        image_prompt = response.text.strip()
        return image_prompt
    except Exception as e:
        print(f"Error generating image prompt: {e}")
        # Fallback prompt
        return f"A colorful, vibrant children's book cover illustration for '{title}'. {story_description}. Bright colors, friendly characters, suitable for children."


def generate_cover_image(title: str, story_description: str):
    """
    Generate cover illustration using gemini-2.5-flash-image
    
    Args:
        title: Book title
        story_description: What the story is about
        
    Returns:
        PIL Image object
        
    Raises:
        Exception: If image generation fails due to authentication or API issues
    """
    from PIL import Image
    import io
    
    # Generate image prompt
    image_prompt = generate_cover_image_prompt(title, story_description)
    
    try:
        # Use gemini-2.5-flash-image which supports generateContent
        image_model = genai.GenerativeModel('models/gemini-2.5-flash-image')
        response = image_model.generate_content(image_prompt)
            
        # Handle different response formats
        if hasattr(response, 'images') and response.images:
            return response.images[0]
        elif hasattr(response, 'image'):
            return response.image
        elif hasattr(response, 'parts'):
            # Check if response has image parts
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data.mime_type.startswith('image'):
                    return Image.open(io.BytesIO(part.inline_data.data))
    except Exception as e:
        print(f"Error generating cover image: {e}")
        raise Exception(f"Failed to generate cover image: {e}")


def create_cover(author_name: str, story_description: str) -> dict:
    """
    Main function to create book cover
    
    Args:
        author_name: Kid's full name
        story_description: What the story is about
        
    Returns:
        Dictionary with title, author_name, and image (PIL Image or None)
    """
    # Generate title
    title = generate_book_title(story_description)
    
    # Generate cover image
    try:
        image = generate_cover_image(title, story_description)
        return {
            "title": title,
            "author_name": author_name,
            "image": image
        }
    except Exception as e:
        print(f"Error in create_cover: {e}")
        # Return cover data without image for now
        return {
            "title": title,
            "author_name": author_name,
            "image": None,
            "error": str(e)
        }
