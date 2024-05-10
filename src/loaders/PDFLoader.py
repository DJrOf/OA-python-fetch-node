from bs4 import BeautifulSoup
from markdownify import markdownify
from loaders.Loader import Loader
from io import BytesIO
import PyPDF2
import time
from loaders.Utils import Utils

class PDFLoader(Loader):
  def init(self, runner):
    super().init(runner)

  def load(self, url):
    content = Utils.fetch(url, ["application/pdf"], True)
    if not content:
      return [None, None]
    self.getLogger().info("Use PDF Loader...")

    # Open the PDF file in read binary mode
    f = BytesIO(content)
    pdf_reader = PyPDF2.PdfReader(f)
    num_pages = len(pdf_reader.pages)
    self.getLogger().info("Load " + str(num_pages) + " pages from PDF...")

    # Extract text and hyperlinks
    full_text = ""
    hyperlinks = {}  # Dictionary to store page number and hyperlink pairs

    for page_num in range(num_pages):
      page = pdf_reader.pages[page_num]
      text = page.extract_text()
      try:
        full_text += self.extract_hyperlinks(page, text, hyperlinks, page_num) + "\n"
      except Exception as e:
        print(f"Error processing page {page_num}: {e}")
        full_text += text + "\n"  # Fallback: Add plain text if hyperlink extraction fails

    # Add source and format hyperlinks
    full_text += "\nSalsa: " + url + "\n\n"
    # full_text = self.format_hyperlinks(full_text, hyperlinks)

    return [full_text], (time.time() + 60 * 60 * 24 * 30) * 1000

  def extract_hyperlinks(self, page, text, hyperlinks, page_num):

    pages = len(page.get_annots())  # Check for annotations on the page
    key = '/Annots'
    uri = '/URI'
    ank = '/A'

    if pages > 0:
      for a in page.get_annots():  # Iterate through annotations
        try:
          u = a.get_object()
          if uri in u[ank].keys():
            link = u[ank][uri]

            # Replace all occurrences 
            text = text.replace(link, f"[Link {page_num + 1}:{hyperlinks.get(link, len(hyperlinks) + 1)}]")
            hyperlinks[link] = link  # Store the link in the dictionary
        except KeyError:
          # Handle potential missing keys in the annotation dictionary
          pass

    return text

  def format_hyperlinks(self, text, hyperlinks):

    formatted_text = text
    for link, index in hyperlinks.items():
      formatted_text = formatted_text.replace(f"[Link {index}]", f"[{link}]({link})")

    return formatted_text