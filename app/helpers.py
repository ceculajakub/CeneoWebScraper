def extract(source, selector, attribute=None):
    try:
        if attribute:
            if isinstance(attribute, str): # typeof(attribute) == typeof(string) C#
                return source.select(selector).pop(0)[attribute].strip()
            else:
                return [item.get_text().strip() for item in source.select(selector)]
        else:
            return source.select(selector).pop(0).get_text().strip()
    except IndexError: #Out of range e.g
        return None