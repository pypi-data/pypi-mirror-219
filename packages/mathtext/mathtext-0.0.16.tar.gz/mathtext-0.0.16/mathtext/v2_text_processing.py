import copy
# import datetime
# import pandas as pd
# import re

from mathtext.v1_text_processing import format_int_or_float_answer
from mathtext.utils.nlutils import (
    text2time,
    text2equation,
    text2fraction,
    text2exponent
)

APPROVED_RESPONSE_CASES = [
    ['yes', 'answer', ['yes', 't']],
    ['y', 'answer', ['yes', 't']],
    ['yah', 'answer', ['yes', 't']],
    ['yeah', 'answer', ['yes',  't']],
    ['ok', 'answer', ['yes', 't']],
    ['okay', 'answer', ['yes', 't']],
    ['okey', 'answer', ['yes', 't']],
    ['yea', 'answer', ['yes', 't']],
    ['yh', 'answer', ['yes', 't']],
    ['ys', 'answer', ['yes', 't']],
    ['yrs', 'answer', ['yes', 't']],
    ['yes.', 'answer', ['yes', 't']],
    ['yep', 'answer', ['yes', 't']],
    ['yee', 'answer', ['yes', 't']],
    ['yed', 'answer', ['yes', 't']],
    ['yesh', 'answer', ['yes', 't']],
    ['yew', 'answer', ['yes', 't']],
    ['yex', 'answer', ['yes', 't']],
    ['yey', 'answer', ['yes', 't']],
    ['yez', 'answer', ['yes', 't']],
    ['ready', 'answer', ['yes']],
    ['proceed', 'answer', ['yes']],
    ['continue', 'answer', ['yes']],
    ['t', 'answer', ['yes', 't']],
    ['true', 'answer', ['yes', 't']],
    ['1', 'answer', ['yes', 't']],
    ['no', 'answer', ['no', 'f']],
    ['n', 'answer', ['no', 'f']],
    ['nah', 'answer', ['no', 'f']],
    ['f', 'answer', ['no', 'f']],
    ['false', 'answer', ['no', 'f']],
    ['0', 'answer', ['no', 'f']],
    ['even', 'answer', ['even']],
    ['odd', 'answer', ['odd']],
    ['monday', 'answer', ['monday']],
    ['tuesday', 'answer', ['tuesday']],
    ['wednesday', 'answer', ['wednesday']],
    ['thursday', 'answer', ['thursday']],
    ['friday', 'answer', ['friday']],
    ['saturday', 'answer', ['saturday']],
    ['sunday', 'answer', ['sunday']],
    ['mon', 'answer', ['monday']],
    ['tues', 'answer', ['tuesday']],
    ['wed', 'answer', ['wednesday']],
    ['thurs', 'answer', ['thursday']],
    ['fri', 'answer', ['friday']],
    ['sat', 'answer', ['saturday']],
    ['sun', 'answer', ['sunday']],
    ['>', 'answer', ['>', 'g']],
    ['g', 'answer', ['>', 'g']],
    ['gt', 'answer', ['>', 'g']],
    ['greater', 'answer', ['>', 'g']],
    ['greater than', 'answer', ['>', 'g']],
    ['<', 'answer', ['<', 'l']],
    ['l', 'answer', ['<', 'l']],
    ['lt', 'answer', ['<', 'l']],
    ['less', 'answer', ['<', 'l']],
    ['less than', 'answer', ['<', 'l']],
    ['>=', 'answer', ['>=', 'gte']],
    ['gte', 'answer', ['>=', 'gte']],
    ['greater than or equal', 'answer', ['>=', 'gte']],
    ['<=', 'answer', ['<=', 'lte']],
    ['lte', 'answer', ['<=', 'lte']],
    ['less than or equal', 'answer', ['<=', 'lte']],
    ['=', 'answer', ['=', 'e']],
    ['e', 'answer', ['=', 'e']],
    ['equal', 'answer', ['=', 'e']],
    ['same', 'answer', ['=', 'e']],
    ['a', 'answer', ['a']],
    ['b', 'answer', ['b']],
    ['c', 'answer', ['c']],
    ['d', 'answer', ['d']],
    ['easier', 'keyword', 'easier'],
    ['harder', 'keyword', 'harder'],
    ['hint', 'keyword', 'hint'],
    ['next', 'keyword', 'next'],
    ['stop', 'keyword', 'stop'],
    ['help', 'keyword', 'help'],
    ['support', 'keyword', 'support'],
    ['skip', 'keyword', 'skip'],
    ['menu', 'keyword', 'menu'],
    # These keywords below may not be very useful
    ['finish', 'keyword', 'finish'],
    ['hard', 'keyword', 'hard'],
    ['tired', 'keyword', 'tired'],
    ['tomorrow', 'keyword', 'tomorrow'],
    ['finished', 'keyword', 'finished'],
    ['exit', 'keyword', 'exit'],
    ['easy', 'keyword', 'easy'],
    ['manu', 'keyword', 'menu'],
    ['menue', 'keyword', 'menu'],
    ['meun', 'keyword', 'menu'],
    ['menus', 'keyword', 'menu'],
    ['skio', 'keyword', 'skip'],
    ['hints', 'keyword', 'hint'],
    ['hin', 'keyword', 'hint'],
    ['stp', 'keyword', 'stop'],
    ['yws', 'keyword', 'yes'],
    ['nest', 'keyword', 'next'],
    ['nex', 'keyword', 'next'],
    ['herder', 'keyword', 'harder'],
    ['hardier', 'keyword', 'harder'],
    ['easer', 'keyword', 'easier'],
    ['earier', 'keyword', 'easier'],
    ['dtop', 'keyword', 'stop'],
]

