"""
Quick test script for cover_agent
"""
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from cover_agent import create_cover

def test_cover_agent():
    """Test the cover agent with sample data"""
    print("=" * 60)
    print("Testing Cover Agent")
    print("=" * 60)
    
    # Test data
    author_name = "Emma Johnson"
    story_description = "A story about a brave little dragon who learns to fly"
    
    print(f"\nAuthor: {author_name}")
    print(f"Story Description: {story_description}")
    print("\nGenerating cover... (this may take a moment)\n")
    
    try:
        # Create cover
        result = create_cover(author_name, story_description)
        
        # Display results
        print("=" * 60)
        print("RESULTS")
        print("=" * 60)
        print(f"Title: {result.get('title')}")
        print(f"Author: {result.get('author_name')}")
        print(f"Has Image: {result.get('image') is not None}")
        
        if result.get('error'):
            print(f"\n⚠️  Warning: {result.get('error')}")
        else:
            print("\n✅ Cover generation successful!")
            
        if result.get('image'):
            print(f"Image Type: {type(result.get('image'))}")
            if hasattr(result.get('image'), 'size'):
                print(f"Image Size: {result.get('image').size}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_cover_agent()
    sys.exit(0 if success else 1)

