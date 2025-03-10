from PIL import Image
from io import BytesIO

def validate_png(file_bytes):
    try:
        with Image.open(BytesIO(file_bytes)) as image:
            if image.format != 'PNG':
                return False, "Uploaded file is not a valid PNG image."
        return True, None
    except Exception as e:
        return False, f"Error processing image: {str(e)}"