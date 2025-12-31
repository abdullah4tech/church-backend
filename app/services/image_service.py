from io import BytesIO
from typing import Tuple, Optional
from PIL import Image as PILImage

class ImageProcessor:
    @staticmethod
    def process_image(file_content: bytes) -> Tuple[BytesIO, int, int, str]:
        """
        Process image: validate, resize (if needed), and return metadata.
        Returns: (processed_file_io, width, height, format)
        """
        try:
            img = PILImage.open(BytesIO(file_content))
            
            # Validate format
            if img.format not in ['JPEG', 'PNG', 'WEBP']:
                raise ValueError("Unsupported image format. Use JPEG, PNG, or WEBP.")
            
            # Extract dimensions
            width, height = img.size
            
            # Optimize/Resize logic can go here (Phase 2)
            # For MVP, we just validate and return original
            
            output = BytesIO()
            img.save(output, format=img.format, optimize=True, quality=85)
            output.seek(0)
            
            return output, width, height, img.format
            
        except Exception as e:
            raise ValueError(f"Invalid image file: {e}")
