from PyPDF2 import PdfReader
from googletrans import Translator
import time

# Load the PDF
input_pdf_path = "/Users/izzy/pdf_translator/your_file_name.pdf"
output_text_path = "/Users/izzy/pdf_translator/your_file_name_translated.txt"

# Initialize the translator
translator = Translator()

# Function to handle retries on translation errors
def translate_with_retry(text, src_lang, dest_lang, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return translator.translate(text, src=src_lang, dest=dest_lang).text
        except Exception as e:
            print(f"Error translating, attempt {attempt + 1}: {e}")
            time.sleep(delay)  # Wait before retrying
    raise Exception("Failed to translate after multiple attempts")

# Read the original PDF
reader = PdfReader(input_pdf_path)

# Open a text file for writing the translated text
with open(output_text_path, 'w', encoding='utf-8') as text_file:

    # Translate each page to Hebrew and write to the text file
    for page_num, page in enumerate(reader.pages):
        original_text = page.extract_text()

        # If no text is found, skip the page
        if not original_text or not original_text.strip():
            print(f"No text found on page {page_num + 1}. Skipping.")
            continue

        try:
            # Clean the text to ensure no None values and remove excessive spaces
            cleaned_text = ' '.join([str(text).strip() for text in original_text.split() if text])

            # If the text is too large, you can also split it into smaller parts
            max_length = 5000  # Set a limit for max text length for translation
            text_parts = [cleaned_text[i:i + max_length] for i in range(0, len(cleaned_text), max_length)]

            translated_text = ""
            for part in text_parts:
                translated_part = translate_with_retry(part, src_lang='en', dest_lang='he')
                translated_text += translated_part

            # Write the translated text to the text file without reversing the order
            if translated_text:
                text_file.write(f"Page {page_num + 1}:\n")
                text_file.write(translated_text + "\n\n")
            else:
                print(f"Translation failed on page {page_num + 1}.")

        except Exception as e:
            print(f"Error translating page {page_num + 1}: {e}")

print("Translation complete. Saved to:", output_text_path)
