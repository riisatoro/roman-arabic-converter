from main.constants import (
    NumberType,
    prioroty_combinations,
    roman_arabic_equivalent,
    roman_numbers,
)
from main.models import History


def save_history(raw_number, converted_number):
    """
    Save convertation history
    """
    History.objects.create(
        convert_from=raw_number,
        convert_to=converted_number,
    )


def get_number_type(raw_number: str):
    """
    Check, if number is arabic or roman.
    Raise value error if number is not roman nor arabic
    """

    if not raw_number:
        raise ValueError('Number can\'t be empty.')

    if raw_number.isdigit():
        if int(raw_number) < 1:
            raise ValueError('Can\'t convert numbers lower that 1.')
        return NumberType.ARABIC

    if set(raw_number).issubset(set(roman_numbers)):
        return NumberType.ROMAN

    raise ValueError('Number is not roman nor arabic.')


def get_closest_roman(number):
    for roman in roman_numbers:
        if roman_arabic_equivalent[roman] <= number:
            return roman, roman_arabic_equivalent[roman]
    smallest_roman = roman_numbers[-1]
    return smallest_roman, roman_arabic_equivalent[smallest_roman]


def convert_to_roman(number: int) -> str:
    """
    Convert integer from arabic to roman
    """
    roman_number = ""

    while number > 0:
        roman, value = get_closest_roman(number)
        roman_amount = number // value
        roman_number += roman * roman_amount
        number -= value * roman_amount

    return roman_number


def convert_to_arabic(number: str) -> int:
    """
    Convert roman number to arabic
    """

    arabic = 0
    number = number.upper()

    for numerals in [prioroty_combinations, roman_numbers]:
        for numeral in numerals:
            numeral_amount = len(number.split(numeral)) - 1
            arabic += roman_arabic_equivalent[numeral] * numeral_amount
            number = ''.join(number.split(numeral))

    return arabic
