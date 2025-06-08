
export interface AuthState {
  username: string;
  password: string;
  website: string;
  token?: string | null;
  deals?: string[];
  loading?: boolean | false;
  error?: string | null;
}