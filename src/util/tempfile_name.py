import random
import string

def generate_random_string(str_length:int) -> str:
    """
    Arg
    str_length (int): The length of string that you'd like to generate. 
    """
    random_strings = random.choices(string.ascii_letters, k=str_length)
    random_string = "".join(random_strings)
    return random_string

