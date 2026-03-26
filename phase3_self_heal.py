# phase3_self_heal.py

import subprocess
from autogen_agentchat.agents import AssistantAgent


ANALYZER_PROMPT = """
You are a code analyzer.

INPUT:
- Python code
- Error log

TASK:
- Find root cause
- Explain briefly
- Propose fix

OUTPUT:
===FIX===
<text>
"""

FIXER_PROMPT = """
You are a code fixer.

INPUT:
- Original code
- Fix instructions

TASK:
- Apply fix
- Return FULL updated code

OUTPUT:
===CODE===
```python
<code>
```

"""

def run_generated():
    result = subprocess.run(
        ["python", "generated_system.py"],
        capture_output=True,
        text=True
    )
    return result
    
def extract_fix(text: str):
    import re
    m = re.search(r"===FIX===\s*(.*)", text, re.DOTALL)
    return m.group(1).strip() if m else None

def extract_code(text: str):
    import re

    # сначала ищем python блок
    m = re.search(r"```python\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        return m.group(1)

    # fallback — любой код блок
    m = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        return m.group(1)

    return None
    
async def self_heal_loop(code, analyzer_model, fixer_model, max_attempts=3):
    analyzer = AssistantAgent(
        name="analyzer",
        model_client=analyzer_model,
        system_message=ANALYZER_PROMPT
    )

    fixer = AssistantAgent(
        name="fixer",
        model_client=fixer_model,
        system_message=FIXER_PROMPT
    )

    for attempt in range(max_attempts):
        print(f"[Phase3] Attempt {attempt+1}")

        with open("generated_system.py", "w", encoding="utf-8") as f:
            f.write(code)

        result = run_generated()

        if result.returncode == 0:
            print("[Phase3] SUCCESS")
            return code

        print(f"[Phase3] ERROR detected: returncode={result.returncode}")

        # --- Analyzer ---
        analyzer_input = f"""
CODE:
{code}

RETURN CODE:
{result.returncode}

STDOUT:
{result.stdout}

STDERR:
{result.stderr}
"""
        response = await analyzer.run(task=analyzer_input)
        fix_text = extract_fix(str(response))

        if not fix_text:
            print("[Phase3] Analyzer failed")
            print(response)
            break

        # --- Fixer ---
        fixer_input = f"""
CODE:
{code}

FIX:
{fix_text}
"""
        response = await fixer.run(task=fixer_input)
        new_code = extract_code(str(response))

        if not new_code:
            print("[Phase3] Fixer failed")
            break

        code = new_code

    print("[Phase3] FAILED after retries")
    return code
