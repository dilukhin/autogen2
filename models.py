from autogen_ext.models.openai import OpenAIChatCompletionClient
import os

def make_model(model_name, temperature=0.2):
    return OpenAIChatCompletionClient(
        model=model_name,
        temperature=temperature,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),

        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
            "family": "unknown"
        }
    )

architect_model = make_model("mistralai/codestral-2508", 0.2)
builder_model = make_model("mistralai/codestral-2508", 0.1)