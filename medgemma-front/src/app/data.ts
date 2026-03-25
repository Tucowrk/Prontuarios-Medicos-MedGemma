export type PatientProfile = {
  name: string;
  age: string;
  sex: string;
  complaint: string;
  cid: string;
  history: string;
};

export const initialPatient: PatientProfile = {
  name: "João Silva",
  age: "45",
  sex: "Masculino",
  complaint: "Dor torácica",
  cid: "R07.4",
  history: "Paciente hipertenso, relata desconforto retroesternal há 2 horas.",
};

export const systemMetadata = {
  title: "MedGemma",
  version: "1.5-PRO",
  company: "COMPANY NAME",
};