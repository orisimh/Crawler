import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { AuthState } from "../../types/auth";
import { login } from "../../services/auth";
import axios from "axios";


const tokenFromSession = sessionStorage.getItem("token");

const initialState: AuthState = {
  username: "",
  password: "",
  website: "",
  token: tokenFromSession,
  deals: [],
  loading: false,
  error: null,
};

export const loginUser = createAsyncThunk(
  "auth/loginUser",
  async (_, { getState, rejectWithValue }: any) => {
    const state: any = getState();
    const { username, password, website } = state.auth;
    try {
      return await login({ username, password, website });
    } catch (err: any) {

      console.error("Login error:", err);

      if (!err.response || err.response.status === 401) {
        sessionStorage.removeItem("token");
        return rejectWithValue(err.response?.data?.detail || "Unauthorized: Please log in again.");
      }
      return rejectWithValue(err.response?.data?.detail || "Login failed");
    }
  }
);

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setUsername: (state, action) => { state.username = action.payload },
    setPassword: (state, action) => { state.password = action.payload },
    setWebsite: (state, action) => { state.website = action.payload },
    resetAuth: () => initialState,
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.loading = false;
        state.token = action.payload.token;
        state.deals = action.payload.deals;

        // if (action.payload.token) {
        //     sessionStorage.setItem("token", action.payload.token);
        // }
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { setUsername, setPassword, setWebsite, resetAuth } = authSlice.actions;
export default authSlice.reducer;