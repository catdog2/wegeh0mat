def starts_with_one_of(string: str ,*teststrings : str) -> bool:
    return any([string.startswith(i) for i in teststrings])

