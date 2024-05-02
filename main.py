import tabula
import os
import fitz
import PyPDF2
import re
import csv

def extract_tables(pdf_path, output_csv):
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i, table in enumerate(tables):
            table.to_csv(f"table_{i+1}.csv")

def extract_images(pdf_path, output_folder):
    pdf_file = fitz.open(pdf_path)
    for page_num in range(len(pdf_file)):
        page = pdf_file.load_page(page_num)
        images = page.get_images()
        for i, img in enumerate(images):
            base_image = pdf_file.extract_image(img[0])
            image_bytes = base_image['image']
            image_ext = base_image['ext']
            image_name = f"page_{page_num+1}_image_{i+1}.{image_ext}"
            with open(os.path.join(output_folder, image_name), 'wb') as image_file:
                image_file.write(image_bytes)

def extract_links_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        links = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            links.extend(urls)
    return links

if __name__ == "__main__":
    pdf_path = "2023_1Q_Interim_Report.pdf"
    output_folder = "images_output"
    output_csv = "tables_output.csv"

    # Extract images
    os.makedirs(output_folder, exist_ok=True)
    extract_images(pdf_path, output_folder)
    print("Images extracted successfully.")

    # Extract tables
    extract_tables(pdf_path, output_csv)
    print("Tables extracted successfully and saved as CSV.")

    # Extract links
    extracted_links = extract_links_from_pdf(pdf_path)
    print("Links extracted successfully:")
    for link in extracted_links:
        print(link)
