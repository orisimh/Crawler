
import axios from "axios";
import { AuthState } from "../../types/auth";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;


export const login = async (data: AuthState) => {
  const response = await axios.post(`${API_BASE_URL}/login`, data);
  return response.data;
};