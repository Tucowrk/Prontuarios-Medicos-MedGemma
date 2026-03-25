export interface Paciente {
  id: string;
  nomeCompleto: string;
  cpf: string;
  dataNascimento: string;
  sexo: 'Masculino' | 'Feminino' | 'Outro';
  sexoDescricao?: string; // O "?" indica que só será preenchido se a opção for 'Outro'
  endereco: string;
}

export interface Diagnostico {
  id: string;
  pacienteId: string;
  sintomas: string;
  imagemUrl?: string; // O "?" significa que não é obrigatório (nem sempre terá raio-x)
  resultadoIa: string;
  nivelUrgencia: 'Baixo' | 'Médio' | 'Alto';
  data: string;
}