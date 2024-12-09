from datetime import datetime

def format_date(date, format_string='%Y-%m-%d'):
    """
    Format a date object to a string.
    
    :param date: Date object to format
    :param format_string: String specifying the desired format
    :return: Formatted date string
    """
    return date.strftime(format_string)

def calculate_age(birth_date):
    """
    Calculate age based on birth date.
    
    :param birth_date: Date object representing the birth date
    :return: Age as an integer
    """
    today = datetime.now()
    age = today.year - birth_date.year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age

