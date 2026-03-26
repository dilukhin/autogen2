# phase2_builder.py

from autogen_agentchat.agents import AssistantAgent

BUILDER_SYSTEM_PROMPT = """
You are a system builder.

Your task:
Convert SYSTEM SPEC into runnable Python AutoGen system.

STRICT RULES:
- follow SPEC exactly
- generate full code
- include:
  - models
  - tools
  - agents
  - team
  - main()
CRITICAL OUTPUT RULES:
- Output raw Python code
- DO NOT escape symbols: newlines (\n), backslashes (\\) etc.
- DO NOT wrap code in JSON strings
- Use real line breaks
- Output ONLY a markdown block:

OUTPUT FORMAT:

===CODE===
<python code>
"""

def create_builder_agent(model):
    return AssistantAgent(
        name="builder_agent",
        model_client=model,
        system_message=BUILDER_SYSTEM_PROMPT
    )


def build_builder_prompt(spec):
    return f"""
SYSTEM SPEC:
{spec}

Generate full Python implementation.
"""