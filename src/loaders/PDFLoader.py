from bs4 import BeautifulSoup
from markdownify import markdownify
from loaders.Loader import Loader
from io import BytesIO
import PyPDF2
import time
from loaders.Utils import Utils

class PDFLoader(Loader):
  def __init__(self, runner):
    super().__init__(runner)

  def load(self, url):
    content = Utils.fetch(url, ["application/pdf"], True)
    if not content:
      return [None, None]
    self.getLogger().info("Use PDF Loader...")

    # Open the PDF file in read binary mode
    f = BytesIO(content)
    pdf_reader = PyPDF2.PdfReader(f)
    num_pages = len(pdf_reader.pages)
    self.getLogger().info(f"Load {num_pages} pages from PDF...")

    # Iterate through all pages and extract text & links
    fullText = ""
    extracted_links = []
    for page_num in range(num_pages):
      page = pdf_reader.pages[page_num]
      text = page.extract_text()
      fullText += text.strip()

      # Extract links from current page
      self.extract_links(page, extracted_links)

    fullText += "\n"

    # Prepare link information for output
    link_info = ""
    if extracted_links:
      link_info = "\n**External Links:**\n"
      for link in extracted_links:
        link_info += f"- {link}\n"

    # Combine text and link information
    fullText += link_info + f"\nSource: {url}\n\n"
    return [fullText], (time.time() + 60 * 60 * 24 * 30) * 1000

  def extract_links(self, page, extracted_links):
    pages = len(pdf_reader.pages)
    key = '/Annots'
    uri = '/URI'
    ank = '/A'

    pageSliced = page.get_object()
    if key in pageSliced.keys():
      ann = pageSliced[key]
      for a in ann:
        u = a.get_object()
        if uri in u[ank].keys():
          extracted_links.append(u[ank][uri])