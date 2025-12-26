import uuid

PA_STORE = {}

def save_pa(data: dict) -> str:
    pa_id = str(uuid.uuid4())
    PA_STORE[pa_id] = data
    return pa_id

def update_pa(pa_id: str, data: dict):
    PA_STORE[pa_id] = data

def get_pa(pa_id: str):
    return PA_STORE.get(pa_id)