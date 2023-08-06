
def is_number(n):
    """
    return True if n represents a number else False

    n is a number or a string
        
    Example:
    >>> is_number(3)
    True
    >>> is_number('5.2')
    True
    >>> is_number('Hello')
    False
    """

    try:
        float(n)
    except ValueError:
        return False
    return True

