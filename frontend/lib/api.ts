import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/v1";

export const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});
