# 🩺 MedGemma · Clinical AI Assistant

![Status do projeto 🚀](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)

## 💻 Sobre o Projeto
O diagnóstico clínico assistido por imagem enfrenta desafios de precisão e agilidade em ambientes hospitalares de alta demanda. Este projeto, o MedGemma, aplica engenharia de software e inteligência artificial para gerar suporte diagnóstico de ponta. A plataforma integra uma interface minimalista com uma infraestrutura capaz de processar dados clínicos e imagens médicas em tempo real.

Logo, este projeto visa atuar como um ecossistema de auxílio médico, conectando o histórico do paciente a análises neurais profundas, oferecendo uma segunda opinião qualificada para profissionais de saúde.

---

## ⚙️ Funcionalidades Desenvolvidas

### 🖥️ Front-end (Experiência do Médico)
* **Design Minimalista e Glassmorphism:** Interface limpa focada em reduzir a fadiga cognitiva do profissional (Next.js, Tailwind CSS).
* **Transições Cinematográficas:** Navegação suave entre a landing page e o painel de análise para uma experiência fluida.
* **Gestão de Contexto do Paciente:** Sidebar dinâmica para entrada de metadados (Nome, Idade, CID, Queixa e Histórico Clínico).
* **Chat Multimodal:** Painel interativo para envio simultâneo de exames de imagem e texto, comunicando-se diretamente com a API.
* **Preview de Exames:** Sistema de miniatura e remoção de arquivos antes do processamento.

### 🏢 Back-end (Orquestração e Persistência)
* **Arquitetura RESTful corporativa:** API desenvolvida em Java com Spring Boot para gerenciar o tráfego de dados do hospital.
* **Persistência de Dados:** Integração com MySQL via Spring Data JPA/Hibernate, garantindo o armazenamento seguro de todo o histórico clínico e metadados estruturados (`PatientCase`).
* **Design Pattern MVC e DTO:** Estruturação limpa e escalável, separando responsabilidades entre Controllers, Services e Repositories.
* **Orquestração de Microsserviços:** Endpoint configurado para receber imagens (`MultipartFile`) e dados estruturados, atuando como o "gerente" que fará a ponte com o modelo de IA.

### 🧠 Inteligência Artificial (Próxima Fase)
* **Integração de Metadados:** O sistema enviará automaticamente o histórico estruturado para o microsserviço de IA.
* **Visão Computacional e LLMs:** Preparação da arquitetura Python/FastAPI para receber as requisições do Java e processar as imagens e laudos através do modelo MedGemma.

---

## 🛠️ Tecnologias Utilizadas

<br>

<div align="center">
  <img src="https://skillicons.dev/icons?i=nextjs" title="Next.js" alt="Next.js" />
  <img src="https://skillicons.dev/icons?i=react" title="React" alt="React" />
  <img src="https://skillicons.dev/icons?i=ts" title="TypeScript" alt="TypeScript" />
  <img src="https://skillicons.dev/icons?i=tailwind" title="Tailwind CSS" alt="Tailwind" />
  <img src="https://skillicons.dev/icons?i=python" title="Python" alt="Python" />
  <img src="https://skillicons.dev/icons?i=fastapi" title="FastAPI" alt="FastAPI" />
  <img src="https://skillicons.dev/icons?i=git" title="Git" alt="Git" />
  <img src="https://skillicons.dev/icons?i=vscode" title="VS Code" alt="VS Code" />
</div>

<br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0052D4,4364F7&height=120&section=footer" width="100%"/>
