export type IRole = 'user' | 'admin';

export type IUser = {
  id: string;
  email: string;
  role: IRole;
};

export type IAccessToken = string;
