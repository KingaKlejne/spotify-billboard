import re


# Input from user
def get_input() -> str:
    date_input = input(
        "Which year do you want to travel to? "
        "Type the date in this format YYYY-MM-DD: ")
    return date_input


# Check if input has correct format
def check_date(date_input: str):
    regex = r'(?:1958|1959|19[6-9][0-9]|20[01][0-9]|2022)' \
            r'-(?:0[1-9]|1[012])-(?:0[1-9]|[12][0-9]|3[01])'
    date_match = re.compile(regex).match
    return date_match(date_input) is not None
