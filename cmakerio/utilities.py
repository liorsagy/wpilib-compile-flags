def until(s: str, part: str, remove: bool = False) -> str:
    if part not in s:
        return s
    return s[:s.index(part) + (0 if remove else len(part))]
