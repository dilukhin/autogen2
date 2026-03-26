# phase1_5_validator.py

import json

REQUIRED_KEYS = ["agents", "tools"]

ALLOWED_TOOLS = {
    "run_shell",
    "write_file",
    "read_file",
    "http_request"
}


def validate_spec(spec: dict, model_catalog: list):
    errors = []

    # --- структура ---
    for key in REQUIRED_KEYS:
        if key not in spec:
            errors.append(f"Missing key: {key}")

    # --- модели ---
    valid_models = {m["id"] for m in model_catalog}

    for agent in spec.get("agents", []):
        model = agent.get("model")
        if model not in valid_models:
            errors.append(f"Invalid model: {model}")

    # --- tools ---
    for tool in spec.get("tools", []):
        name = tool.get("name")
        if name not in ALLOWED_TOOLS:
            errors.append(f"Invalid tool: {name}")

    return errors


def try_parse_spec(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None