import logging
import re
from unidecode import unidecode

from mathtext.utils.answer_checkers import check_answer_type
from mathtext.constants import TOKENS2INT_ERROR_INT
from mathtext.utils.nlutils import (
    text2num,
    text2time,
    text2text,
    text2exponent,
    text2fraction,
    text2symbol,
    text2equation,
    has_unicode_characters,
    unicode2str
    )
from mathtext.utils.text2int_so import text2int, text2float

log = logging.getLogger(__name__)


def check_expected_answer_validity(expected_answer):
    """ Ensures that the expected_answer is a string or returns error code """
    # TODO: Is this necessary anymore?
    # TODO: Why are there two?
    if not isinstance(expected_answer, str) or not isinstance(expected_answer, str):
        try:
            expected_answer = str(expected_answer)
        except:
            return TOKENS2INT_ERROR_INT
    return expected_answer


answer_evaluation_functions = {
    'exponent': text2exponent,
    'fraction': text2fraction,
    'text': text2text,
    'time': text2time,
    'symbol': text2symbol,
    'equation': text2equation,
}


def format_answer_to_expected_answer_type(text, expected_answer=None):
    """ 
    >>> format_answer_to_expected_answer_type("Y", "Yes")
    "Yes"
    >>> format_answer_to_expected_answer_type("yes", "T")
    "T"
    >>> format_answer_to_expected_answer_type("1 / 2", "1/2")
    """
    expected_answer = check_expected_answer_validity(expected_answer)
    answer_type = check_answer_type(expected_answer)

    has_unicode = has_unicode_characters(text)

    if has_unicode:
        text = unicode2str(text)

    if answer_type == "other":
        return TOKENS2INT_ERROR_INT

    eval_function = answer_evaluation_functions[answer_type]
    result = eval_function(text, expected_answer)
    if result != TOKENS2INT_ERROR_INT:
        return result
    return TOKENS2INT_ERROR_INT


def format_int_or_float_answer(text):
    """ Attempts to convert a student message into an int or float

    >>> format_int_or_float_answer("12")
    12
    >>> format_int_or_float_answer("maybe 0.5")
    0.5
    >>> format_int_or_float_answer("I don't know")
    32202
    >>> format_int_of_float_answer("¹1")
    32202
    """
    try:
        num = text2num(text)
        if num != TOKENS2INT_ERROR_INT:
            return num

        result = text2float(text)
        if result and result != None:
            return result

        result = text2int(text)
        if result and result != 0:
            return result
    except ValueError:
        log.exception("ValueError")
    except Exception:
        log.exception("Exception")
    return TOKENS2INT_ERROR_INT


def convert_text_to_answer_format(text, expected_answer=None):
    """ Attempts to convert a message to a text answer or float/int answer

    Used for testing in test_cases_all.py 
    """
    result = format_answer_to_expected_answer_type(text, expected_answer)
    if result != TOKENS2INT_ERROR_INT:
        return result

    return format_int_or_float_answer(text)
