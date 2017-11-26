import re

def validate_email(email):
    """
    Validate user email
    """
    if len(email) > 7:
        if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                    email) is not None:
            return True
    return False

def validate_text(text):
    """
    Make sure the user does not submit empty strings

    """
    stripped_value = str(text).strip()
    if len(stripped_value) == 0:
        return False
    return True