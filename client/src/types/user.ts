export type IRole = 'user' | 'admin';

export type IUser = {
  id: number;
  email: string;
  role: IRole;
};

export type IAccessToken = string;
