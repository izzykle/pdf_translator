from PyPDF2 import PdfReader
from fpdf import FPDF
from googletrans import Translator
from bidi.algorithm import get_display  # Import to handle bidirectional text

# Load the PDF
input_pdf_path = "/Users/izzy/pdf_translator/your_file_name.pdf"
output_pdf_path = "/Users/izzy/pdf_translator/your_file_name_translated.pdf"

# Initialize the translator
translator = Translator()

# Read the original PDF
reader = PdfReader(input_pdf_path)

# Create a PDF writer to write the translated text
pdf_writer = FPDF()

# Add a font that supports Unicode (you'll need to download and store this font locally)
pdf_writer.add_font("DejaVu", "", "/Users/izzy/pdf_translator/fonts/dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf", uni=True)
pdf_writer.set_font("DejaVu", size=12)

# Translate each page to Hebrew and add to the new PDF
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
            translated_part = translator.translate(part, src='en', dest='he').text
            translated_text += translated_part

        # Reverse the direction of the Hebrew text using the bidi algorithm
        translated_text_rtl = get_display(translated_text)

        # Check if translation was successful and add to PDF, with right alignment
        if translated_text_rtl:
            pdf_writer.add_page()
            pdf_writer.set_auto_page_break(auto=True, margin=15)
            pdf_writer.multi_cell(0, 10, translated_text_rtl, align='R')  # Align text to the right
        else:
            print(f"Translation failed on page {page_num + 1}.")

    except Exception as e:
        print(f"Error translating page {page_num + 1}: {e}")

# Save the translated PDF
pdf_writer.output(output_pdf_path, 'F')

print("Translation complete. Saved to:", output_pdf_path)
