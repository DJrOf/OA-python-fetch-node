from bs4 import BeautifulSoup
from markdownify import markdownify
import sys
sys.path.append("/Users/danielofosu/Desktop/openagents-document-retrieval")  
from src.loaders.Utils import Utils
from src.loaders.PDFLoader import PDFLoader
from io import BytesIO
import PyPDF2
import time
from pdfminer.high_level import extract_pages  # Import from pdfminer.six (for Pytohn3)

class PDFLoader(Loader):
  
  def __init__(self, runner):
    super().__init__(runner)

  def load(self, url):

    content = Utils.fetch(url, ["application/pdf"], True)

    if not content:
      return [None, None]
    
    # Open the PDF file in read binary mode
    f = BytesIO(content)
    
    # Use pdfminer.six to extract information with link handling 
    try:
      extracted_pages = list(extract_pages(f, encoding='utf-8'))
      full_text = ""
      links = []
      for page in extracted_pages:
        text_content = page.get_text()
        link_annotations = page.get_annots() 

        # Process link annotations 
        for annotation in link_annotations:
          if annotation.get_subtype() == '/Link':  # Check for link annotation type
            # Extract link details (text and url) and store them
            link_text = annotation.get('Dest') or annotation.get('ActualText')  # Explore options for link text
            link_url = annotation.get('URI') or annotation.get('A')  # Explore options for link url
            links.append({"text": link_text, "url": link_url})
        full_text += text_content.strip()

      # Integrate links into the text 
      for link in links:
        link_text = link.get("text", "")
        link_url = link.get("url", "")
        formatted_link = f"{link_text}:{link_url}"  
        full_text = full_text.replace(link_text, formatted_link)
      full_text += "\nSource: " + url + '\n\n'
      return [full_text], (time.time() + 60 * 60 * 24 * 30) * 1000
    except Exception as e:
      self.getLogger().error(f"Error processing PDF with pdfminer.six: {e}")
      return [None, None]