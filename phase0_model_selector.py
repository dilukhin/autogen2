# phase0_model_selector.py

import json

def load_models(path="models.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["data"]

def filter_models(models):
    result = []

    for m in models:
        id = m.get("id")
        if not id:
            continue
        arch = m.get("architecture") or {}
        modality = arch.get("modality")

        if not modality:
            continue

        # Примеры: "modality": "text-\u003etext", "modality": "text+image-\u003etext", "modality": "text+audio-\u003etext+audio", 
        # "modality": "text+image+file-\u003etext", "modality": "text+image+file+audio+video-\u003etext",
        # нормализуем
        modality = modality.replace("\\u003e", ">")

        # делим на input и output
        parts = modality.split("->")

        if len(parts) != 2:
            continue

        input_mod, output_mod = parts

        # нас интересует только output = text
        if "text" not in output_mod:
            continue
    
        context = m.get("context_length", 0)

        if context < 32000:
            continue

        pricing = m.get("pricing") or {}

        price_prompt = pricing.get("prompt")
        price_completion = pricing.get("completion")

        # если нет цены — ставим большую (чтобы отфильтровать)
        if price_prompt is None:
            price_prompt = 999

        if price_completion is None:
            price_completion = 999
    
        if price_prompt == 999:
            continue

        result.append({
            "id": m["id"],
            "description": m.get("description", "")[:200],
            "context": m.get("context_length", 0),
            "price_prompt": price_prompt,
            "price_completion": price_completion
        })

    # сортировка по цене + контексту
    result = sorted(result, key=lambda x: (x["price_prompt"], -x["context"]))

    return result[:15]  # топ-15