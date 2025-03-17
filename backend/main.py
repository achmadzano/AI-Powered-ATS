from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from database import roles_collection, cv_collection
from models import Role, CVUpload
import shutil
import os
from cv_extractor import extract_text
from matcher import match_cv_to_roles
from bson import ObjectId


app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Endpoint untuk menambahkan role
@app.post("/roles")
def add_role(role: Role):
    if roles_collection.find_one({"role": role.role}):
        raise HTTPException(status_code=400, detail="Role already exists")
    
    roles_collection.insert_one(role.dict())
    return {"message": "Role added successfully"}

# Endpoint untuk mendapatkan semua role
@app.get("/roles")
def get_roles():
    roles = list(roles_collection.find({}, {"_id": 0}))
    return roles

# Endpoint untuk mengupload CV
@app.post("/upload_cv_file")
def upload_cv_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Simpan file ke server
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Ekstraksi teks
    extracted_text = extract_text(file_path)

    if not extracted_text:
        raise HTTPException(status_code=400, detail="Failed to extract text from CV")

    # Simpan ke MongoDB dengan nama, teks, dan filename
    cv_data = {
        "filename": file.filename,
        "text": extracted_text
    }
    result = cv_collection.insert_one(cv_data)

    return {
        "message": "CV uploaded and extracted successfully",
        "cv_id": str(result.inserted_id),
        "text": extracted_text[:500]  # Biar ga kepanjangan di response
    }


@app.post("/match_cv/{cv_id}")
def match_cv(cv_id: str):
    """Matching CV yang sudah di-upload dengan role di database."""
    
    # Ambil CV dari database
    cv = cv_collection.find_one({"_id": ObjectId(cv_id)})
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")

    # Matching dengan LLM
    result = match_cv_to_roles(cv["text"])

    if not result:
        return {"message": "No roles found in the database"}

    return result

