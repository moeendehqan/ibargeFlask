import sys
if sys.version_info >= (3, 6):
    import zipfile
else:
    import zipfile36 as zipfile

import os
from PyPDF2 import PdfReader, PdfWriter



def extract_images_from_pdf(pdf_path, output_zip_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        image_counter = 0
        with zipfile.ZipFile(output_zip_path, 'w') as zip_file:
            for page_number, page in enumerate(pdf_reader.pages):
                images = page.images
                for image in images:
                    image_counter += 1
                    image_path = f'fileStorege/image{image_counter}.png'
                    
                    # Save the image
                    with open(image_path, 'wb') as image_file:
                        image_file.write(image.data)
                    
                    # Add the image to the ZIP file
                    zip_file.write(image_path)
                    
                    # Delete the temporary image file
                    os.remove(image_path)
    return image_counter