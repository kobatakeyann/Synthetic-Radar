import random
import string


def generate_random_strings(letter_num) -> str:
    """
    Arg
    letter_num (int): The length of string that you'd like to generate. 
    """
    random_letters = random.choices(string.ascii_letters, k=letter_num)
    random_string = "".join(random_letters)
    return random_string

