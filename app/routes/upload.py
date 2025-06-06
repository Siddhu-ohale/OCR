
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
from app.services.ocr_service import extract_raw_text
from app.services.gemini_service import ask_gemini_to_parse
import logging

router = APIRouter()
UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = UPLOAD_DIR / file.filename
        contents = await file.read()
        with open(file_location, "wb") as f:
            f.write(contents)

        logging.info(f"Uploaded file: {file.filename}")
        raw_text = extract_raw_text(file_location)
        structured_data = ask_gemini_to_parse(raw_text)
        return JSONResponse(content={"Information": structured_data})

    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})
