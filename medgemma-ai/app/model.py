"""
MedGemma 1.5 - 8-bit Quantization com Suporte a Imagens
Modelo médico para análise de imagens (X-rays, CT scans, etc)

Requisitos:
- VRAM: ~4-5 GB
- Python 3.8+
- CUDA compatível
"""

import os
import torch
from transformers import AutoProcessor, BitsAndBytesConfig, Gemma3ForConditionalGeneration
from PIL import Image
import warnings
warnings.filterwarnings('ignore')


class MedGemmaModel:
    """Classe para gerenciar o modelo MedGemma com quantização 8-bit"""
    
    def __init__(self, model_id="google/medgemma-1.5-4b-it", use_8bit=True):
        """
        Inicializa o modelo MedGemma
        
        Args:
            model_id: ID do modelo no HuggingFace
            use_8bit: Se True, usa quantização 8-bit (economiza memória)
        """
        self.model_id = model_id
        self.use_8bit = use_8bit
        self.token = os.getenv("HF_TOKEN")
        self.processor = None
        self.model = None
        
        # Verificar ambiente
        self._check_environment()
        
        # Carregar modelo
        self._load_model()
    
    def _check_environment(self):
        """Verifica se o ambiente está configurado corretamente"""
        print("=" * 70)
        print("VERIFICANDO AMBIENTE")
        print("=" * 70)
        
        # Verificar CUDA
        if not torch.cuda.is_available():
            print("⚠️  AVISO: CUDA não disponível. O modelo rodará na CPU (muito lento)")
            print("    Considere usar um ambiente com GPU")
        else:
            gpu_name = torch.cuda.get_device_name(0)
            vram_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"✓ GPU detectada: {gpu_name}")
            print(f"✓ VRAM disponível: {vram_gb:.2f} GB")
            
            if vram_gb < 4:
                print(f"⚠️  AVISO: VRAM baixa ({vram_gb:.1f} GB). Recomendado: 4+ GB")
        
        # Verificar token
        if not self.token:
            print("⚠️  AVISO: HF_TOKEN não encontrado no ambiente")
            print("    Configure com: export HF_TOKEN='seu_token_aqui'")
            print("    Ou: os.environ['HF_TOKEN'] = 'seu_token_aqui'")
        else:
            print("✓ Token HuggingFace detectado")
        
        print()
    
    def _load_model(self):
        """Carrega o processador e o modelo"""
        print("=" * 70)
        print("CARREGANDO MODELO")
        print("=" * 70)
        
        # Carregar processador
        print("Carregando processador...")
        try:
            self.processor = AutoProcessor.from_pretrained(
                self.model_id, 
                token=self.token
            )
            print("✓ Processador carregado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao carregar processador: {e}")
            raise
        
        # Configurar quantização
        if self.use_8bit:
            print("\nConfigurando quantização 8-bit...")
            bnb_config = BitsAndBytesConfig(
                load_in_8bit=True,
                llm_int8_threshold=6.0,
                llm_int8_has_fp16_weight=False,
                llm_int8_enable_fp32_cpu_offload=True
            )
            print("✓ Configuração 8-bit criada")
        else:
            bnb_config = None
            print("\nCarregando sem quantização (FP16)...")
        
        # Carregar modelo
        print(f"\nCarregando modelo {self.model_id}...")
        print("(Isso pode levar alguns minutos...)")
        
        try:
            # Tentativa 1: Com device_map="auto"
            if bnb_config is not None:
                self.model = Gemma3ForConditionalGeneration.from_pretrained(
                    self.model_id,
                    quantization_config=bnb_config,
                    device_map="auto",
                    token=self.token,
                    low_cpu_mem_usage=True
                )
            else:
                self.model = Gemma3ForConditionalGeneration.from_pretrained(
                    self.model_id,
                    device_map="auto",
                    token=self.token,
                    low_cpu_mem_usage=True
                )
            
            print("✓ Modelo carregado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro com device_map='auto': {e}")
            print("\nTentando método alternativo...")
            
            try:
                # Tentativa 2: Sem device_map
                if bnb_config is not None:
                    self.model = Gemma3ForConditionalGeneration.from_pretrained(
                        self.model_id,
                        quantization_config=bnb_config,
                        token=self.token,
                        low_cpu_mem_usage=True
                    )
                else:
                    self.model = Gemma3ForConditionalGeneration.from_pretrained(
                        self.model_id,
                        token=self.token,
                        low_cpu_mem_usage=True
                    )
                
                # Mover para GPU manualmente
                if torch.cuda.is_available() and bnb_config is None:
                    self.model = self.model.to("cuda")
                
                print("✓ Modelo carregado com método alternativo!")
                
            except Exception as e2:
                print(f"❌ Erro fatal ao carregar modelo: {e2}")
                print("\nSoluções:")
                print("1. Atualize as bibliotecas: pip install --upgrade transformers accelerate bitsandbytes")
                print("2. Verifique se tem VRAM suficiente (4+ GB recomendado)")
                print("3. Tente sem quantização: use_8bit=False")
                raise
        
        # Mostrar uso de memória
        if torch.cuda.is_available():
            memory_used = torch.cuda.memory_allocated() / 1024**3
            print(f"✓ Memória GPU utilizada: {memory_used:.2f} GB")
        
        print()
    
    def analyze_image(self, image_path, prompt=None, max_tokens=1000, temperature=0.7):
        """
        Analisa uma imagem médica
        
        Args:
            image_path: Caminho para a imagem
            prompt: Prompt customizado (opcional)
            max_tokens: Número máximo de tokens na resposta
            temperature: Criatividade da resposta (0.0 a 1.0)
        
        Returns:
            str: Análise do modelo
        """
        print("=" * 70)
        print("ANALISANDO IMAGEM")
        print("=" * 70)
        
        # Carregar imagem
        print(f"Carregando imagem: {image_path}")
        try:
            image = Image.open(image_path)
            print(f"✓ Imagem carregada: {image.size} pixels")
            
            # Converter para RGB se necessário
            if image.mode != 'RGB':
                image = image.convert('RGB')
                print(f"✓ Imagem convertida para RGB")
        
        except Exception as e:
            print(f"❌ Erro ao carregar imagem: {e}")
            raise
        
        # Preparar prompt
        if prompt is None:
            prompt = "Analyze this chest X-ray and describe any findings, abnormalities, or conditions you observe."
        
        print(f"\nPrompt: {prompt}")
        
        # Criar mensagens no formato correto
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        # Processar inputs
        print("\nProcessando inputs...")
        prompt_text = self.processor.apply_chat_template(
            messages, 
            add_generation_prompt=True, 
            tokenize=False
        )
        
        inputs = self.processor(
            text=prompt_text, 
            images=[image], 
            return_tensors="pt"
        )
        
        # Mover para GPU
        if torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}
        
        # Gerar resposta
        print("Gerando resposta...")
        print(f"(Aguarde ~30-60 segundos...)\n")
        
        try:
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    top_p=0.9,
                    repetition_penalty=1.1
                )
            
            # Decodificar resposta
            response = self.processor.decode(outputs[0], skip_special_tokens=True)
            
            print("✓ Análise concluída!")
            print()
            
            return response
        
        except Exception as e:
            print(f"❌ Erro durante geração: {e}")
            
            if "out of memory" in str(e).lower():
                print("\n💡 Dica: GPU sem memória. Tente:")
                print("   - Reduzir max_tokens")
                print("   - Limpar cache: torch.cuda.empty_cache()")
                print("   - Usar imagem menor")
            
            raise
    
    def batch_analyze(self, image_paths, prompt=None, max_tokens=800):
        """
        Analisa múltiplas imagens em lote
        
        Args:
            image_paths: Lista de caminhos de imagens
            prompt: Prompt customizado (opcional)
            max_tokens: Número máximo de tokens por resposta
        
        Returns:
            list: Lista de análises
        """
        results = []
        
        print(f"\n{'=' * 70}")
        print(f"ANÁLISE EM LOTE: {len(image_paths)} imagens")
        print(f"{'=' * 70}\n")
        
        for i, img_path in enumerate(image_paths, 1):
            print(f"\n>>> Imagem {i}/{len(image_paths)}: {os.path.basename(img_path)}")
            
            try:
                # Limpar cache de GPU antes de cada imagem
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                result = self.analyze_image(
                    img_path, 
                    prompt=prompt, 
                    max_tokens=max_tokens
                )
                results.append({
                    'image': img_path,
                    'analysis': result,
                    'success': True
                })
            
            except Exception as e:
                print(f"❌ Erro ao processar {img_path}: {e}")
                results.append({
                    'image': img_path,
                    'analysis': None,
                    'success': False,
                    'error': str(e)
                })
        
        return results


