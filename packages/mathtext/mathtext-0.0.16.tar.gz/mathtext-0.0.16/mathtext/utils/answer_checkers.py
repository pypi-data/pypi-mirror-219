"""
Symbols and keywords defined in Owen's math language:

Dictionary for translating from raw student text
(lowered and stripped) into symbols in Owen's vocabulary.
>>> dict_answer_normalized
{'yes': 'yes-no',
 'no': 'yes-no',
 't': 'true-false',
 'f': 'true-false',
 'a': 'multiple-choice',
 'b': 'multiple-choice',
 'c': 'multiple-choice',
 'd': 'multiple-choice',
 'even': 'even-odd',
 'odd': 'even-odd',
 'monday': 'day-of-the-week',
 'tuesday': 'day-of-the-week',
 'wednesday': 'day-of-the-week',
 'thursday': 'day-of-the-week',
 'friday': 'day-of-the-week',
 'saturday': 'day-of-the-week',
 'sunday': 'day-of-the-week',
 '>': '>',
 'g': '>',
 'gt': '>',
 'greater': '>',
 '<': '<',
 'l': '<',
 'lt': '<',
 'less': '<',
 '>=': '>=',
 'gte': '>=',
 '<=': '<=',
 'lte': '<=',
 '=': '=',
 'e': '=',
 'equal': '='}

Dictionary for translating from raw student text (lowered and stripped)
into an answer type category 'text', 'symbol'.
Other types will return None when looked up with dict.get():
>>> dict_answer_type
{'yes': 'text',
 'no': 'text',
 't': 'text',
 'f': 'text',
 'a': 'text',
 'b': 'text',
 'c': 'text',
 'd': 'text',
 'even': 'text',
 'odd': 'text',
 'monday': 'text',
 'tuesday': 'text',
 'wednesday': 'text',
 'thursday': 'text',
 'friday': 'text',
 'saturday': 'text',
 'sunday': 'text',
 '>': 'symbol',
 'g': 'symbol',
 'gt': 'symbol',
 'greater': 'symbol',
 '<': 'symbol',
 'l': 'symbol',
 'lt': 'symbol',
 'less': 'symbol',
 '>=': 'symbol',
 'gte': 'symbol',
 '<=': 'symbol',
 'lte': 'symbol',
 '=': 'symbol',
 'e': 'symbol',
 'equal': 'symbol'}
"""

text_type_answers = {
    'yes-no': ['yes', 'no'],
    'true-false': ['t', 'f'],
    'multiple-choice': ['a', 'b', 'c', 'd'],
    'even-odd': ['even', 'odd'],
    'day-of-the-week': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
}
dict_text_normalized = {}
for normalized_ans, possible_answers in text_type_answers.items():
    dict_text_normalized.update(
        {ans: normalized_ans for ans in possible_answers}
        )
dict_answer_type = {ans: 'text' for ans in dict_text_normalized}

symbol_type_answers = {
    '>': ['>', 'g', 'gt', 'greater'],
    '<': ['<', 'l', 'lt', 'less'],
    '>=': ['>=', 'gte'],
    '<=': ['<=', 'lte'],
    '=': ['=', 'e', 'equal'],
}
dict_symbol_normalized = {}
for normalized_ans, possible_answers in symbol_type_answers.items():
    dict_symbol_normalized.update(
        {ans: normalized_ans for ans in possible_answers}
        )
dict_answer_type.update({ans: 'symbol' for ans in dict_symbol_normalized})

dict_answer_normalized = {}
dict_answer_normalized.update(dict_text_normalized)
dict_answer_normalized.update(dict_symbol_normalized)


def check_answer_type(expected_answer):
    """ Determines if the expected answer is not a float or int

    >>> check_answer_type("2 ^ 5")
    "exponent"
    >>> check_answer_type("11: 30 PM")
    "time"
    >>> check_answer_type("T")
    "text"
    >>> check_answer_type("2")
    "other"
    """
    expected_answer = str(expected_answer).strip().lower()
    symbol_text_ans_type = dict_answer_type.get(expected_answer)
    if symbol_text_ans_type:
        return symbol_text_ans_type
    if "^" in expected_answer:
        return 'exponent'
    if "/" in expected_answer:
        return 'fraction'
    if ":" in str(expected_answer):
        return 'time'
    if "x" in str(expected_answer):
        return 'equation'

    return 'other'

