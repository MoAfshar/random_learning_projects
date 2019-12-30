import re
import textract
import string
from nltk.corpus import stopwords
import tika

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    """
        text: a string

        return: modified initial string
    """
    text = text.lower() # lowercase text
    #text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
    #text = BAD_SYMBOLS_RE.sub('', text) # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing.
    text = re.sub(r'\d+', ' ', text) # remove all numbers
    text = text.translate(text.maketrans('','', string.punctuation)) #remove all punctuations
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # remove stopwords from text
    return text

if __name__ == '__main__':
    text = textract.process(r'C:\Users\945970\Desktop\PDF_to_Text\Annual_Report.pdf')
    text = text.decode('utf-8')
    text = clean_text(text)
    print(text)
    print(type(text))
