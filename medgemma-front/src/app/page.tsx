"use client";

import * as React from "react";
import { systemMetadata, initialPatient } from "./data";

export default function Home() {
  const [isStarted, setIsStarted] = React.useState(false);
  const [mounted, setMounted] = React.useState(false);
  const [isAnalyzing, setIsAnalyzing] = React.useState(false);
  const [isTyping, setIsTyping] = React.useState(false); 
  const [zoomedImage, setZoomedImage] = React.useState<string | null>(null); 
  
  const [patient, setPatient] = React.useState(initialPatient);
  const [message, setMessage] = React.useState("");
  const [selectedImages, setSelectedImages] = React.useState<{file: File, preview: string}[]>([]);
  const [chatLog, setChatLog] = React.useState<{role: 'user' | 'ai', text: string, images?: string[]}[]>([]);
  
  const fileInputRef = React.useRef<HTMLInputElement>(null);
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  React.useEffect(() => {
    setMounted(true);
  }, []);

  React.useEffect(() => {
    scrollToBottom();
  }, [chatLog, isTyping]);

  if (!mounted) return null;

  const isSidebarComplete = Object.values(patient).every(value => 
    value !== null && value !== undefined && String(value).trim() !== ""
  );

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const filesArray = Array.from(e.target.files).map(file => ({
        file,
        preview: URL.createObjectURL(file)
      }));
      setSelectedImages(prev => [...prev, ...filesArray]);
    }
  };

  // Função auxiliar para limpar a resposta médica
  const cleanMedicalResponse = (text: string) => {
    if (!text) return "Não foi possível obter a análise.";

    // Prioridade 1: Tenta achar o padrão de saída do MedGemma Local
    const findingsIndex = text.indexOf("FINDINGS:");
    if (findingsIndex !== -1) return text.substring(findingsIndex).trim();

    // Prioridade 2: Tenta limpar se vier com o lixo do prompt (palavra 'model')
    const modelIndex = text.lastIndexOf("model");
    if (modelIndex !== -1) return text.substring(modelIndex + 5).trim();

    return text;
  };

  const handleSendMessage = async () => {
    if (!message.trim() && selectedImages.length === 0) return;
    
    const currentMessage = message;
    const currentImages = [...selectedImages];
    const imageUrls = currentImages.map(img => img.preview);
    
    // Adiciona a mensagem do usuário no chat imediatamente
    setChatLog(prev => [...prev, { role: 'user', text: currentMessage, images: imageUrls }]);
    
    // Limpa os campos de entrada
    setMessage("");
    setSelectedImages([]);
    setIsTyping(true);

    try {
      const formData = new FormData();
      formData.append('patient_data', JSON.stringify(patient));
      formData.append('message', currentMessage);
      
      if (currentImages.length > 0) {
        formData.append('files', currentImages[0].file);
      }

      // Chamada para o Backend Python
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error("Erro na resposta do servidor");

      const data = await response.json();

      // Exibe a resposta limpa da IA
      setChatLog(prev => [...prev, { 
        role: 'ai', 
        text: cleanMedicalResponse(data.analysis || "") 
      }]);

    } catch (error) {
      console.error("Erro ao conectar com a IA:", error);
      setChatLog(prev => [...prev, { 
        role: 'ai', 
        text: "Houve um erro na comunicação com o servidor. Verifique se o backend Python está rodando na porta 8000." 
      }]);
    } finally {
      setIsTyping(false);
    }
  };



  // Tailwind

  const dataAtual = new Date().toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' }).toUpperCase();
  const horaAtual = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

  return (
    <main className="min-h-screen bg-[#1A3644] p-4 flex flex-col font-sans selection:bg-[#35596C]/20 overflow-hidden">
      
      {zoomedImage && (
        <div 
          className="fixed inset-0 z-[100] bg-black/90 backdrop-blur-sm flex items-center justify-center p-10 cursor-zoom-out animate-in fade-in duration-300"
          onClick={() => setZoomedImage(null)}
        >
          <img src={zoomedImage} className="max-w-full max-h-full rounded-lg shadow-2xl" alt="Zoom" />
          <button className="absolute top-10 right-10 text-white text-4xl">&times;</button>
        </div>
      )}

      <header className="flex justify-between items-center text-white/80 text-[10px] font-bold px-2 mb-4 tracking-[0.2em] uppercase">
        <div className="flex gap-6"><span>{dataAtual}</span><span>{horaAtual}</span></div>
        <span>{systemMetadata.company}</span>
      </header>

      <div className="relative flex-1 bg-[#F8F9FA] rounded-[24px] overflow-hidden flex shadow-2xl">
        <div className="absolute inset-0 z-0 pointer-events-none opacity-40">
          <div className="bubble"></div><div className="bubble"></div><div className="bubble"></div>
        </div>

        <div className={`absolute inset-0 z-10 flex flex-col justify-center pl-[10%] md:pl-[12%] transition-all duration-1000 ease-in-out ${isStarted ? "opacity-0 pointer-events-none scale-95 blur-xl" : "opacity-100"}`}>
            <h1 className="text-[#35596C] flex flex-col leading-[0.85] font-[family-name:var(--font-plus-jakarta)]">
              <span className="text-6xl md:text-[150px] font-semibold tracking-tighter">{systemMetadata.title}:</span>
              <span className="text-5xl md:text-[150px] font-normal tracking-tighter">Assistente</span>
              <span className="text-5xl md:text-[150px] font-light tracking-tighter">Clínico IA</span>
            </h1>
            <button onClick={() => setIsStarted(true)} className="mt-10 group flex items-center gap-4 bg-[#35596C] text-white px-10 py-5 rounded-full text-lg font-medium hover:bg-[#254150] transition-all w-fit">
              Iniciar Painel <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </button>
        </div>

        <div className={`absolute inset-0 z-20 flex w-full h-full bg-white/30 backdrop-blur-2xl transition-all duration-1000 delay-100 ease-out ${isStarted ? "opacity-100 translate-y-0" : "opacity-0 pointer-events-none translate-y-12"}`}>
          
          <aside className="w-[340px] bg-white/60 border-r border-slate-200/50 flex flex-col shadow-xl flex-shrink-0">
            <div className="p-8 border-b border-slate-100/50 flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#35596C] flex items-center justify-center text-white shadow-lg"><svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div>
              <div><h2 className="text-xl font-bold text-[#35596C] leading-none">{systemMetadata.title}</h2><p className="text-[9px] text-slate-400 font-mono tracking-widest uppercase mt-1">v{systemMetadata.version}</p></div>
            </div>

            <div className="p-8 flex-1 overflow-y-auto space-y-8 scrollbar-none">
              <section className="space-y-4">
                <h3 className="text-[10px] font-black text-slate-300 uppercase tracking-[0.3em] flex items-center gap-4"> IDENTIFICAÇÃO <span className="flex-1 h-[1px] bg-slate-100"></span> </h3>
                <div className="space-y-4">
                  <div className="group"><label className="text-[9px] font-bold text-slate-400 uppercase">Nome</label>
                    <input type="text" value={patient.name} onChange={(e) => setPatient({...patient, name: e.target.value})} className="w-full bg-transparent border-b border-slate-200 py-1 text-sm text-slate-700 outline-none focus:border-[#35596C] transition-all" />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="group"><label className="text-[9px] font-bold text-slate-400 uppercase">Idade</label><input type="text" value={patient.age} onChange={(e) => setPatient({...patient, age: e.target.value})} className="w-full bg-transparent border-b border-slate-200 py-1 text-sm outline-none" /></div>
                    <div className="group"><label className="text-[9px] font-bold text-slate-400 uppercase">Sexo</label><input type="text" value={patient.sex} onChange={(e) => setPatient({...patient, sex: e.target.value})} className="w-full bg-transparent border-b border-slate-200 py-1 text-sm outline-none" /></div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="group"><label className="text-[9px] font-bold text-slate-400 uppercase">CID</label><input type="text" value={patient.cid} onChange={(e) => setPatient({...patient, cid: e.target.value})} className="w-full bg-transparent border-b border-slate-200 py-1 text-sm outline-none" /></div>
                    <div className="group"><label className="text-[9px] font-bold text-slate-400 uppercase">Caso</label><input type="text" value={patient.complaint} onChange={(e) => setPatient({...patient, complaint: e.target.value})} className="w-full bg-transparent border-b border-slate-200 py-1 text-sm outline-none" /></div>
                  </div>
                </div>
              </section>

              <section className="space-y-4">
                <h3 className="text-[10px] font-black text-slate-300 uppercase tracking-[0.3em] flex items-center gap-4"> CONTEXTO <span className="flex-1 h-[1px] bg-slate-100"></span> </h3>
                <textarea value={patient.history} onChange={(e) => setPatient({...patient, history: e.target.value})} rows={3} className="w-full p-4 bg-white/40 border border-slate-100 rounded-2xl text-xs text-slate-600 outline-none resize-none shadow-inner" />
              </section>

              <button disabled={!isSidebarComplete} onClick={() => { setIsAnalyzing(true); setChatLog([{role:'ai', text: `Pronto para análise. Por favor, anexe os exames de imagem.`}])}} className={`w-full py-4 rounded-2xl font-bold text-[10px] uppercase tracking-[0.2em] transition-all ${isSidebarComplete ? "bg-[#35596C] text-white shadow-lg cursor-pointer" : "bg-slate-100 text-slate-300 cursor-not-allowed"}`}>
                {isAnalyzing ? "Sessão Ativa" : "Iniciar Análise"}
              </button>
            </div>
          </aside>

          <main className="flex-1 flex flex-col min-w-0">
            <div className="h-[80px] flex justify-end items-center px-10">
              <button onClick={() => {setIsStarted(false); setIsAnalyzing(false); setChatLog([]);}} className="text-[10px] font-black text-slate-300 hover:text-[#35596C] transition-all tracking-[0.2em] uppercase">Encerrar Sessão</button>
            </div>

            <div className="flex-1 overflow-y-auto px-10 space-y-6 scrollbar-none pb-4">
              {!isAnalyzing ? (
                <div className="h-full flex flex-col items-center justify-center text-center opacity-40">
                  <svg className="w-16 h-16 mb-4 text-slate-300" fill="none" stroke="currentColor" strokeWidth="1" viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                  <p className="text-sm font-light">Aguardando ativação dos dados clínicos...</p>
                </div>
              ) : (
                <div className="max-w-4xl mx-auto space-y-6">
                  {chatLog.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-in fade-in slide-in-from-bottom-2`}>
                      <div className={`max-w-[75%] p-4 rounded-[22px] text-sm shadow-sm ${msg.role === 'user' ? 'bg-[#35596C] text-white rounded-tr-none' : 'bg-white text-slate-600 border border-slate-100 rounded-tl-none'}`}>
                        {msg.images?.map((url, i) => (
                          <img key={i} src={url} onClick={() => setZoomedImage(url)} className="h-32 rounded-lg mb-3 cursor-zoom-in hover:brightness-90 transition-all" alt="Exame" />
                        ))}
                        <p className="leading-relaxed whitespace-pre-wrap">{msg.text}</p>
                      </div>
                    </div>
                  ))}
                  
                  {isTyping && (
                    <div className="flex justify-start animate-in fade-in duration-300">
                      <div className="bg-white/50 border border-slate-100 p-4 rounded-[22px] rounded-tl-none flex items-center gap-2">
                        <span className="text-[10px] font-bold text-[#35596C] animate-pulse uppercase tracking-widest">MedGemma está analisando</span>
                        <div className="flex gap-1">
                          <span className="w-1 h-1 bg-[#35596C] rounded-full animate-bounce"></span>
                          <span className="w-1 h-1 bg-[#35596C] rounded-full animate-bounce [animation-delay:0.2s]"></span>
                          <span className="w-1 h-1 bg-[#35596C] rounded-full animate-bounce [animation-delay:0.4s]"></span>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </div>
              )}
            </div>

            <div className="p-10 pt-0">
              <div className="max-w-4xl mx-auto space-y-4">
                {selectedImages.length > 0 && (
                  <div className="flex gap-3 px-4 animate-in slide-in-from-bottom-2">
                    {selectedImages.map((img, i) => (
                      <div key={i} className="relative group">
                        <img src={img.preview} className="w-16 h-16 object-cover rounded-xl border-2 border-white shadow-md" alt="Preview" />
                        <button onClick={() => setSelectedImages(prev => prev.filter((_, idx) => idx !== i))} className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-5 h-5 text-[10px] flex items-center justify-center shadow-lg">✕</button>
                      </div>
                    ))}
                  </div>
                )}
                <div className={`flex items-center gap-4 bg-white/80 border border-slate-200 p-3 rounded-[26px] shadow-sm backdrop-blur-md transition-all ${!isAnalyzing && 'opacity-40 pointer-events-none grayscale'}`}>
                  <input type="file" ref={fileInputRef} className="hidden" multiple accept="image/*" onChange={handleFileSelect} />
                  <button onClick={() => fileInputRef.current?.click()} className="p-3 text-slate-300 hover:text-[#35596C] transition-colors"><svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" /></svg></button>
                  <input type="text" value={message} onChange={(e) => setMessage(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()} placeholder="Descreva os achados clínicos..." className="flex-1 bg-transparent outline-none text-sm text-slate-600 placeholder:text-slate-300 font-medium" />
                  <button onClick={handleSendMessage} disabled={isTyping} className={`${isTyping ? "bg-slate-300" : "bg-[#35596C] hover:scale-105"} text-white w-12 h-12 rounded-2xl flex items-center justify-center transition-all shadow-lg`}><svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24"><path d="M22 2 11 13M22 2 15 22 11 13 2 9l20-7z"/></svg></button>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </main>
  );
}