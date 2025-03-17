import json, re
from langchain_sambanova import ChatSambaNovaCloud
from database import roles_collection
from typing import Dict, Optional
from dotenv import load_dotenv
import os

load_dotenv()

# Inisialisasi model

sambanova_api_key = os.getenv("SAMBANOVA_API_KEY")
llm = ChatSambaNovaCloud(model="Qwen2.5-72B-Instruct",
                          sambanova_api_key=sambanova_api_key,
                          max_tokens=1024)

def match_cv_to_roles(cv_text: str) -> Optional[Dict[str, any]]:
    """Matching CV dengan role menggunakan LLM."""

    # Ambil semua role dari database
    roles = list(roles_collection.find({}, {"_id": 0}))

    if not roles:
        return None  # Jika tidak ada role di database

    # Format role untuk prompt
    roles_prompt = json.dumps(roles, indent=2)

    # Prompt untuk LLM
    prompt = f"""
    Berikut adalah daftar role yang tersedia:
    ```json
    {roles_prompt}
    ```

    CV kandidat berikut:
    ---
    {cv_text}
    ---

    Tentukan nama kandidat dari CV, lalu tentukan role yang paling cocok untuk kandidat ini berdasarkan pengalaman dan skill yang ada.

    Hasil harus dalam format JSON berikut tanpa tambahan teks lain:
    ```json
    {{
      "name": "NAMA_KANDIDAT",
      "matched_roles": [
        {{
          "role": "ROLE_1",
          "score": SCORE_1,
          "justification": "ALASAN_1"
        }},
        {{
          "role": "ROLE_2",
          "score": SCORE_2,
          "justification": "ALASAN_2"
        }}
      ]
    }}
    ```

    Jika tidak ada role yang cocok, buat `matched_roles` menjadi array kosong `[]` seperti ini:
    ```json
    {{
      "name": "NAMA_KANDIDAT",
      "matched_roles": []
    }}
    ```
    """

    # Dapatkan hasil dari LLM
    response = llm.invoke(prompt)
    result = response.content if hasattr(response, "content") else str(response)

    # Ekstrak hanya bagian JSON dari output LLM
    json_match = re.search(r"\{.*\}", result, re.DOTALL)
    if json_match:
        result = json_match.group(0)  # Ambil hanya bagian JSON
    else:
        return {"error": "No valid JSON found"}

    # Parsing hasil menjadi JSON
    try:
        parsed_result = json.loads(result)
        return parsed_result
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format from LLM"}