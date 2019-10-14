import re
import unicodedata
import uuid
import random

def random_time_sleep(level):
    if level == 0:
        return random.uniform(0.5, 1)
    if level == 1:
        return random.uniform(1, 2)
    if level >= 2:
        return random.uniform(2, 3)

def gen_uuid_list(len):
    uuid_list = []
    for i in range(len):
        uuid_list.append(uuid.uuid4())
    return uuid_list

def convert_to_nosymbol(text, instead_space='_'):
    """
    Convert from 'Tieng Viet co dau' thanh 'Tieng Viet khong dau'
    text: input string to be converted
    Return: string converted
    """

    patterns = {
        '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
        '[đ]': 'd',
        '[èéẻẽẹêềếểễệ]': 'e',
        '[ìíỉĩị]': 'i',
        '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
        '[ùúủũụưừứửữự]': 'u',
        '[ỳýỷỹỵ]': 'y',
        '[ ]': instead_space
    }

    text = unicodedata.normalize('NFC', text)
    raw_words = text.split()
    normalized_words = []

    for raw_word in raw_words:
        try:
            normalized_words += re.findall('[^\W]+', raw_word)
        except:
            pass
    text = ' '.join(normalized_words)

    output = text.replace('.', '').replace(',', '').strip()
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output.lower()