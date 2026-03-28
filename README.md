# 🩺 MedGemma · Clinical AI Assistant

![Project Status 🚀](https://img.shields.io/badge/Status-In_Development-yellow)

## 💻 About the Project
Image-assisted clinical diagnosis faces challenges of accuracy and agility in high-demand hospital environments. This project, MedGemma, applies software engineering and artificial intelligence to generate cutting-edge diagnostic support. The platform integrates a minimalist interface with an infrastructure capable of processing clinical data and medical images in real time.

Therefore, this project aims to act as a medical assistance ecosystem, connecting the patient's history to deep neural analyses, offering a qualified second opinion for healthcare professionals.

---

## ⚙️ Developed Features

### 🖥️ Front-end (Physician Experience)
* **Minimalist Design and Glassmorphism:** Clean interface focused on reducing the professional's cognitive fatigue (Next.js, Tailwind CSS).
* **Cinematic Transitions:** Smooth navigation between the landing page and the analysis dashboard for a fluid experience.
* **Patient Context Management:** Dynamic sidebar for metadata input (Name, Age, ICD, Complaint, and Clinical History).
* **Multimodal Chat:** Interactive panel for simultaneous submission of imaging exams and text, communicating directly with the API.
* **Exam Preview:** Thumbnail and file removal system prior to processing.

### 🏢 Back-end (Orchestration and Persistence)
* **Corporate RESTful Architecture:** API developed in Java with Spring Boot to manage the hospital's data traffic.
* **Data Persistence:** Integration with MySQL via Spring Data JPA/Hibernate, ensuring the secure storage of all clinical history and structured metadata (`PatientCase`).
* **MVC and DTO Design Patterns:** Clean and scalable structuring, separating responsibilities among Controllers, Services, and Repositories.
* **Microservices Orchestration:** Endpoint configured to receive images (`MultipartFile`) and structured data, acting as the "manager" that will bridge the gap with the AI model.

### 🧠 Artificial Intelligence
* **Metadata Integration:** The system will automatically send the structured history to the AI microservice.
* **Computer Vision and LLMs:** Preparation of the Python/FastAPI architecture to receive requests from Java and process images and reports through the MedGemma model.

---

## 🛠️ Technologies Used

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
