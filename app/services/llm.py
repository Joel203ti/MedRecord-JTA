import json, re
from openai import OpenAI
from app.config import settings
from app.prompts import CLINICAL_INSTRUCTIONS, ANALYSIS_PROMPT, QA_INSTRUCTIONS

def _client():
    if not settings.azure_foundry_api_key or "REEMPLAZA" in settings.azure_foundry_api_key:
        raise RuntimeError("Falta AZURE_FOUNDRY_API_KEY en el archivo .env")
    base=settings.azure_foundry_endpoint.rstrip('/')
    if base.endswith('/responses'): base=base[:-10]
    return OpenAI(base_url=base, api_key=settings.azure_foundry_api_key)

def _json(text):
    text=text.strip()
    text=re.sub(r'^```(?:json)?\s*|\s*```$','',text,flags=re.I|re.S)
    return json.loads(text)


def summarize(text):
    response=_client().responses.create(model=settings.azure_foundry_model, instructions=CLINICAL_INSTRUCTIONS, input=ANALYSIS_PROMPT.format(record=text[:100000]))
    print("========== GPT RESPONSE ==========")
    print(response.output_text)
    print("=================================")
    return _json(response.output_text)

def answer(question,text):
    response=_client().responses.create(model=settings.azure_foundry_model, instructions=QA_INSTRUCTIONS, input=f"EXPEDIENTE:\n{text[:100000]}\n\nPREGUNTA:\n{question}")
    return response.output_text
