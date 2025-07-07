from django.conf import settings

from string import ascii_letters, digits
from collections import OrderedDict

# Define the character space for short codes
# Maps index to character: {0: 'a', 1: 'b', ...}
KEY_SPACE = OrderedDict({
    y: x for y, x in enumerate(''.join([
        ascii_letters,  # a-z, A-Z
        digits,        # 0-9
        '-',           # -
        '_',           # _
    ]))
})

# Define reverse mapping for quick character lookup
# Maps character to index: {'a': 0, 'b': 1, ...}
KEY_SPACE_REVERSE = OrderedDict({x: y for y, x in KEY_SPACE.items()})


def generate_short_code(previous_short_code: str) -> str:
    """
    Generate the next short code in sequence by incrementing the previous code.
    
    This function implements a custom base-N number system where N is the size of KEY_SPACE.
    It increments the previous code by 1, handling carries similar to decimal addition.
    The result is padded to SHORTENER_MINIMAL_LENGTH with 'a' characters on the left.
    
    Examples:
        >>> generate_short_code('a')  # Returns 'b' (if SHORTENER_MINIMAL_LENGTH=0)
        >>> generate_short_code('z')  # Returns 'aa' (if SHORTENER_MINIMAL_LENGTH=2)
        >>> generate_short_code('9')  # Returns 'aa' (if SHORTENER_MINIMAL_LENGTH=2)
        >>> generate_short_code('99')  # Returns 'aaaa' (if SHORTENER_MINIMAL_LENGTH=4)
    
    Args:
        previous_short_code: The last generated short code to increment
        
    Returns:
        str: The next short code in sequence, padded to SHORTENER_MINIMAL_LENGTH
        
    Raises:
        ValueError: If the input contains characters not in KEY_SPACE
    """
    if not previous_short_code or previous_short_code == "":
        return KEY_SPACE[0] * settings.SHORTENER_MINIMAL_LENGTH

    carry = None
    position = -1
    result = ""
    
    while True:
        if carry is True:
            position -= 1

        try:
            current_char = previous_short_code[position]
        except IndexError:
            # Handle overflow by adding a new digit
            result += KEY_SPACE[0]
            break

        try:
            char_index = KEY_SPACE_REVERSE[current_char]
        except KeyError:
            raise ValueError(f"Invalid character '{current_char}' in short code")

        try:
            next_char = KEY_SPACE[char_index + 1]
            carry = False
        except KeyError:
            # Handle carry when reaching the end of KEY_SPACE
            next_char = KEY_SPACE[0]
            carry = True

        result += next_char

        if not carry:
            # No more carries needed, append remaining characters
            result += previous_short_code[:position]
            break

    # Reverse to get correct order
    result = result[::-1]

    # Pad with 'a' to reach minimal length
    minimal_length = settings.SHORTENER_MINIMAL_LENGTH
    if len(result) < minimal_length:
        result = KEY_SPACE[0] * (minimal_length - len(result)) + result
    
    return result

__all__ = ('generate_short_code',)