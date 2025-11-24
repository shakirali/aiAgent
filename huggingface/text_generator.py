"""
Simple Hugging Face project to generate text based on a query.
This is a minimal example for learning purposes.
"""

from transformers import pipeline


def generate_text(prompt, model_name="gpt2", max_length=100, num_return_sequences=1):
    """
    Generate text based on a prompt using Hugging Face text generation model.
    
    Args:
        prompt: The input text/prompt to generate from
        model_name: The Hugging Face model to use (default: "gpt2")
        max_length: Maximum length of generated text (default: 100)
        num_return_sequences: Number of sequences to generate (default: 1)
    
    Returns:
        List of generated text sequences
    """
    # Load the text generation pipeline
    print(f"Loading model: {model_name}...")
    generator = pipeline("text-generation", model=model_name)
    
    # Generate text
    print(f"Generating text from prompt: '{prompt}'...\n")
    results = generator(
        prompt,
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        truncation=True
    )
    
    return results


def display_results(results):
    """Display the generated text results."""
    print("=== Generated Text ===\n")
    
    for i, result in enumerate(results, 1):
        generated_text = result['generated_text']
        print(f"Option {i}:")
        print(f"{generated_text}\n")


def main():
    """Main function to run text generation."""
    print("Hugging Face Text Generator")
    print("=" * 40)
    print()
    
    # Get user input
    prompt = input("Enter your prompt (or press Enter for default): ").strip()
    
    if not prompt:
        prompt = "The future of artificial intelligence"
        print(f"Using default prompt: '{prompt}'\n")
    
    # Generate text
    try:
        results = generate_text(prompt, max_length=150, num_return_sequences=1)
        display_results(results)
    except Exception as e:
        print(f"Error generating text: {e}")
        print("\nNote: The model will be downloaded on first use.")


if __name__ == "__main__":
    main()

