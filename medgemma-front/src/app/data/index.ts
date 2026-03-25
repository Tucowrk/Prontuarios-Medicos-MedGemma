// Configurações Gerais e Metadados do Sistema
export const systemMetadata = {
  title: "MedGemma",
  version: "1.5-PRO",
  model: "medgemma-7b-it",
  company: "COMPANY NAME",
};

// Estrutura de dados do paciente (Modelo inicial)
export interface PatientProfile {
  name: string;
  age: string;
  sex: string;
  complaint: string;
  cid: string;
  history: string;
}

export const initialPatient: PatientProfile = {
  name: "João Silva",
  age: "45",
  sex: "Masculino",
  complaint: "Dor torácica",
  cid: "R07.4",
  history: "Paciente hipertenso, relata desconforto retroesternal há 2 horas.",
};

// Sugestões de Análise (Sidebar)
export const quickActions = [
  { id: 'rad', label: "Radiografia de Tórax", icon: "🫁" },
  { id: 'diag', label: "Diagnósticos Diferenciais", icon: "📋" },
  { id: 'tech', label: "Qualidade Técnica", icon: "⚙️" },
];

// Sugestões do Chat (Empty State)
export const chatSuggestions = [
  "Analise os campos pulmonares",
  "Avalie a silhueta cardíaca",
  "Existe sinal de congestão?",
];