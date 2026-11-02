def process_text(text: str, operation: str) -> list | int:
    """process text using a supported operation"""

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if operation == "uppercase":
        return text.upper()

    if operation == "lowercase":
        return text.lower()

    if operation == "word_count":
        return len(text.split())

    raise ValueError(f"Unsupported operation: {operation}")