"""
exceptions.py

MIT Licence

FastPDF Service/Fast Track Technologies
"""

class PDFException(Exception):
    """Exception raised for custom purpose.

    Attributes:
        response -- Response object from requests library
        message -- explanation of the error
    """

    def __init__(self, response, message="Server returned an HTTP error"):
        self.status_code = response.status_code
        self.response = response
        self.text = response.text
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}. Status Code: {self.status_code}, Response: {self.text}"
        
        
