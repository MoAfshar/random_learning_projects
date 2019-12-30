import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
from tqdm import tqdm
from functools import lru_cache
import re
from nltk.corpus import stopwords

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

@lru_cache(maxsize=None)
def pdfparser(data):
	'''
	input: Path of data file(s)
	output: Text file of all the content of pdf
	'''
	fp = open(data, 'rb')
	rsrcmgr = PDFResourceManager()
	retstr = io.StringIO()
	codec = 'utf-8'
	laparams = LAParams()
	device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
	# Create a PDF interpreter object
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	# Process each page contained in the document
	for page in PDFPage.get_pages(fp):
		interpreter.process_page(page)
		data =  retstr.getvalue()

	return data

def clean_text(text):
    """
        text: a string
        
        return: modified initial string
    """
    text = text.lower() # lowercase text
    text = text.strip() # remove trailing and leading whitespace
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
    text = BAD_SYMBOLS_RE.sub('', text) # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing. 
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # remove stopwords from text
    text = text.split('<0x0c>') # split by paragraphs
    return text

if __name__ == '__main__':
    content = pdfparser("Annual_Report.pdf")
    clean_content = clean_text(content)
    print(clean_content)
	