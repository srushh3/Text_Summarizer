
A Text Summarizer condenses long pieces of text into shorter, more meaningful summaries while retaining key information. It helps in extracting essential details from articles, documents, or web content efficiently.

🔹 Types of Text Summarization

Extractive Summarization – Selects the most important sentences from the original text (BERT-based).
eg: BERT Summarization (Extractive Approach)

Abstractive Summarization – Generates new sentences by paraphrasing the original text (T5-based).
eg: T5 Summarization (Abstractive Approach)

🔹 Project Explanation

1. Handles multiple input types: Extracts text from .txt, .pdf, and website URLs.
2. Uses pdf2image & pytesseract: Converts PDFs into images and extracts text using OCR. Output is stored in JSON format.
3. Pretrained T5 model and Bert Model: Uses T5 Transformer (t5-base) for abstractive summarization (paraphrasing & rewording) and BERT Extractive Summarizer selects the most important sentences instead of paraphrasing.
4. Fuzzy Matching (find_near_matches): Finds approximate matches of summary sentences in the original text.


Work Flow (T5 model)
1. Takes Input
2. Converts PDF to images and extacts text from them using pytesseract. Output is stored in JSON format (i.e page no and page content form)
3. Content from each page is summarized using T5 approach and saved in JSON format in .json file

Work Flow (Bert Model)
1. Takes Input
2. Converts PDF to images and extracts text from them using pytesseract. 
3. The OCR output is summarized using BERT model.
4. The summary is highlighted in the OCR text and saved in a document









