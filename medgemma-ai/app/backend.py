"""
MedGemma Backend API - FastAPI Server
Conecta o frontend/Java ao modelo MedGemma 1.5 Local ou Gemini Cloud

Uso:
Acessar o arquivo guia.txt 

O servidor ficará disponível em http://localhost:8000
"""

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn
import os
import shutil
from model import MedGemmaModel
import google.generativeai as genai
from PIL import Image 

ACTIVE_AI_PROVIDER = "CLOUD_GEMINI" # Mude para "LOCAL_MEDGEMMA" quando quiser usar a GPU
GOOGLE_API_KEY = "AIzaSyA4UJ3P7OlKyoKzVeZcdmNmQ5ftkjRmIjk"

app = FastAPI(title="MedGemma AI Microservice")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INICIALIZAÇÃO DO MODELO DE IA (LOCAL OU CLOUD)
ai_model = None

if ACTIVE_AI_PROVIDER == "LOCAL_MEDGEMMA":
    print("=" * 70)
    print("🖥️ MODO LOCAL: Carregando MedGemma na GPU...")
    ai_model = MedGemmaModel(use_8bit=True)
    print("✅ Modelo carregado com sucesso na GPU!")
    print("=" * 70)
else:
    print("=" * 70)
    print("🚀 MODO CLOUD: Usando Gemini 1.5 Flash")
    genai.configure(api_key=GOOGLE_API_KEY)
    print("=" * 70)

@app.get("/")
def read_root():
    return {"status": "Online", "provider": ACTIVE_AI_PROVIDER}

@app.post("/analyze")
async def analyze_case(
    patient_data: str = Form(...),
    message: Optional[str] = Form(""),
    files: List[UploadFile] = File(None)
):
    print(f"\n📥 Nova requisição recebida via {ACTIVE_AI_PROVIDER}")
    
    if not files or len(files) == 0:
        return {"analysis": "Erro: Nenhuma imagem enviada."}

    image_file = files[0]
    temp_path = f"temp_{image_file.filename}"
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(image_file.file, buffer)
        
    try:
        custom_prompt = f"Patient context: {patient_data}\nPhysician's Notes: {message}\nTask: Analyze the attached medical image."
        
        if ACTIVE_AI_PROVIDER == "CLOUD_GEMINI":
            # CHAMADA PARA O GOOGLE CLOUD
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            with Image.open(temp_path) as img:
                img.load()
                response = model.generate_content([custom_prompt, img])
                response_text = response.text
        else:
            # CHAMADA PARA A GPU LOCAL
            response_text = ai_model.analyze_image(
                image_path=temp_path,
                prompt=custom_prompt,
                max_tokens=200,
                temperature=0.7
            )
            
        print("✅ Análise concluída com sucesso!")
        return {"analysis": response_text}

    except Exception as e:
        print(f"❌ Erro detalhado: {str(e)}")
        if "404" in str(e):
            return {"analysis": "Erro: O modelo Gemini 1.5 Flash não foi encontrado. Verifique sua chave de API e região."}
        return {"analysis": f"Erro no processamento: {str(e)}"}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)