APPROVED_RESPONSES_BY_TYPE = {}
KEYWORD_LOOKUP = {}
TEXT_ANSWER_LOOKUP = {}
for entry in APPROVED_RESPONSE_CASES:
    APPROVED_RESPONSES_BY_TYPE[entry[0]] = entry[1]
    if entry[1] == 'answer':
        TEXT_ANSWER_LOOKUP[entry[0]] = entry[2]
    else:
        KEYWORD_LOOKUP[entry[0]] = entry[2]

NUMBER_MAP = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fourty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
    'hundred': 100,
    'thousand': 1000,
    'million': 1000000,
    'billion': 1000000000,
    'trillion': 1000000000000,
}

regex_evaluation_functions = {
    'text2exponent': text2exponent,
    'text2fraction': text2fraction,
    'text2time': text2time,
    'text2equation': text2equation,
}


def run_regex_evaluations(message_text, expected_answer):
    """ Calls functions that evaluate for specific answer types with regex """
    regex_functions = "text2time text2equation text2fraction text2exponent".split()
    for regex_function in regex_functions:
        eval_function = regex_evaluation_functions[regex_function]
        result = eval_function(message_text, expected_answer)
        if result != 32202 and result:
            return result


def normalize_message_and_answer(student_message, expected_answer):
    """
    >>> normalize_message_and_answer("Maybe 5000", "5,000")
    ('maybe 5000', '5000')
    >>> normalize_message_and_answer("Yeah I think so", "Yes")
    ('yeah i think so', 'yes')
    """
    normalized_student_message = str(student_message).strip().replace(',','').lower()[0:100] 
    normalized_expected_answer = str(expected_answer).strip().replace(',','').lower()
    return normalized_student_message, normalized_expected_answer


def extract_approved_response_from_phrase(
    tokenized_student_message,
    normalized_expected_answer,
    expected_answer
):
    """ Searches a message for predefined answers or keywords as well common mispellings

    >>> extract_approved_response_from_phrase(['maybe', 'y'], 'yes', 'Yes')   
    'Yes'
    >>> extract_approved_response_from_phrase(['*menu*', 'y'], 'yes', 'Yes')   
    'Yes'
    >>> extract_approved_response_from_phrase(['maybe', '5000'], '5000', '5000')   
    '5000'
    """
    answer_dict = copy.deepcopy(APPROVED_RESPONSES_BY_TYPE)
    if not answer_dict.get(normalized_expected_answer,''):
        answer_dict[normalized_expected_answer] = 'expected_answer'
    answer_types = [(answer_dict[token.replace('.', '').replace('*','')], token.replace('.', '').replace('*','')) for token in tokenized_student_message if token.replace('.', '').replace('*','') in answer_dict]

    for answer_type in answer_types:
        if answer_type[0] == 'expected_answer':
            return expected_answer
    for answer_type in answer_types:
        if answer_type[0] == 'answer' and normalized_expected_answer in TEXT_ANSWER_LOOKUP[answer_type[1]]:
            return expected_answer
    for answer_type in answer_types:
        if answer_type[0] == 'keyword':
            return KEYWORD_LOOKUP[answer_type[1]]


def is_number(normalized_student_message):
    """ Checks whether a student message can be converted to an integer or float
    >>> is_number("maybe 5000")
    False
    >>> is_number("2")
    True
    >>> is_number("2.75")
    True
    >>> is_number("-3")
    True
    """
    try:
        if float(normalized_student_message):
            return True
    except ValueError:
        pass
    try:
        if int(normalized_student_message):
            return True
    except ValueError:
        pass
    return False


def run_text_evaluations(message_text, expected_answer):
    result = ''
    normalized_student_message, normalized_expected_answer= normalize_message_and_answer(message_text, expected_answer)

    if normalized_student_message.replace(' ', '') == normalized_expected_answer.replace(' ', ''):
        return expected_answer
    
    tokenized_student_message = normalized_student_message.split()

    result = extract_approved_response_from_phrase(
        tokenized_student_message,
        normalized_expected_answer,
        expected_answer
    )
    if result:
        return result
    
    result = run_regex_evaluations(message_text, expected_answer)
    if result:
        return result

    result = format_int_or_float_answer(message_text)
    if result != 32202 and result:
        return str(result)
    
    return '32202'