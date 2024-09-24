from PyPDF2 import PdfReader
from googletrans import Translator
import time

# Load the PDF
input_pdf_path = "/Users/izzy/pdf_translator/your_file_name.pdf"
output_html_path = "/Users/izzy/pdf_translator/your_file_name_translated.html"

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

# Open an HTML file for writing the translated text
with open(output_html_path, 'w', encoding='utf-8') as html_file:
    # Write the basic HTML structure
    html_file.write("<html><head><meta charset='UTF-8'></head><body style='direction: rtl; text-align: right;'>\n")

    # Translate each page to Hebrew and write to the HTML file
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

            # Write the translated text to the HTML file with right alignment
            if translated_text:
                html_file.write(f"<h3>Page {page_num + 1}</h3>\n")
                html_file.write(f"<p>{translated_text}</p>\n")
            else:
                print(f"Translation failed on page {page_num + 1}.")

        except Exception as e:
            print(f"Error translating page {page_num + 1}: {e}")

    # Close the HTML structure
    html_file.write("</body></html>")

print("Translation complete. Saved to:", output_html_path)
