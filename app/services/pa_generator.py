from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from app.services.llm_service import get_llm
import json


def generate_pa_form(clinical_note: str) -> dict:
    llm = get_llm()   #  provider-agnostic

    extract_prompt = PromptTemplate(
        input_variables=["note"],
        template="""
Extract diagnosis and requested procedure from the note below.

Return STRICT JSON:
{{
  "diagnosis": "...",
  "procedure": "..."
}}

Clinical Note:
{note}
"""
    )

    extract_chain = RunnableSequence(extract_prompt | llm)
    extract_output = extract_chain.invoke({"note": clinical_note})

    extracted = json.loads(extract_output.content)

    justification_prompt = PromptTemplate(
        input_variables=["note"],
        template="""
Write a clear, insurance-compliant medical necessity justification.

Clinical Note:
{note}
"""
    )

    justification_chain = RunnableSequence(justification_prompt | llm)
    justification_output = justification_chain.invoke(
        {"note": clinical_note}
    )

    return {
        "diagnosis": extracted.get("diagnosis", "Unknown"),
        "procedure": extracted.get("procedure", "Unknown"),
        "medical_necessity": justification_output.content.strip()
    }
