##########################################################
# Anki AI Toolkit - PDF to QA Class
# (c)pschuelpen.tec
#
# www.tec.pschuelpen.com/anki_ai_toolkit/
#
# Create Q&A Pairs
#
# Optimized for:
# Python3 - Running on any computer - Docker
#
##########################################################
# Import Libraries
##########################################################


from openai import OpenAI
import re
import os
import PyPDF2
from pytesseract import pytesseract
from PIL import Image
from pdf2image import convert_from_path


#####################################
#            Class Def. 
#####################################

#pytesseract.tesseract_cmd = "/usr/bin/tesseract"

class PDFToQA:
    def __init__(self, api_key=None, search_api_key=None, search_engine_id=None):
        """
        Initialize the PDFToQA class.
        :param api_key: OpenAI API key. If not provided, will look for 'OPENAI_API_KEY' in environment variables.
        :param search_api_key: Search engine API key for web search functionality.
        :param search_engine_id: Search engine ID for web search functionality (e.g., Google Custom Search ID).
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set in the environment variable 'OPENAI_API_KEY'.")
        
        self.client_openai = OpenAI(
            # This is the default and can be omitted
            api_key=self.api_key
        )

        self.search_api_key = search_api_key or os.getenv('SEARCH_API_KEY')
        self.search_engine_id = search_engine_id or os.getenv('SEARCH_ENGINE_ID')

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a PDF file, including OCR for image-based PDFs.
        :param pdf_path: Path to the PDF file.
        :return: Extracted text as a single string.
        """
        text = ""

        print(f"[Info] Reading Text")
        # Try to read text-based PDF
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"[Error] Error reading PDF as text: {e}")

        print(f"[Info] Using OCR - Extracting Text now")
        # Use OCR if text extraction failed or is insufficient
        if not text.strip():
            try:
                images = convert_from_path(pdf_path)
                for image in images:
                    text += pytesseract.image_to_string(image)
            except Exception as e:
                print(f"[Error] Error performing OCR on PDF: {e}")

        # Strip Text and Create Debug Message
        txt = text.strip()
        print(f"[Info] Text Extracted - {len(txt)} chars")

        return txt

    def perform_web_search(self, query):
        """
        Perform a web search using an external API to verify or enhance QA generation.
        :param query: Search query.
        :return: List of search results.
        """
        if not self.search_api_key or not self.search_engine_id:
            print("[Error] Web search functionality is not configured.")
            return []

        import requests

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.search_api_key,
            "cx": self.search_engine_id,
            "q": query,
        }

        try:
            response = requests.get(url, params=params)
            results = response.json().get("items", [])
            return [item["snippet"] for item in results]
        except Exception as e:
            print(f"[Error] Error performing web search: {e}")
            return []

    def generate_qa_pairs(self, text, max_pairs=10, use_web_search=False):
        """
        Generate question-answer pairs from the given text using OpenAI API.
        :param text: The input text to process.
        :param max_pairs: Maximum number of QA pairs to generate.
        :param use_web_search: Whether to enhance QA generation with web search.
        :return: List of (question, answer) tuples.
        """
        print("[Info] Generating Q&A Pairs using OpenAI ChatGPT")

        prompt = (
            f"Extrahiere maximal {max_pairs} Frage Antwort Paare vom folgenden Text. Stelle Sicher, dass Formeln auch inkludiert sind "
            f"in MathJax Format im folgenden Syntax umschlossen \\( ... \\):\n\n"
            f"{text}\n\n"
            "Output Format:\n- Q: [frage]\n  A: [antwort]\n"
        )

        try:
            if use_web_search:
                search_results = self.perform_web_search("key topics from the text")
                additional_context = "\n".join(search_results)
                prompt += f"\n\nAdditionally, consider the following web search results:\n\n{additional_context}\n"

            response = self.client_openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Du bist ein Assitent, der Fragen Antwort Paare für Karteikarten erstellt."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1500,
            )
            output = response.choices[0].message.content

            print("[Info] Q&A Pairs Generated - Returning now ...")

            qa_pairs = []

            # Use regex to find each question-answer pair
            pairs = re.findall(r"- Q: (.*?)\n  A: (.*?)\n", output)

            # Add pairs to the list
            qa_pairs = [(q.strip(), a.strip()) for q, a in pairs]
            return qa_pairs
        except Exception as e:
            print(f"[Error] Error generating QA pairs: {e}")
            return []

    def process_pdf_to_qa(self, pdf_path, max_pairs=10, use_web_search=False):
        """
        Extract text from a PDF and generate QA pairs.
        :param pdf_path: Path to the PDF file.
        :param max_pairs: Maximum number of QA pairs to generate.
        :param use_web_search: Whether to enhance QA generation with web search.
        :return: List of (question, answer) tuples.
        """
        text = self.extract_text_from_pdf(pdf_path)
        return self.generate_qa_pairs(text, max_pairs, use_web_search)



#####################################
#          Example Usage 
#####################################

if __name__ == "__main__":
    api_key = "your_openai_api_key_here"  # Replace with your OpenAI API key
    search_api_key = "your_search_api_key_here"  # Replace with your search API key (if using web search)
    search_engine_id = "your_search_engine_id_here"  # Replace with your search engine ID (if using web search)
    pdf_path = "example.pdf"  # Replace with your PDF file path

    generator = PDFToQA(api_key, search_api_key, search_engine_id)
    qa_pairs = generator.process_pdf_to_qa(pdf_path, max_pairs=5, use_web_search=True)

    for i, (question, answer) in enumerate(qa_pairs, start=1):
        print(f"{i}. Q: {question}\n   A: {answer}\n")
