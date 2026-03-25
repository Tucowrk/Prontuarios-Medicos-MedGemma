"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [isStarted, setIsStarted] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const dataAtual = mounted ? new Date().toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' }).toUpperCase() : '';
  const horaAtual = mounted ? new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) : '';

  return (
    <main className="min-h-screen bg-[#1A3644] p-4 flex flex-col font-sans">
      
      {/* Cabeçalho */}
      <header className="flex justify-between items-center text-white text-sm font-semibold px-2 mb-4 tracking-wider">
        <div className="flex gap-4">
          <span>DATE {dataAtual}</span>
          <span>{horaAtual}</span>
        </div>
        <span>COMPANY NAME</span>
      </header>

      {/* Cartão Central Branco */}
      <div className="relative flex-1 bg-[#F8F9FA] rounded-[20px] overflow-hidden shadow-2xl shadow-black/20">
        
        {/* Bolhas Flutuantes (Fundo contínuo) */}
        <div className="absolute inset-0 z-0 pointer-events-none">
          <div className="bubble"></div>
          <div className="bubble"></div>
          <div className="bubble"></div>
          <div className="bubble"></div>
          <div className="bubble"></div>
        </div>

        <div 
          className={`absolute inset-0 z-10 flex flex-col justify-center pl-[10%] md:pl-[15%] transition-all duration-1000 ease-in-out ${
            isStarted ? "opacity-0 pointer-events-none scale-95 blur-sm" : "opacity-100 scale-100 blur-0"
          }`}
        >
          <div className="flex flex-col items-start">
            <h1 className="text-[#35596C] flex flex-col leading-[0.9] font-[family-name:var(--font-plus-jakarta)] text-left">
              <span className="text-6xl md:text-[150px] font-semibold tracking-tight">
                MedGemma:
              </span>
              <span className="text-5xl md:text-[150px] font-normal tracking-tight">
                Assistente
              </span>
              <span className="text-5xl md:text-[150px] font-light tracking-tight">
                Clínico IA
              </span>
            </h1>

            <button 
              onClick={() => setIsStarted(true)}
              className="mt-12 group flex items-center justify-center gap-4 bg-[#35596C] text-white px-8 py-4 rounded-full text-xl font-medium hover:bg-[#254150] transition-all w-max shadow-lg shadow-[#35596C]/20"
            >
              Iniciar Painel
              <svg className="w-6 h-6 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </button>
          </div>
        </div>


        <div 
          className={`absolute inset-0 z-20 flex w-full h-full bg-white/60 backdrop-blur-md transition-all duration-1000 delay-150 ease-out ${
            isStarted ? "opacity-100 translate-y-0" : "opacity-0 pointer-events-none translate-y-8"
          }`}
        >
          
          <aside className="w-[320px] bg-white/80 border-r border-slate-200 flex flex-col flex-shrink-0">
            <div className="p-5 border-b border-slate-200 flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#35596C] to-[#4A8FC4] flex items-center justify-center text-white">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
              </div>
              <div>
                <h2 className="text-sm font-bold text-[#35596C]">MedGemma</h2>
                <p className="text-[10px] text-slate-500 font-mono">CLINICAL AI · v1.5</p>
              </div>
            </div>

            <div className="p-5 flex-1 overflow-y-auto space-y-6 scrollbar-thin scrollbar-thumb-slate-200">
              <section>
                <h3 className="text-[10px] font-bold tracking-widest text-slate-400 uppercase mb-4 flex items-center gap-2">
                  Contexto do Paciente <span className="flex-1 h-px bg-slate-200"></span>
                </h3>
                <div className="space-y-3">
                  <input type="text" placeholder="Nome do paciente" className="w-full bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg px-3 py-2.5 focus:outline-none focus:border-[#35596C] focus:bg-white transition-colors" />
                  <div className="grid grid-cols-2 gap-3">
                    <input type="text" placeholder="Idade" className="w-full bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg px-3 py-2.5 focus:outline-none focus:border-[#35596C] focus:bg-white transition-colors" />
                    <input type="text" placeholder="Sexo" className="w-full bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg px-3 py-2.5 focus:outline-none focus:border-[#35596C] focus:bg-white transition-colors" />
                  </div>
                  <input type="text" placeholder="CID / Queixa principal" className="w-full bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg px-3 py-2.5 focus:outline-none focus:border-[#35596C] focus:bg-white transition-colors" />
                  <textarea placeholder="Histórico clínico, comorbidades, alergias..." rows={4} className="w-full bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg px-3 py-2.5 focus:outline-none focus:border-[#35596C] focus:bg-white transition-colors resize-none"></textarea>
                </div>
              </section>

              <section>
                <h3 className="text-[10px] font-bold tracking-widest text-slate-400 uppercase mb-3 flex items-center gap-2">
                  Análises Rápidas <span className="flex-1 h-px bg-slate-200"></span>
                </h3>
                <div className="space-y-2">
                  <button className="w-full text-left p-3 rounded-lg border border-slate-200 bg-white hover:border-[#35596C] hover:shadow-sm transition-all text-xs text-slate-600 flex items-start gap-2">
                    <svg className="w-4 h-4 text-[#4A8FC4] shrink-0 mt-0.5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
                    Analise esta radiografia e descreva achados.
                  </button>
                  <button className="w-full text-left p-3 rounded-lg border border-slate-200 bg-white hover:border-[#35596C] hover:shadow-sm transition-all text-xs text-slate-600 flex items-start gap-2">
                    <svg className="w-4 h-4 text-[#4A8FC4] shrink-0 mt-0.5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M9 12h6M12 9v6M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/></svg>
                    Liste diagnósticos diferenciais do caso.
                  </button>
                </div>
              </section>
            </div>
          </aside>

          <main className="flex-1 flex flex-col relative">
            
            <div className="h-[65px] border-b border-slate-200 flex justify-end items-center px-6">
              <button 
                onClick={() => setIsStarted(false)} 
                className="text-xs font-semibold text-slate-400 hover:text-slate-700 transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M15 19l-7-7 7-7"/></svg>
                Voltar ao Início
              </button>
            </div>

            <div className="flex-1 overflow-y-auto flex flex-col items-center justify-center p-8">
              <div className="w-16 h-16 bg-[#EDF5FB] border border-[#C2DDEF] rounded-2xl flex items-center justify-center mb-6 shadow-sm">
                <svg className="w-8 h-8 text-[#2D6EAA]" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
              </div>
              <h2 className="text-xl font-semibold text-[#1A3644] mb-2">Pronto para análise clínica</h2>
              <p className="text-slate-500 text-sm max-w-sm text-center font-light leading-relaxed">
                Envie uma imagem médica (radiografia, tomografia, ressonância) e descreva a hipótese clínica para uma análise assistida por IA.
              </p>
              <div className="flex flex-wrap justify-center gap-2 mt-6">
                <span className="px-4 py-1.5 border border-slate-200 rounded-full text-xs text-slate-500 cursor-pointer hover:bg-slate-50 transition-colors">Radiografia de tórax</span>
                <span className="px-4 py-1.5 border border-slate-200 rounded-full text-xs text-slate-500 cursor-pointer hover:bg-slate-50 transition-colors">TC de abdome</span>
                <span className="px-4 py-1.5 border border-slate-200 rounded-full text-xs text-slate-500 cursor-pointer hover:bg-slate-50 transition-colors">Ressonância magnética</span>
              </div>
            </div>

            <div className="p-6 pt-0">
              <div className="max-w-3xl mx-auto bg-white border border-slate-200 rounded-2xl shadow-sm focus-within:border-[#35596C] focus-within:shadow-md transition-all overflow-hidden flex items-end">
                <button className="p-4 text-slate-400 hover:text-[#35596C] transition-colors">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
                </button>
                <textarea 
                  placeholder="Descreva o caso clínico ou faça uma pergunta..." 
                  className="flex-1 max-h-[120px] py-4 bg-transparent border-none outline-none resize-none text-slate-700 text-sm font-light placeholder:text-slate-400"
                  rows={1}
                ></textarea>
                <div className="p-3">
                  <button className="w-9 h-9 bg-gradient-to-br from-[#35596C] to-[#4A8FC4] rounded-full flex items-center justify-center text-white hover:scale-105 transition-transform shadow-sm">
                    <svg className="w-4 h-4 ml-0.5" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24"><path d="M22 2 11 13M22 2 15 22 11 13 2 9l20-7z"/></svg>
                  </button>
                </div>
              </div>
              <p className="text-center text-[10px] font-mono text-slate-400 mt-3">
                <span className="bg-slate-100 border border-slate-200 rounded px-1.5 py-0.5">Enter</span> para enviar · MedGemma é uma ferramenta de suporte.
              </p>
            </div>

          </main>
        </div>

      </div>
    </main>
  );
}