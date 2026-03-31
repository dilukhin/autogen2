import re
import ast

def extract_json_block(text: str):
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    return None
    
def extract_code_block(text: str):
    match = re.search(r"```python\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    return None
    
def try_unescape(code: str) -> str:
    """
    Safely unescape string if it's a Python-escaped string.
    """

    if not code:
        return code

    # если выглядит как экранированная строка
    if "\\n" in code or "\\t" in code or "\\\\" in code:
        try:
            # Пробуем decode unicode escape
            return code.encode('utf-8').decode('unicode_escape')
        except Exception:
            pass

    return code
    