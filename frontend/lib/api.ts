import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/v1";

export const api = axios.create({
  baseURL: API_URL,
  // 5s era pouco pra listagem completa de turmas (~2 MB) em produção e o
  // dashboard dava timeout. Enquanto a API não pagina, espera mais.
  timeout: 15000,
});
