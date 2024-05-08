import unittest
import sys
sys.path.append("/Users/danielofosu/Desktop/openagents-document-retrieval")  
from src.loaders.PDFLoader import PDFLoader
import io  # For creating a BytesIO object

class TestPDFLoader(unittest.TestCase):

    def test_load_success(self):
        # Replace with a valid PDF URL
        url = "https://example.com/test.pdf"
        content = Utils.fetch(url, ["application/pdf"], True)  # Mock Utils.fetch
        f = io.BytesIO(content)

        loader = PDFLoader(None)  # Assuming no runner needed for unit testing
        full_text, next_update = loader.load(f)

        self.assertIsNotNone(full_text)
        self.assertIn("Source: " + url, full_text)  # Check for source URL inclusion

    def test_load_error(self):
        # Simulate an invalid URL
        url = "invalid_url"
        loader = PDFLoader(None)
        full_text, next_update = loader.load(url)

        self.assertIsNone(full_text)
        # ... (add assertions for expected error logging)

    # Add more test cases for link handling, etc.

if __name__ == "__main__":
    unittest.main()