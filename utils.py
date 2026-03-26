import re
import json
import ast


def extract_code_auto(text: str) -> str:
    """
    Extract and normalize Python code from LLM output.
    Handles:
    - markdown blocks
    - JSON-encoded code
    - escaped one-line strings
    """

    if not text:
        return None

    # -------------------------
    # 1. ```python block
    # -------------------------
    m = re.search(r"```python\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()

    # -------------------------
    # 2. ``` any code block
    # -------------------------
    m = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()

    # -------------------------
    # 3. Try JSON
    # -------------------------
    try:
        data = json.loads(text)

        if isinstance(data, dict):
            for key in ["code", "python", "content"]:
                if key in data and isinstance(data[key], str):
                    return normalize_escaped(data[key])

    except Exception:
        pass

    # -------------------------
    # 4. Escaped string (one-liner)
    # -------------------------
    if "\\n" in text or "\\t" in text:
        return normalize_escaped(text)

    # -------------------------
    # 5. Fallback (as-is)
    # -------------------------
    return text.strip()


def normalize_escaped(code: str) -> str:
    """
    Safely unescape Python code string.
    """

    if not code:
        return code

    # если уже нормальный код — не трогаем
    if "\n" in code and not "\\n" in code:
        return code

    # попытка корректного decode через AST
    try:
        return ast.literal_eval(f'"""{code}"""')
    except Exception:
        pass

    # fallback (минимальный)
    code = code.replace("\\n", "\n")
    code = code.replace("\\t", "\t")

    return code
    
def extract_json_block(text: str):
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    return None
    
