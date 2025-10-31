from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from docxtpl import DocxTemplate
from io import BytesIO
import base64
import os

app = FastAPI()

TEMPLATE_PATH = "./Full_Stack_Template.docx"

class GenerateRequest(BaseModel):
    context: dict  # Example: {"name": "Ganesh", "role": "Senior Developer"}

class GenerateResponse(BaseModel):
    filename: str
    docx_b64: str

@app.post("/generate-docx", response_model=GenerateResponse)
def generate_docx(payload: GenerateRequest):
    # Step 1: Check if template exists
    if not os.path.exists(TEMPLATE_PATH):
        raise HTTPException(status_code=404, detail="Template file not found")

    try:
        # Step 2: Load and render template
        doc = DocxTemplate(TEMPLATE_PATH)
        doc.render(payload)
        # doc.save("Ganesh_Gouru_Resume_Filled.docx")
        # Step 3: Save to in-memory stream
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        # Step 4: Encode to base64
        docx_b64 = base64.b64encode(buffer.read()).decode("utf-8")

        # Step 5: Return response
        return GenerateResponse(
            filename="Ganesh_Gouru_Resume.docx",
            docx_b64=docx_b64
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating document: {str(e)}")

@app.get("/health")
def health():
    return {"ok": True}
