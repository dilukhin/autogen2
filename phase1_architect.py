# phase1_architect.py

from autogen_agentchat.agents import AssistantAgent

ARCHITECT_SYSTEM_PROMPT = """
You are a system architect.

Your task:
Design a multi-agent system and produce SYSTEM SPEC in JSON.

Be flexible but practical.

Use provided model catalog.

OUTPUT FORMAT:
===SPEC===
<json>

===EXPLANATION===
<text>
"""

def create_architect_agent(model):
    return AssistantAgent(
        name="architect_agent",
        model_client=model,
        system_message=ARCHITECT_SYSTEM_PROMPT
    )


def build_architect_prompt(task, model_catalog):
    return f"""
TASK:
{task}

MODEL CATALOG:
{model_catalog}

Requirements:
- choose appropriate models
- design agents
- define tools
- include execution loop if needed
"""