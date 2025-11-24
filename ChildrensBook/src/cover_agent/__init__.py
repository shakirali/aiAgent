"""
Cover Agent package
"""
from .agent import (
    generate_book_title,
    generate_cover_image_prompt,
    generate_cover_image,
    create_cover
)

__all__ = [
    'generate_book_title',
    'generate_cover_image_prompt',
    'generate_cover_image',
    'create_cover'
]
