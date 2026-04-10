export interface AuthToken {
  access_token: string;
  token_type: string;
  user_id: string;
}

export interface AuthUser {
  id: string;
  name: string;
  email: string;
  role: string;
  status: string;
}

export interface LoginCommand {
  email: string;
  password: string;
}
