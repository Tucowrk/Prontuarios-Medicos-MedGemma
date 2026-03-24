"""
MedGemma Backend API - Flask Server
Conecta o frontend HTML ao modelo MedGemma 1.5

Uso:
  pip install flask flask-cors pillow
  python backend.py

O servidor ficará disponível em http://localhost:5000
"""

import os
import io
import base64
import tempfile
import traceback

from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image

# ── Importar seu modelo MedGemma ──────────────────────────────────────────────
# Assumindo que medgemma_model.py está no mesmo diretório
from model import MedGemmaModel          # ← ajuste se necessário

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})   # Permite chamadas do frontend local

# ── Carregamento do modelo (uma única vez na inicialização) ───────────────────
print("Inicializando MedGemma...")
medgemma = MedGemmaModel(use_8bit=True)
print("✓ Modelo pronto. API disponível em http://localhost:5000")


# ── Utilitários ───────────────────────────────────────────────────────────────

def pil_from_request_file(file_storage):
    """Converte um FileStorage (upload Flask) em PIL Image."""
    img_bytes = file_storage.read()
    img = Image.open(io.BytesIO(img_bytes))
    if img.mode != "RGB":
        img = img.convert("RGB")
    return img


def save_pil_to_temp(pil_img, suffix=".jpg"):
    """Salva PIL Image em arquivo temporário e retorna o path."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    pil_img.save(tmp.name, format="JPEG", quality=95)
    tmp.close()
    return tmp.name


def cleanup_temp_files(*paths):
    for path in paths:
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except Exception:
            pass


# ── Endpoint principal: /analyze ──────────────────────────────────────────────

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Recebe:
      - prompt          (form field, texto)
      - patient_context (form field, texto opcional)
      - image_0 … image_N (file uploads)

    Retorna:
      { "response": "análise do modelo" }
    """
    temp_paths = []

    try:
        # ── Ler campos de texto ──────────────────────────────────────────────
        user_prompt      = request.form.get("prompt", "").strip()
        patient_context  = request.form.get("patient_context", "").strip()

        # ── Montar prompt completo ───────────────────────────────────────────
        full_prompt_parts = []

        if patient_context:
            full_prompt_parts.append(
                f"[CONTEXTO DO PACIENTE]\n{patient_context}\n"
            )

        if user_prompt:
            full_prompt_parts.append(user_prompt)
        else:
            full_prompt_parts.append(
                "Analyze this medical image and describe all relevant findings, "
                "including any abnormalities, their location, severity, and "
                "possible clinical significance. Provide differential diagnoses "
                "if applicable."
            )

        final_prompt = "\n".join(full_prompt_parts)

        # ── Coletar imagens enviadas ─────────────────────────────────────────
        image_files = []
        for key in sorted(request.files.keys()):       # image_0, image_1 …
            if key.startswith("image_"):
                image_files.append(request.files[key])

        if not image_files:
            # Sem imagem: modo texto puro
            response_text = run_text_only(final_prompt)
            return jsonify({"response": response_text})

        # ── Processar cada imagem ────────────────────────────────────────────
        # Por enquanto, análise sequencial; adapte para batch se precisar
        results = []
        for i, img_file in enumerate(image_files):
            pil_img   = pil_from_request_file(img_file)
            tmp_path  = save_pil_to_temp(pil_img)
            temp_paths.append(tmp_path)

            analysis = medgemma.analyze_image(
                image_path=tmp_path,
                prompt=final_prompt,
                max_tokens=500,
                temperature=0.2
            )

            # O modelo retorna o prompt + resposta; extrair apenas a resposta
            analysis_clean = extract_model_response(analysis, final_prompt)

            if len(image_files) > 1:
                results.append(f"**Imagem {i+1} ({img_file.filename}):**\n{analysis_clean}")
            else:
                results.append(analysis_clean)

        combined = "\n\n---\n\n".join(results)
        return jsonify({"response": combined})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

    finally:
        cleanup_temp_files(*temp_paths)


# ── Endpoint: /health ─────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    """Verificação de saúde da API."""
    import torch
    gpu_info = {}
    if torch.cuda.is_available():
        gpu_info = {
            "name":        torch.cuda.get_device_name(0),
            "vram_total":  round(torch.cuda.get_device_properties(0).total_memory / 1024**3, 2),
            "vram_used":   round(torch.cuda.memory_allocated() / 1024**3, 2),
        }
    return jsonify({
        "status":    "ok",
        "model":     medgemma.model_id,
        "quantized": medgemma.use_8bit,
        "gpu":       gpu_info or "CPU mode",
    })


# ── Helpers ───────────────────────────────────────────────────────────────────

def run_text_only(prompt: str) -> str:
    """
    Fallback para perguntas sem imagem.
    O MedGemma é multimodal; sem imagem usamos geração de texto simples.
    """
    # Aqui você pode usar o processador diretamente ou retornar aviso
    return (
        "⚕ Nenhuma imagem foi enviada. "
        "Por favor, anexe uma imagem médica para análise. "
        f"\n\n_Sua pergunta foi: '{prompt}'_"
    )


def extract_model_response(full_output: str, prompt: str) -> str:
    """
    O MedGemma (estilo Gemma) repete o prompt na saída antes da resposta.
    Esta função tenta extrair apenas a parte gerada pelo modelo.
    """
    # Estratégia 1: buscar "model\n" que indica início da resposta no template
    if "\nmodel\n" in full_output:
        return full_output.split("\nmodel\n", 1)[-1].strip()

    # Estratégia 2: remover o prompt do início se ele aparecer
    if prompt and full_output.startswith(prompt):
        return full_output[len(prompt):].strip()

    # Fallback: retornar tudo
    return full_output.strip()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=False)
    # threaded=False: evita conflitos com o modelo PyTorch em múltiplas threads