def main():
    """Função principal com exemplos de uso"""
    
    # =========================================================================
    # CONFIGURAÇÃO
    # =========================================================================
    
    # Configurar token (escolha uma opção):
    # Opção 1: Variável de ambiente
    # export HF_TOKEN="seu_token_aqui"
    
    # Opção 2: Diretamente no código (NÃO RECOMENDADO para produção)
    # os.environ['HF_TOKEN'] = "seu_token_aqui"
    
    # =========================================================================
    # INICIALIZAR MODELO
    # =========================================================================
    
    print("\n🏥 MedGemma 1.5 - Análise de Imagens Médicas\n")
    
    # Criar modelo com quantização 8-bit
    model = MedGemmaModel(use_8bit=True)
    
    # =========================================================================
    # EXEMPLO 1: ANÁLISE ÚNICA
    # =========================================================================
    
    # Caminho da sua imagem
    image_path = "C:/Users/User/Desktop/Projeto MED/Imagens teste/Tuberculose2.jpg"
    
    # Analisar
    response = model.analyze_image(
        image_path=image_path,
        prompt="Analyze this chest X-ray and describe any findings, abnormalities, or conditions you observe.",
        max_tokens=500,
        temperature=0.2
    )
    
    # Mostrar resultado
    print("=" * 70)
    print("RESULTADO DA ANÁLISE")
    print("=" * 70)
    print(response)
    print("=" * 70)
    
    # =========================================================================
    # EXEMPLO 2: ANÁLISE EM LOTE (opcional)
    # =========================================================================
    
    # Descomentar para analisar múltiplas imagens
    """
    image_list = [
        "C:/Users/User/Desktop/Projeto MED/Imagens teste/tuberculose.jpeg",
        "C:/Users/User/Desktop/Projeto MED/Imagens teste/pneumonia.jpeg",
        "C:/Users/User/Desktop/Projeto MED/Imagens teste/normal.jpeg"
    ]
    
    results = model.batch_analyze(
        image_paths=image_list,
        prompt="Provide a brief analysis of this chest X-ray.",
        max_tokens=500
    )
    
    # Mostrar todos os resultados
    for i, result in enumerate(results, 1):
        print(f"\n{'=' * 70}")
        print(f"IMAGEM {i}: {os.path.basename(result['image'])}")
        print(f"{'=' * 70}")
        if result['success']:
            print(result['analysis'])
        else:
            print(f"Erro: {result['error']}")
    """
    
    # =========================================================================
    # EXEMPLO 3: PROMPTS CUSTOMIZADOS
    # =========================================================================
    
    # Descomentar para testar diferentes prompts
    """
    custom_prompts = [
        "Is there any sign of pneumonia in this X-ray?",
        "Describe the lung fields and heart size.",
        "What are the differential diagnoses based on this image?",
        "Rate the image quality and suggest any improvements needed."
    ]
    
    for prompt in custom_prompts:
        print(f"\n{'=' * 70}")
        print(f"Prompt: {prompt}")
        print(f"{'=' * 70}")
        
        response = model.analyze_image(
            image_path=image_path,
            prompt=prompt,
            max_tokens=500
        )
        print(response)
    """
    
    # Estatísticas finais
    if torch.cuda.is_available():
        print(f"\n{'=' * 70}")
        print("ESTATÍSTICAS DE MEMÓRIA")
        print(f"{'=' * 70}")
        print(f"Memória máxima usada: {torch.cuda.max_memory_allocated() / 1024**3:.2f} GB")
        print(f"Memória atual: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")


if __name__ == "__main__":
    try:
        main()
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
    
    except Exception as e:
        print(f"\n\n❌ ERRO FATAL: {e}")
        print("\n📋 TROUBLESHOOTING:")
        print("1. Verifique se instalou as bibliotecas:")
        print("   pip install --upgrade transformers accelerate bitsandbytes torch")
        print("\n2. Verifique se tem VRAM suficiente (4+ GB)")
        print("\n3. Configure o HF_TOKEN:")
        print("   export HF_TOKEN='seu_token_aqui'")
        print("\n4. Se o erro persistir, tente sem quantização:")
        print("   model = MedGemmaModel(use_8bit=False)")
