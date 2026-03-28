"""
MedGemma Backend API - Flask Server
Conecta o frontend HTML ao modelo MedGemma 1.5

Uso:
  pip install flask flask-cors pillow
  python backend.py

O servidor ficará disponível em http://localhost:5000
"""

from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Optional
import uvicorn
import os
import shutil
from model import MedGemmaModel

app = FastAPI(title="MedGemma AI Microservice")

print("⏳ Iniciando o servidor e carregando o MedGemma na GPU...")
ai_model = MedGemmaModel(use_8bit=True)

@app.get("/")
def read_root():
    return {"status": "MedGemma AI Service is Online", "model": "Loaded"}

@app.post("/analyze")
async def analyze_case(
    patient_data: str = Form(...),
    message: Optional[str] = Form(""),
    files: List[UploadFile] = File(None)
):
    print(f"\n📥 Nova requisição recebida do Java!")
    print(f"Dados do paciente: {patient_data}")
    
    custom_prompt = f"Patient context: {patient_data}. Doctor's query: {message}. Analyze this image accordingly."

    response_text = "Nenhuma imagem foi enviada para análise."

    if files and len(files) > 0 and files[0].filename:
        image_file = files[0]
        temp_path = f"temp_{image_file.filename}"
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
            
        print(f"🖼️ Imagem salva temporariamente: {temp_path}")
        
        try:
            response_text = ai_model.analyze_image(
                image_path=temp_path,
                prompt=custom_prompt,
                max_tokens=800,
                temperature=0.7
            )
        except Exception as e:
            response_text = f"Erro no processamento da IA: {str(e)}"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        print("⚠️ Nenhuma imagem recebida, respondendo apenas ao texto.")
        response_text = f"Recebi os dados do paciente, mas preciso de uma imagem de raio-x/tomografia para que o MedGemma faça a análise visual."

    return {
        "analysis": response_text
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)