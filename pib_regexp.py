#!/usr/bin/env python3

import re

PERSON_NAME_RE = re.compile(
    r'''
    (?P<family_name>[\w\-\'ʼ]+)
    \s+
    (?P<maiden_name>\([\w\-\'ʼ]*\)\s+)?
    (?P<given_name>[Є-ЯҐ][\w\-\'ʼ]*(\s[а-їґ][\w\-\'ʼ]+)?)
    (\s+)?
    (?P<middle_name>[Є-ЯҐ][\w\-\'ʼ\s]*)?
    ''',
    re.VERBOSE)

BASIC_REPLACEMENTS = {
    "\u00A0": " ",  # " " U+00A0 NO-BREAK SPACE
    "  ": " ",
    "'": "ʼ",  # U+0027 APOSTROPHE
    "’": "ʼ",  # U+2019 RIGHT SINGLE QUOTATION MARK
    "`": "ʼ",  # U+0060 GRAVE ACCENT
    "‘": "ʼ",  # U+2018 LEFT SINGLE QUOTATION MARK
    " ҆": "ʼ",  # U+0486 COMBINING CYRILLIC PSILI PNEUMATA
    "ʹ": "ʼ",  # U+02B9 MODIFIER LETTER PRIME
    "՚": "ʼ",  # U+055A ARMENIAN APOSTROPHE
    "＇": "ʼ",  # U+FF07 FULLWIDTH APOSTROPHE
    "ꞌ": "ʼ",  # U+A78C LATIN SMALL LETTER SALTILLO
    "–": "-",
    "—": "-",
    "\u200B": "",  # "" U+200B ZERO WIDTH SPACE
    "\uFEFF": "",  # U+FEFF ZERO WIDTH NO-BREAK SPACE
    "\u200E": "",  # LEFT-TO-RIGHT MARK
    "“": "\"",
    "”": "\"",
    "\u0301": "",  # COMBINING ACUTE ACCENT
}

REPLACEMENTS_UK = BASIC_REPLACEMENTS.copy()
REPLACEMENTS_UK.update({
    "I": "І",
    "O": "О",
    "i": "і",
    "o": "о",
    "C": "С",
    "c": "с",
    "M": "М",
    "«": "\"",
    "»": "\"",
})

BASIC_REPLACEMENTS = dict(
    (re.escape(k), v) for k, v in BASIC_REPLACEMENTS.items())
BASIC_REPLACEMENTS_PATTERN = re.compile("|".join(BASIC_REPLACEMENTS.keys()))

REPLACEMENTS_UK = dict(
    (re.escape(k), v) for k, v in REPLACEMENTS_UK.items())
REPLACEMENTS_UK_PATTERN = re.compile("|".join(REPLACEMENTS_UK.keys()))

def match_name_parts(full_name):
    sre = PERSON_NAME_RE.match(full_name)
    if not sre:
        print("Некоректне імʼя {}".format(full_name))
    return sre.groupdict()

def standard_name_cleaner(name, return_dict=False):
        name = UkFieldsMixin.clean_uk_field(name)\
            .replace(',', '')\
            .replace('.', ' ')\
            .replace('"', 'ʼ')\
            .replace('0', 'О')\
            .replace('1', 'І')\
            .replace('3', 'З')\
            .replace('!', 'І')\
            .strip()
        name = FOP_RE.sub('', name)
        name = MULTISPACED_RE.sub(' ', name)
        name_parts = match_name_parts(name)
        if return_dict:
            return name_parts
        return " ".join(filter(None, (
            name_parts['family_name'],
            name_parts['given_name'],
            name_parts['middle_name'])))\
            .strip()

def clean_field(value):
    if value:
        value = REPLACEMENTS_UK_PATTERN.sub(
            lambda m:
                REPLACEMENTS_UK[re.escape(m.group(0))], value)
        return value.strip()
    return value
