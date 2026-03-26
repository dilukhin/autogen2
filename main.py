from dotenv import load_dotenv
load_dotenv()

import asyncio

from models import architect_model, builder_model
from phase0_model_selector import load_models, filter_models
from phase1_architect import create_architect_agent, build_architect_prompt
from phase2_builder import create_builder_agent, build_builder_prompt
from utils import extract_json_block
from utils import extract_code_auto

async def main():
    task = """
    Build a system to configure WireGuard VPN and troubleshoot network issues.
    """

    # Phase 0
    models = load_models("models.json")
    shortlist = filter_models(models)

    # Phase 1
    architect = create_architect_agent(architect_model)
    prompt1 = build_architect_prompt(task, shortlist)

    response1 = await architect.run(task=prompt1)
    text1 = str(response1)

    print("=== RAW PHASE 1 ===")
    print(text1)

    spec = extract_json_block(text1)

    print("=== SPEC ===")
    print(spec)

    if not spec:
        print("ERROR: SPEC not generated")
        return

    # Phase 2
    builder = create_builder_agent(builder_model)
    prompt2 = build_builder_prompt(spec)

    response2 = await builder.run(task=prompt2)
    text2 = str(response2)

    print("=== RAW PHASE 2 ===")
    print(text2)

    code = extract_code_auto(text2)

    if not code:
        print("ERROR: CODE not generated")
        return

    print("[Phase2] Code extracted and normalized")

    with open("generated_system.py", "w", encoding="utf-8") as f:
        f.write(code)


if __name__ == "__main__":
    asyncio.run(main())