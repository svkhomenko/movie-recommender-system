import { createSlice } from '@reduxjs/toolkit';
import type { IRole } from '~/types/user';

type IInitialState = {
  user: {
    id: number | undefined;
    email: string | undefined;
    role: IRole | undefined;
  };
  accessToken: string | null;
};

const initialState: IInitialState = {
  user: {
    id: undefined,
    email: undefined,
    role: undefined,
  },
  accessToken: null,
};

const profileSlice = createSlice({
  name: 'profile',
  initialState,
  reducers: {
    setUser(state, { payload }) {
      const { accessToken, ...user } = payload;
      state.user = user;
    },
    setUserAndToken(state, { payload }) {
      const { access_token, ...user } = payload;
      state.user = user;
      state.accessToken = access_token;
    },
    updateUser(state, { payload }) {
      Object.assign(state.user, payload);
    },
    setToken(state, { payload }) {
      const { access_token } = payload;
      state.accessToken = access_token;
    },
    logout(state) {
      state.user = initialState.user;
      state.accessToken = null;
    },
  },
});

export const { setUser, setUserAndToken, setToken, updateUser, logout } = profileSlice.actions;
export default profileSlice.reducer;
