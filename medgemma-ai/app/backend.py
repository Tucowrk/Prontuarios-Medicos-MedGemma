"""
MedGemma Backend API - FastAPI Server
Conecta o frontend/Java ao modelo MedGemma 1.5 Local

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
ACTIVE_AI_PROVIDER = "CLOUD_GEMINI"
GOOGLE_API_KEY = "SUA_CHAVE_AQUI_DENTRO_DAS_ASPAS"

app = FastAPI(title="MedGemma Local AI Microservice")

# Libera o acesso para o Next.js (porta 3000) ou Java (porta 8080) conversarem com o Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("=" * 70)
print("🖥️ Iniciando o Servidor FastAPI e alocando o MedGemma na GPU...")
print("⚠️ ATENÇÃO: Fique de olho na aba 'Desempenho' do Gerenciador de Tarefas!")
print("=" * 70)

# Carrega o modelo na memória
ai_model = MedGemmaModel(use_8bit=True)
print("✅ Modelo carregado com sucesso na GPU! Servidor pronto.")

@app.get("/")
def read_root():
    return {"status": "MedGemma Local FastAPI is Online", "provider": "Local GPU"}

@app.post("/analyze")
async def analyze_case(
    patient_data: str = Form(...),
    message: Optional[str] = Form(""),
    files: List[UploadFile] = File(None)
):
    print("\n📥 Nova requisição recebida!")
    response_text = "Nenhuma imagem foi enviada para análise."

    if files and len(files) > 0 and files[0].filename:
        image_file = files[0]
        temp_path = f"temp_{image_file.filename}"
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
            
        print(f"🖼️ Imagem recebida. Iniciando processamento local...")
        
        try:
            custom_prompt = f"Patient context: {patient_data}\nPhysician's Notes: {message}\nTask: Analyze the attached medical image."
            
            # Chama a IA local (model.py)
            response_text = ai_model.analyze_image(
                image_path=temp_path,
                prompt=custom_prompt,
                max_tokens=100,
                temperature=0.7
            )
            print("✅ Análise concluída!")
            
        except Exception as e:
            response_text = f"Erro no processamento da IA Local: {str(e)}"
            print(f"❌ {response_text}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        response_text = "Erro: O assistente visual requer uma imagem médica para análise."

    return {"analysis": response_text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)