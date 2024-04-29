

def sanitize_string(string: str) -> str:
    s1 = string.strip().replace(" ", "-")
    return ''.join(e for e in s1 if e.isalnum() or (e in ['.', '-', '_']))
