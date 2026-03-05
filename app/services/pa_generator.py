from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from app.services.llm_service import get_llm
import json


def generate_pa_form(clinical_note: str) -> dict:
    llm = get_llm()   #  provider-agnostic

    extract_prompt = PromptTemplate(
        input_variables=["note"],
        template="""
Extract ALL fields from the clinical note below.

Return STRICT JSON with exactly these keys (empty string "" if not found):
{{
  "diagnosis": "diagnosis with ICD-10 code e.g. Rheumatoid Arthritis - M05.9",
  "procedure": "full medication or procedure name e.g. Adalimumab (Humira) 40mg subcutaneous injection",
  "strength": "strength and route e.g. 40mg subcutaneous injection",
  "frequency": "how often e.g. every 2 weeks",
  "quantity": "quantity e.g. 2 pens per month",
  "therapy_length": "duration e.g. 12 months",
  "cpt": "CPT or HCPCS code e.g. 99214",
  "allergies": "drug allergies e.g. Penicillin (rash), Sulfa (hives)",
  "height_weight": "height and weight e.g. 5'11, 198 lbs",
  "new_prescription": "Yes or No",
  "urgency": "Standard or Urgent",
  "patient_first_name": "first name only e.g. James",
  "patient_last_name": "last name only e.g. Carter",
  "patient_dob": "date in YYYY-MM-DD format e.g. 1968-07-14",
  "patient_sex": "Male, Female, or Other",
  "patient_phone": "phone number e.g. 214-555-7832",
  "patient_email": "email address e.g. james.carter@outlook.com",
  "member_id": "insurance member ID e.g. UHC-2024-447821",
  "address": "street address only e.g. 412 Oakwood Drive, Apt 7A",
  "city": "city only e.g. Dallas",
  "state": "state abbreviation e.g. TX",
  "zip": "zip code e.g. 75201",
  "prescriber_first": "prescriber first name only e.g. Sarah",
  "prescriber_last": "prescriber last name only e.g. Mitchell",
  "npi": "NPI number e.g. 1234567890",
  "office_phone": "office phone e.g. 214-555-0100",
  "office_fax": "office fax e.g. 214-555-0101",
  "failed": "ALL failed treatments listed in full",
  "reasons": "comma-separated from ONLY these options: Adverse outcome with alternatives, Complex chronic condition, Higher dosage required, Formulary exception, Other"
}}

Clinical Note:
{note}
"""
    )

    extract_chain = RunnableSequence(extract_prompt | llm)
    extract_output = extract_chain.invoke({"note": clinical_note})

    # ── strip markdown fences if LLM wraps in ```json ... ``` ──
    raw = extract_output.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    extracted = json.loads(raw.strip())

    justification_prompt = PromptTemplate(
        input_variables=["note"],
        template="""
Write a clear, insurance-compliant medical necessity justification.
Include: primary diagnosis, why the requested medication is necessary,
what prior treatments were attempted and why they failed.
Be specific and thorough — 3 to 5 sentences.

Clinical Note:
{note}
"""
    )

    justification_chain = RunnableSequence(justification_prompt | llm)
    justification_output = justification_chain.invoke(
        {"note": clinical_note}
    )

    return {
        # ── your original 3 fields ──────────────────────────────
        "diagnosis":         extracted.get("diagnosis",        "Unknown"),
        "procedure":         extracted.get("procedure",        "Unknown"),
        "medical_necessity": justification_output.content.strip(),

        # ── new fields ──────────────────────────────────────────
        "medication":        extracted.get("procedure",        ""),   # frontend checks data.medication first
        "strength":          extracted.get("strength",         ""),
        "frequency":         extracted.get("frequency",        ""),
        "quantity":          extracted.get("quantity",         ""),
        "therapy_length":    extracted.get("therapy_length",   ""),
        "cpt":               extracted.get("cpt",              ""),
        "allergies":         extracted.get("allergies",        ""),
        "height_weight":     extracted.get("height_weight",    ""),
        "new_prescription":  extracted.get("new_prescription", ""),
        "urgency":           extracted.get("urgency",          "Standard"),
        "failed":            extracted.get("failed",           ""),
        "reasons":           extracted.get("reasons",          ""),
        "rationale":         justification_output.content.strip(),

        # ── patient info ────────────────────────────────────────
        "patient_first_name": extracted.get("patient_first_name", ""),
        "patient_last_name":  extracted.get("patient_last_name",  ""),
        "patient_dob":        extracted.get("patient_dob",        ""),
        "patient_sex":        extracted.get("patient_sex",        ""),
        "patient_phone":      extracted.get("patient_phone",      ""),
        "patient_email":      extracted.get("patient_email",      ""),
        "member_id":          extracted.get("member_id",          ""),
        "address":            extracted.get("address",            ""),
        "city":               extracted.get("city",               ""),
        "state":              extracted.get("state",              ""),
        "zip":                extracted.get("zip",                ""),

        # ── prescriber info ─────────────────────────────────────
        "prescriber_first":   extracted.get("prescriber_first",   ""),
        "prescriber_last":    extracted.get("prescriber_last",    ""),
        "npi":                extracted.get("npi",                ""),
        "office_phone":       extracted.get("office_phone",       ""),
        "office_fax":         extracted.get("office_fax",         ""),
    }