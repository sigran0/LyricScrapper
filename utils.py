
import re


def extract_numbers(str):
    return re.findall(r'\d+', str)