# import regex
import re
import unicodedata
import datetime


def remove_accents(input_str) -> str:
    """
    Function normalizes string with NFKD form and encodes w. ASCII encoding

    returns: encoded string
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')

    return only_ascii


def normalizeText(string: str) -> str:
    """
    Function removes unwanted symbols from text

    returns: clean text(string)
    """
    
    encoding = "utf-8"

    # lover input text
    lowerString = string.lower()

    # remove all punctuation except words and space
    noPuncString = re.sub(r'[^\w\s]', '', lowerString)

    # remove white spaces
    noWspaceString = noPuncString.strip()

    # finally remove all nonalpha. characters
    finalString = re.sub(r'[\W_]+', '', noWspaceString)

    # accents remover
    finalString = remove_accents(finalString)

    cleanText = finalString.decode(encoding)

    return cleanText


def constructtimestamp():
    return "{:%Y%m%d%H%M%S}.csv".format(datetime.datetime.now())
