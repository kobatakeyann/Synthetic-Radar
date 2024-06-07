from random import choices
from string import ascii_letters

def generate_random_string(str_length:int) -> str:
    """
    Arg
    str_length (int): The length of string that you'd like to generate. 
    """
    random_strings = choices(ascii_letters, k=str_length)
    random_string = "".join(random_strings)
    return random_string

