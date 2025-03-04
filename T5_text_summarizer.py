import fitz  
import pytesseract
import re
import urllib.request
import json
import nltk
import requests
from pdf2image import convert_from_path
from transformers import pipeline
from fuzzysearch import find_near_matches
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup

nltk.download('punkt')

def pdf_to_images(pdf_path):
    return convert_from_path(pdf_path, dpi=300)

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(pdf_path):
    pages = pdf_to_images(pdf_path)
    extracted_data = {}
    
    for idx, page in enumerate(pages):
        extracted_text = extract_text_from_image(page).strip()
        extracted_data[idx + 1] = { 
            "page_no": idx + 1,
            "page_content": extracted_text
        }
    
    return extracted_data

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    text = "\n".join([para.get_text() for para in paragraphs])
    return {1: {"page_no": 1, "page_content": text.strip()}}  

def extract_text_from_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as file:
        text = file.read()
    return {1: {"page_no": 1, "page_content": text.strip()}}  

def summarize_text_t5(text):
    summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")
    summary_output = summarizer(text, min_length=5, max_length=500, do_sample=False)
    return summary_output[0]['summary_text']

def generate_summary_json(text_data):
    """Generate JSON output containing page number, content, and summary."""
    output_json = {}
    
    for page_no, data in text_data.items():
        extracted_text = data["page_content"]
        summary = summarize_text_t5(extracted_text)
        
        output_json[page_no] = {
            "page_no": page_no,
            "page_content": extracted_text,
            "summary": summary
        }
    
    return output_json

def main():
    print("Select the input file type:")
    print("1. .txt file")
    print("2. .pdf file")
    print("3. Website URL")
    
    choice = input("Enter your choice (1/2/3): ")
    
    if choice == "1":
        file_path = input("Enter the path of the .txt file: ")
        text_data = extract_text_from_txt(file_path)
    elif choice == "2":
        file_path = input("Enter the path of the .pdf file: ")
        text_data = extract_text_from_pdf(file_path)
    elif choice == "3":
        url = input("Enter the website URL: ")
        text_data = extract_text_from_url(url)
    else:
        print("Invalid choice! Exiting.")
        return
    
    output_json = generate_summary_json(text_data)

    print(json.dumps(output_json, indent=4))

    return output_json  

if __name__ == "__main__":
    summary_result = main()
