import random
import string


def generate_text(length: int) -> str:
    return ''.join(random.choice(string.digits) for _ in range(length))
