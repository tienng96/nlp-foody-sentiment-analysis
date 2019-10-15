import re
from pyvi import ViTokenizer

def remove_newline(text):
#     remove \n, \t , \b, \r \None
    text = re.sub('\n', ' ', text)
    text = re.sub('\t', ' ', text)
    text = re.sub('\b', ' ', text)
    text = re.sub('\r', ' ', text)
    return text

def clean_text(text):
    text = re.sub("(?s)<ref>.+?</ref>", "", text) # remove reference links
    text = re.sub("(?s)<[^>]+>", "", text) # remove html tags
    text = re.sub("&[a-z]+;", "", text) # remove html entities
    text = re.sub("#[a-z]+;", "", text) # remove hash tags
    text = re.sub("(?s){{.+?}}", "", text) # remove markup tags
    text = re.sub("(?s){.+?}", "", text) # remove markup tags
    text = re.sub("[']{5}", "", text) # remove italic+bold symbols
    text = re.sub("[']{3}", "", text) # remove bold symbols
    text = re.sub("[']{2}", "", text) # remove italic symbols
    text = re.sub("[ ]{2,}", " ", text) # Squeeze spaces.
    return text

def remove_symbol(text):
#     remove symbol
    text = re.sub('\"', ' ', text)
    text = re.sub('\'', ' ', text)
    text = re.sub(r'\.', ' ', text)
    text = re.sub(',', ' ', text)
    text = re.sub(r'\?', ' ', text)
    text = re.sub(':', ' ', text)
    text = re.sub('!', ' ', text)
    text = re.sub(r'\(', ' ', text)
    text = re.sub(r'\)', ' ', text)
    text = re.sub(r'\*', ' ', text)
    text = re.sub(r'\+', ' ', text)
    text = re.sub(r'\-', ' ', text)
    text = re.sub('\"', ' ', text)
    text = re.sub('/', ' ', text)
    text = re.sub('“', ' ', text)
    text = re.sub('”', ' ', text)
    text = re.sub('"', ' ', text)
    return text

def remove_number(text):
    """
    numbers are not toxic
    """
    return re.sub('([0-9]+[^\s]*)', '', text)

def preprocess(content):
    content =  remove_newline(content)
    content  = content.lower()
    content  = remove_symbol(content)
    content  = remove_number(content)
    content  = clean_text(content)
    return content
